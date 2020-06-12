"""
Module board.py
===============

This module contains the implementation of the Board and Token classes
"""
import copy
from math import inf
from typing import Any, Iterable, Set, Union

from pygame.locals import MOUSEBUTTONUP

from src.ai import has_won, alpha_beta
from src.constants import *
from src.player import Player

__all__ = ['Board', 'Token']
__version__ = '0.1'
__author__ = 'Eric G.D'


class Token:

    def __init__(self, color: str = None, outline: str = 'normal'):
        self.color: str = color
        self.outline: str = outline

    def __bool__(self) -> bool:
        return bool(self.__color)

    def __eq__(self, other: Any) -> bool:
        return isinstance(other, Token) and other.color == self.color and other.__outline == self.__outline

    def __str__(self) -> str:
        return self.color[0].title()

    def __repr__(self) -> str:
        return f'Token({self.__color!r}, {self.__outline!r})'

    @property
    def color(self) -> str:
        return self.__color

    @color.setter
    def color(self, color: str):
        if color is not None and color not in Board.images['token'].keys():
            raise ValueError(f"'{color}' is not a valid token color!")
        self.__color = color

    @property
    def outline(self) -> str:
        return self.__outline

    @outline.setter
    def outline(self, outline: str) -> None:
        if outline is not None and outline not in Board.images['board'].keys():
            raise ValueError(f"'{outline}' is not a valid token outline!")
        self.__outline = outline


class Board:
    clock: 'pygame.time.Clock' = None
    images: ImageDict = {}
    old_rects: List[pygame.Rect] = []
    resolutions: ResDict = {}

    difficulty: Dict[str, int] = {
        'very easy': 1,
        'easy': 2,
        'medium': 3,
        'hard': 5,
        'expert': 7
    }

    def __init__(self, rows: int, cols: int, players: Tuple[Player, Player]):
        self.__rows: int = rows
        self.__cols: int = cols
        self.__turn_num: int = 0
        self.__extra_token_pos: Position = (0, 0)
        self.__center_extra_token: bool = False
        self.__board: List[List[Token]] = [[Token() for _ in range(cols)] for _ in range(rows)]
        self.__prev_boards: List[List[List[Token]]] = []  # Will be used to store move history
        self.__players: Tuple[Player, Player] = players
        self.__available_moves: Set[int] = set(range(cols))

    def __len__(self) -> int:
        return len(self.__board)

    def __iter__(self) -> Iterable[List[Token]]:
        return iter(self.__board)

    def convert(self) -> GameState:
        """
        :return: A simplified version of this object for use in the negamax algorithm
        """
        return [[token.color for token in row] for row in self.__board]

    def negamax(self, depth: str = None) -> int:
        """
        :param depth:   A key for Board.difficulty used to get the maximum search depth
        :return: The best column to pick for the next turn
        """
        board = self.convert()
        move_set = copy.deepcopy(self.__available_moves)
        depth = Board.difficulty.get(depth, Board.difficulty['medium'])
        color = self.get_current_player().color
        return alpha_beta(board, color, move_set, -inf, inf, depth)

    def get_current_player(self) -> Player:
        """
        :return: The player who is currently playing
        """
        return self.__players[self.__turn_num % len(self.__players)]

    def get_winning_player(self) -> Union[str, None]:
        """
        :return: The color of the player who has won, None otherwise
        """
        return self.get_current_player().color if has_won(self.convert()) else None

    def is_full(self) -> bool:
        """
        :return: True if there are no empty spaces in the board, False otherwise
        """
        # return self.__turn_num >= self.tile_num
        return not self.__available_moves

    def lowest_space(self, column: int) -> int:
        """
        :param column: The column to check
        :return: The index of lowest empty slot in :column:
        """
        return next((i for i in range(self.rows) if not self.__board[i][column]), -1)

    def column_full(self, column: int) -> bool:
        """
        :param column:  The index of a column
        :return: True if the column is full, False otherwise
        """
        return self.__board[-1][column].color is not None

    def insert(self, surface: pygame.Surface, column: int, color: str) -> None:
        """
        Inserts a :color: token into :board:'s :column:th column
        :param surface: The surface object to draw the new token on
        :param column:  The index of the column that the new token will be inserted into
        :param color:   The color of the new token
        :return: None
        """
        if not 0 <= column < self.cols:
            raise ValueError(f'Invalid column index, {column} is not between 0 and {self.cols}')
        if column not in self.__available_moves:
            raise ValueError(f'Cannot insert token into column {column} as it is full.')
        row = self.lowest_space(column)
        self.animate_token(surface, FPS, column, color)
        self.__prev_boards.append(copy.deepcopy(self.__board))
        self.__board[row][column] = Token(color)
        self.__turn_num += 1
        if row == self.rows - 1:
            self.__available_moves.remove(column)

    def draw(self, surface: pygame.Surface, fps: int = 0, extra_token: str = None) -> None:
        """
        Draws the board onto :surface: using the images from Board.images
        :param surface:     The surface to blit onto
        :param fps:         The game's maximum framerate
        :param extra_token: An additional token, drawn above the board on a human player's turn or
                            in the board while dropping a token
        :return: None
        """
        surface.fill(Colors.background)
        x_margin, y_margin = Board.resolutions['margin']
        above_board_rect = pygame.Rect(x_margin, 0,
                                       Board.resolutions['window'][0] - (2 * x_margin), y_margin)
        rects = [above_board_rect]
        if extra_token:
            extra_rect = pygame.Rect(self.extra_token_pos, Board.resolutions['token'])
            if self.__center_extra_token:
                extra_rect.center = self.extra_token_pos
            surface.blit(Board.images['token'][extra_token], extra_rect)
            # surface.fill(Colors.orange, extra_rect)  # Debug
            rects.append(extra_rect)
        for i in range(self.cols):
            for j in range(self.rows):
                pos = tuple(Board.resolutions['margin'][k] +
                            ((i, j)[k] * Board.resolutions['token'][k]) for k in range(2))
                current_space = pygame.Rect(pos, Board.resolutions['token'])
                # TODO: Fixing :pos: typing error
                indexes = -(j + 1), i
                piece = self.__board[indexes[0]][indexes[1]]
                if piece:
                    surface.blit(Board.images['token'][piece.color], current_space)
                surface.blit(Board.images['board'][piece.outline], current_space)
                if not self.__prev_boards or piece != self.__prev_boards[-1][indexes[0]][indexes[1]]:
                    rects.append(current_space)
        pygame.display.update(rects + Board.old_rects)
        Board.clock.tick(fps)
        Board.old_rects[:] = rects

    def animate_token(self, surface: pygame.Surface, fps: int = FPS, column: int = 0, color: str = None) -> None:
        """
        Animates a token falling into the a column
        :param surface: The surface to animate the token on
        :param fps:     Maximum refresh rate for the animation
        :param color:   The color of the token to be animated
        :param column:  The column the token has been inserted into
        :return: None
        """
        if not 0 <= column <= self.cols:
            raise ValueError(f'{column} is not a valid insertion index!')
        if color is None:
            color = self.get_current_player().color
        pygame.event.set_blocked(MOUSEBUTTONUP)
        row = self.lowest_space(column)
        x = Board.resolutions['margin'][0] + column * Board.resolutions['board'][0]  # The x coordinate of the token
        y = Board.resolutions['margin'][1] // 4
        acceleration = Board.resolutions['token'][1] / fps
        velocity = 0
        while True:
            pygame.event.pump()  # Let pygame handle events while animating
            y += int(velocity)
            velocity += acceleration
            if y - Board.resolutions['margin'][1] >= (self.rows - row - 1) * Board.resolutions['token'][1]:
                break
            self.set_extra_token(x, y, is_centred=False)
            self.draw(surface, fps, extra_token=color)
        pygame.event.set_allowed(MOUSEBUTTONUP)

    @property
    def rows(self) -> int:
        return self.__rows

    @property
    def cols(self) -> int:
        return self.__cols

    @property
    def tile_num(self) -> int:
        return self.__rows * self.__cols

    @property
    def extra_token_pos(self):
        return self.__extra_token_pos

    def set_extra_token(self, x: int = None, y: int = None, is_centred: bool = True) -> None:
        """
        :param x:
        :param y:
        :param is_centred:  True if the token should be centered around :pos:, False if :pos: is the top-left corner
        :return:            None
        """
        # TODO: Document this function
        x_margin, y_margin = Board.resolutions['margin']
        token_size = Board.resolutions['token'][0]
        if x is None:
            x = min(max(pygame.mouse.get_pos()[0], x_margin + token_size // 2),
                    Board.resolutions['window'][0] - (x_margin + token_size // 2))
        y = y_margin // 2 if y is None else y
        self.__extra_token_pos = x, y
        self.__center_extra_token = is_centred
