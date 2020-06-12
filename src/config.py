# IMPORTS

import os

# Functions


def print_rules():
    """
    Prints the rules of the game
    :return:    None
    """
    print(RULES)


def asset_path(file):
    """
    Joins the asset pat and file
    :param file: The file name
    :return: The path to ASSETS_PATH\\file
    """
    return os.path.join(ASSETS_PATH, file)

# CONSTANTS

# MISC CONSTANTS

RULES = '''### Welcome to CONNECT FOUR! ###
Objective - Connect 4 of your checkers with a horizontal, vertical or diagonal line.
If more than one game is played, the winner goes first.
HAVE FUN!
'''     # The rules of the game

ASSETS_PATH = os.path.join('..', 'assets')  # Relative Path of ConnectPy/assets from ConnectPy/src


# CONFIGURATION CONSTANTS

EMPTY = ' '     # Empty tile type
BOARD_DIM = (COLUMNS, ROWS) = (7, 6)  # Number of columns and rows in the board
TILE_NUM = ROWS * COLUMNS   # Number of tiles in the board
PLAYER_NUM = 2  # Number of players
WIN_LEN = 4     # Number of tiles in a row needed to win

# CONSTANTS FOR has_won FUNCTION

# Positive X - Up, Positive yellow - Right
DOWN = (-1, 0)   # Multipliers used to traverse down
RIGHT = (0, 1)  # Multipliers used to traverse right
PRIMARY = (-1, 1)   # Multipliers used to traverse through the primary diagonal
SECONDARY = (1, 1)    # Multipliers used to traverse the secondary diagonal
MULTS = [DOWN, RIGHT, PRIMARY, SECONDARY]   # Tuple of traversal multipliers


# RGB COLOR CONSTANTS

RED = (255, 68, 68)     # Red color
YELLOW = (255, 255, 68) # Yellow color
ORANGE = (255, 165, 68) # Orange color
BLUE = (68, 68, 255)    # Blue color
GRAY = (136, 136, 136)  # Gray color
WHITE = (255, 255, 255) # White color
BLACK = (0, 0, 0)       # Black color
COLORS = {'blue': BLUE,
          'gray': GRAY,
          'white': WHITE,
          'black': BLACK}     # Checker colors for graphic game


# GRAPHIC CONSTANTS

FPS = 60                # Maximum game refresh rate

BG_COLOR = GRAY         # Color of the background
TEXT_COLOR = BLACK      # Color of the text
TITLE = 'Connect4Py'    # Window tile
WIDTH = COLUMNS         # The width of the board
HEIGHT = ROWS           # The height of the board


# Assert statements


assert WIN_LEN == 4  # Makes sure the win length is 4
assert PLAYER_NUM == 2  # Makes sure there are only 2 players
assert COLUMNS >= WIN_LEN and ROWS >= WIN_LEN  # Makes sure the board is large enough to win


# Main


if __name__ == '__main__':
    pass
