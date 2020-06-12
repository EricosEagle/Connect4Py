"""
Module player.py
================

This module contains the implementation of the Player class
"""
from typing import Any

from src.constants import NUM_OF_PLAYERS

__version__ = '0.1'
__author__ = 'Eric G.D'


class Player:
    """
    class Player:
    -------------

    This class represents a player, and contains:
    * The player's id
    * Player type (Human or Computer)
    * The color of the player's tokens
    """

    def __init__(self, id_: int, color: str, is_human: bool = True):
        if not 1 <= id_ <= NUM_OF_PLAYERS:
            raise ValueError(f'Player id ({id_}) has to be between 1 and {NUM_OF_PLAYERS}!')
        self.__id: int = id_
        self.__color: str = color
        self.__is_human: bool = is_human
        self.__score: int = 0

    @property
    def id(self) -> int:
        return self.__id

    @property
    def color(self) -> str:
        return self.__color

    @property
    def is_human(self) -> bool:
        return self.__is_human

    @property
    def score(self) -> int:
        return self.__score

    @score.setter
    def score(self, score: int) -> None:
        if score < self.__score and score != 0:
            raise ValueError('Score can only be increased or zeroed!')
        self.__score = score

    def __str__(self) -> str:
        return f'{self.__color.title()} Player'

    def __repr__(self) -> str:
        return f'Player({self.__id}, {self.__color}, {self.__is_human})'

    def __eq__(self, other: Any) -> bool:
        return isinstance(other, Player) and self.__id == other.__id
