"""
Module constants.py
===================

This module contains all of the constant values used in the main program
"""
from __future__ import annotations

from datetime import date
from pathlib import Path
from typing import Dict, List, Tuple

import pygame

__version__ = '0.1'
__author__ = 'Eric G.D'

# Types


GameState = List[List[str]]
Resolution = Tuple[int, int]
ResDict = Dict[str, Resolution]
ImageDict = Dict[str, Dict[str, pygame.Surface]]
Position = Tuple[int, int]
Color = Tuple[int, int, int]

# Game Logic Constants


ROWS: int = 6
COLS: int = 7
BOARD_DIMENSIONS: Tuple[int, int] = (ROWS, COLS)
NUM_OF_CELLS: int = ROWS * COLS
NUM_OF_PLAYERS: int = 2
WIN_LENGTH: int = 4
MAX_SCORE: int = 10 ** 5
LOG_MESSAGE: str = '{0} {1:^22} {0}'


# Graphic Constants


class Colors:
    red: Color = (255, 68, 68)
    yellow: Color = (255, 255, 68)
    orange: Color = (255, 165, 68)
    blue: Color = (68, 68, 255)
    gray: Color = (127, 127, 127)
    white: Color = (255, 255, 255)
    black: Color = (0, 0, 0)
    background: Color = gray
    text: Color = black


FPS: int = 60
title: str = 'Connect4Py'
ASSETS_PATH: Path = Path('assets')
icon_res: Resolution = (32, 32)
icon_path: Path = ASSETS_PATH / 'icon.png'
log_path: Path = Path('logs', f'connect4py_log_{date.today()}.txt')
if not log_path.parent.is_dir():
    log_path.parent.mkdir()

# Assertions


assert ROWS >= WIN_LENGTH and COLS >= WIN_LENGTH, 'Board has to be at least {0}x{0}'.format(WIN_LENGTH)
