from Squares import Square
from Location import Location
import numpy as np

RANKS = ["1", "2", "3", "4", "5", "6", "7", "8"]
FILES = ["a", "b", "c", "d", "e", "f", "g", "h"]
RANKS.reverse()


class Board():

    def __init__(self):
        self._BOARD = []
        for x, rank in enumerate(RANKS):
            _strip = []
            colour = "dark" if not x % 2 == 0 else "light"
            for i, file in enumerate(FILES):
                pos = Location(file, rank)
                _square = Square(colour, pos)
                _strip.append(_square)

                colour = "light" if colour == "dark" else "dark"
            self._BOARD.append(_strip)

    def __repr__(self):
        return str(np.array(self._BOARD))

    def row(self, row):
        return self._BOARD[row]

    def coloum(self, col):
        for row in self._BOARD:
            yield row[col]

    @staticmethod
    def printBoard(self):
        pass

    @property
    def board(self):
        return np.array(self._BOARD)
