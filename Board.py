from Squares import Square
from Location import Location
import numpy as np
from Files import Files, RANKS, Color


class Board():

    def __init__(self):
        self._createBoard()

    def _createBoard(self):
        _BOARD = []
        _map = {}
        for x, rank in enumerate(RANKS):
            _strip = []
            colour = Color.DARK if not x % 2 == 0 else Color.LIGHT
            for i, file in enumerate(Files):

                pos = Location(file, rank)
                _square = Square(colour, pos)

                _strip.append(_square)
                _map[pos] = _square

                colour = Color.LIGHT if colour == Color.DARK else Color.DARK

            _BOARD.append(_strip)
        self._BOARD = _BOARD
        self._map = _map

    def __repr__(self):
        return str(np.array(self._BOARD))

    def rank(self, row):
        i = len(self._BOARD) - row
        return self._BOARD[i]

    def file(self, col):
        file = []
        for row in self._BOARD:
            file.append(row[col])
        return file

    def printBoard(self):
        return

    @property
    def map(self):
        return self._map

    @property
    def board(self):
        return self._BOARD
