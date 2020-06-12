# --- Imports ---


import copy
import logging
import os.path
import pprint
import random
import sys
import time
from math import gcd

import pygame
import pygame.locals as pygl

from classes import *
from config import *

# --- Setup ---

# TODO: Add and rewrite functions from terminal.py to graphic.py
# TODO: Create player selection menu
# TODO: Add Minimax AI algorithm

# +++ Logging +++

logging.basicConfig(filemode='a',
                    filename='ConnectPyGraphicLog.txt',
                    format='%(asctime)s - %(levelname)s - %(message)s',
                    level=logging.INFO)
# logging.disable()


# +++ Globals +++

"""
res_dict    -   A dict containing the resolution of all game images
image_dict  -   A dict of dicts that contain image objects, separated by type
margins     -   A list containing the x and y margins of the window
old_rects   -   A list of rectangles that were to be updated

clock       -   The game's FPS clock
display     -   The window's Surface object
end_image   -   The image that will be displayed at the end of the game
end_rect    -   A rectangle containing the location of where *end_image_ will be displayed
font        -   An object containing the font used to render text

board       -   A matrix containing the values of the board
menu        -   A tuple containing the surface and rectangle of the player_sel menu
player      -   A reference to the current player
turn_num    -   The number of turns that have passed
players     -   A list containing player objects
moves       -   A set containing all the moves that the computer can make
"""

res_dict, image_dict = {}, {}
margins, old_rects = [], []
clock = display = end_image = end_rect = None
font = None
board = menu = player = None
turn_num = -1
players, moves = [], {}


# +++ Functions +++


def res_dict_setup(w=None):
    """
    Generates a dictionary containing the resolution of all of the game's elements
    Stores the dict in the res_dict global
    :param w  The window resolution
    :return: None
    """
    global res_dict
    info = pygame.display.Info()        # Contain information about the screen
    s = info.current_w, info.current_h  # Stores screen resolution
    if not w:                           # If a window resolution wasn't specified
         w = tuple(x // 2 for x in s)
    m = tuple(x // 4 * 3 for x in w)    # Menu size
    ch = b = (gcd(*w),) * 2    # Board and checker resolution
    end = (w[0] // 4,) * 2              # End message resolution
    res_dict = {'screen': s, 'window': w, 'checker': ch, 'board': b, 'end': end}
    logging.info('res_dict generated.')
    logging.debug('res_list = %s' % str(res_dict))


def image_setup(file_name, res):
    """
    Loads and scales an image
    :param path: The image's name
    :param res: The scaled image's resolution
    :return: A loaded and scaled image object with transparency
    """
    img = pygame.image.load(os.path.join(ASSETS_PATH, file_name)).convert_alpha()
    return pygame.transform.scale(img, res)


def image_dict_setup():
    """
    Makes a dictionary filled with images from all files that start with string
    Stores the dictionary in the image_dict global
    :return: None
    """
    global res_dict, image_dict
    start_tuple = tuple(res_dict.keys())[2:]    # Tuple containing file prefixes
    image_dict = {start: {} for start in start_tuple}
    for f in os.listdir(ASSETS_PATH):
        if not f.endswith('.png'):   # If file is not an image
            continue
        start, end = f.split('_')        # Start - Gets the file prefx
        end = end.split('.')[0]             # End - Gets the part of the file name between start and the file extension
        if start in start_tuple:            # If the start is valid
            image_dict[start][end] = image_setup(f, res_dict[start])
    logging.info('image_dict generated.')
    logging.debug('img_dict = %s' % str(image_dict))


def video_setup():
    """
    Sets the PyGame graphics up
    :return:    A tuple containing the clock and display objects
    """
    global clock, display, end_rect, font, image_dict, res_dict, margins, x_margin, y_margin

    os.environ['SDL_VIDEO_CENTERED'] = 'True'  # Make the window open in the centre of the screen
    pygame.init()
    res_dict_setup()
    clock = pygame.time.Clock()
    display = pygame.display.set_mode(res_dict['window'])
    pygame.display.set_caption(TITLE)
    pygame.display.set_icon(pygame.image.load(asset_path('icon_icon.png')))
    display.fill(BG_COLOR)
    pygame.display.update()
    margins = x_margin, y_margin = [(res_dict['window'][i] - (BOARD_DIM[i] * res_dict['checker'][i])) // 2 for i in range(2)]
    image_dict_setup()
    end_rect = image_dict['end']['red'].get_rect()
    end_rect.center = tuple(x // 2 for x in res_dict['window'])
    font = pygame.font.Font(asset_path('visitor.ttf'), min(res_dict['window']) // 10)
    logging.info('Video set up.')


def board_gen():
    """
    :return:    Generates a board with *cfg.ROWS* rows and *cfg.COLUMNS* columns
    """
    logging.info('New board generated.')
    return [[EMPTY for _ in range(COLUMNS)] for _ in range(ROWS)]


def global_setup():
    """
    Initialises the global variables
    :return:    None
    """
    global board, turn_num, moves
    board = board_gen()
    turn_num = 0
    moves = set(range(COLUMNS))
    player = None
    logging.info('Global variables initialised.')


def player_selector():
    """
    Initialises the players list with 2 Human players
    :return: None
    """
    players.extend(Player(i + 1, True) for i in range(2))


def event_setup():
    """
    Sets which events are to be allowed and blocked
    :return:    None
    """
    block_list = [item for name, item in vars(pygl).items() if name.startswith('JOY')]  # Blocks Controller input
    logging.debug('blocked - %s' % str(block_list))
    pygame.event.set_blocked(block_list)


# --- Front-End Functions ---

def draw_board(end=(False, []), extra_token=None):
    """
    Draws the board
    :param end:         Whether the game has ended or not and a list of winning spaces
    :param extra_token: The falling token
    :return:
    """
    global board, clock, display, image_dict, res_dict, old_rects
    display.fill(BG_COLOR)
    rects = []     # List of updated rectangles
    space_size = res_dict['board'][0]   # The length and width of a single space
    board_rect = pygame.Rect(0, 0, space_size, space_size)  # Rectangle of the current space
    if extra_token:     # If a token has been dropped
        rect = pygame.Rect(extra_token['pos'], res_dict['checker'])
        display.blit(image_dict['checker'][extra_token['color']], rect)
        rects.append(rect)
    for x in range(COLUMNS):   # Draws tokens and board
        for y in range(ROWS):
            board_rect.topleft = (x_margin + (x * space_size), y_margin + (y * space_size))
            piece = board[ROWS - y - 1][x]
            if piece != EMPTY:    # Insert token
                display.blit(image_dict['checker'][piece], board_rect)
            key = 'win' if end[0] and (ROWS - y - 1, x) in end[1] else 'normal'
            display.blit(image_dict['board'][key], board_rect)
            rects.append(copy.deepcopy(board_rect))
    if end[0]:     # Draws end message
        global end_image, end_rect
        display.fill(WHITE, end_rect)
        display.blit(end_image, end_rect)
        rects.append(end_rect)
    update_rects = rects + old_rects
    pygame.display.update(update_rects)
    clock.tick(FPS)
    old_rects[:] = rects


def animate_token(column):
    """
    Animates the falling token
    :param column:  The column the token has been inserted into
    :return: None
    """
    global player
    x = margins[0] + column * res_dict['board'][0]  # The x coordinate of the token
    y = margins[1] - res_dict['board'][1]   # The y coordinate of the token
    drop_speed = 0    # The token's velocity
    lowest = lowest_space(column)
    while True:
        y += int(drop_speed)
        drop_speed += 2
        if (y - margins[1]) >= (HEIGHT - lowest - 1) * res_dict['checker'][1]:
            return
        draw_board(extra_token={'pos': (x, y), 'color': player.color})


def display_winner(win_slots):
    """
    Displays the winner and waits for the user to exit or start a new game
    :param win_slots:   A list of winning indexes
    :return:    None
    """
    flag = True
    while flag:     # Until a new game has started or the program has exited
        flag = handle_events(end=True)
        draw_board(end=(True, win_slots))


# +++ Back-end Fucntions +++


def handle_events(end=False):
    """
    Handles events such as quitting, window resizing and mouse clicks
    :param end:
    :return:
    """
    for event in pygame.event.get():
        if event.type == pygl.QUIT or (event.type == pygl.KEYUP and event.key == pygl.K_ESCAPE):
            exit_game()
        if event.type == pygl.MOUSEBUTTONUP:
            return False if end else pygame.mouse.get_pos()
    return end


def exit_game():
    """
    Exits the program
    :return: None
    """
    logging.info("### END OF PROGRAM ###")
    pygame.quit()
    sys.exit()


def board_full():
    """
    :return:    If the board is full or not
    """
    return turn_num + 1 >= TILE_NUM


def turn():
    """
    Performs the player's turn
    :return:        The column where the newest checker was placed
    """
    global player
    column = human_turn() if player.is_human else ai_turn()     # The column where the player has moved
    return insert(column, player.color)


def human_turn():
    """
    Performs a human player's turn
    :return:       The column where the newest checker was placed
    """
    while True:
        draw_board()
        mouse = handle_events()     # The location of the mouse
        if mouse:
            column = token_location(mouse)
            if isinstance(column, int):     # If the column was valid
                return column


def token_location(mouse):
    """
    :param mouse:   The location of the mouse
    :return:        The column of the played counter
    """
    global margins
    x, y = mouse    # The x and y coordinates of the mouse
    if margins[0] <= x <= res_dict['window'][0] - margins[0] and y <= (res_dict['window'][1] - margins[1]):
        # If board was clicked
        column = (x - margins[0]) // res_dict['board'][0]
        if not column_full(column):
            return column


def ai_turn():
    """
    Performs an AI player's turn
    :return:        The column where the newest checker was inserted
    """
    global moves
    is_full = True
    while is_full:
        column = random.sample(moves, 1)[0]
        is_full = column_full(column)
    return column


def insert(column, color):
    """
    :param column:  The column to insert the checker
    :param color:   The color of the checker
    :return:        None
    """
    if not column_check(column):
        logging.error('column = %s' % str(column))
        raise ValueError('Invalid column entered or column is full.')
    animate_token(column)
    row = lowest_space(column)
    board[row][column] = color
    logging.info('%s tile placed at (%d, %d)' % (color, row, column))
    return row, column


def lowest_space(column):
    """
    :param column: The column to check
    :return:       The index of lowest slot in the column that is empty
    """
    for i in range(ROWS):
        logging.debug('column = %d, i = %d' % (column, i))
        if board[i][column] == EMPTY:
            return i


def column_check(column):
    """
    :param column:  The column to check
    :return:        If the column is valid
    """
    return 0 <= column < COLUMNS and not column_full(column)


def column_full(column):
    """
    :param column:  The column to check
    :return:        If the column is full
    """
    return board[-1][column] != EMPTY


def game_loop():
    """
    The main game loop
    :return:    None
    """
    global player, players, turn_num, end_image, board
    while True:     # Game loop
        player = players[turn_num % 2]          # The current player
        prev_turn = turn()                # The turn that was just played
        win_vals = has_won(prev_turn)     # If the player has won and the indexes of the winning rows
        if win_vals[0]:                                 # If the player has won
            end_image = image_dict['end'][player.color]
            logging.info(str(player) + ' Wins!')
            break
        if board_full():    # If there is a tie
            end_image = image_dict['end']['tie']
            logging.info('It\'s a tie!')
            break
        turn_num += 1
    players.insert(0, players.pop(turn_num % PLAYER_NUM))
    display_winner(win_vals[1])


def has_won(index):
    """
    :param index:        The indexes of the previous turn
    :return:            Whether or not the player has won
    """
    color = board[index[0]][index[1]]
    logging.debug('color = %s' % color)
    logging.debug('index = %s' % str(index))
    i = 0           # i - mults index iterator
    val = False     # If the player has won or not
    while i < len(MULTS):   # While all the rows haven't been checked
        flip_counter = 0    # Times x and y have been flipped (Only needs to be flipped once)
        tile_counter = 0    # Counts number of adjacent tiles
        win_slots = [index]      # The indexes of the winning tiles
        while flip_counter < 2:     # While both directions of the row haven't been checked
            j = 1   # Counts how much to add to the current index
            xi, yi = tuple(index + mult * j for index, mult in zip(index[:2], MULTS[i]))
            logging.debug('xi = %d, yi = %d' % (xi, yi))
            while j < WIN_LEN and 0 <= xi < ROWS and 0 <= yi < COLUMNS:     # While the indexes are in range and not won
                if board[xi][yi] == color:  # If the space contains the player's tile
                    tile_counter += 1
                    win_slots.append((xi, yi))
                else:
                    win_slots = (win_slots if val else [index])
                    break
                logging.debug('tile_counter = %d' % tile_counter)
                if tile_counter == WIN_LEN - 1:
                    val = True
                j += 1
                xi, yi = tuple(index + mult * j for index, mult in zip(index[:2], MULTS[i]))
                logging.debug('xi = %d, yi = %d' % (xi, yi))
            if val and (flip_counter == 1 or i == 0):
                # If player has won and all winning indexes were found
                return val, win_slots
            if MULTS[i] == DOWN:  # No need to check above the recently placed counter
                break
            MULTS[i] = tuple(-x for x in MULTS[i])  # Flips the values of the multipliers
            flip_counter += 1
        i += 1
    return val, []


# --- Main ---


def main():
    """
    The program's main function
    :return:    None
    """
    logging.info('### START OF PROGRAM ###')
    video_setup()
    player_selector()
    while True:
        global_setup()
        game_loop()
        logging.info('## Starting new game... ##')


if __name__ == '__main__':
    main()