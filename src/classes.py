# Imports

from config import *


class Player:
    """
    Player class
    Contains:
    * The players number,
    * If the player is human or a computer
    * The color of the player's checkers
    """

    COLOR = ('red', 'yellow')

    def __init__(self, player_num, is_human, color=None):
        """
        Initialises a new player object
        :param player_num:  The players number
        :param is_human:    If the player is human or not
        :param color:       The color of the player's checkers
        """
        if not 1 <= player_num <= PLAYER_NUM:
            raise ValueError('Invalid player number entered')
        if not isinstance(is_human, (bool, int)):
            raise TypeError('Invalid type entered for is_human.')
        if not color:
            color = self.COLOR[player_num - 1]
        self._color = color
        self._player_num = player_num
        self._is_human = is_human

    @property
    def color(self):
        """
        :return:    The color of the player's checkers
        """
        return self._color

    @property
    def player_num(self):
        """
        :return:    The player's number
        """
        return self._player_num

    @property
    def is_human(self):
        """
        :return: If the player is human or not
        """
        return self._is_human

    def __str__(self):
        """
        :return:    The object as a string
        """
        return str(self._color).title() + " Player"
