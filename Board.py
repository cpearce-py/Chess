from Squares import Square
from Location import Location
import numpy as np

RANKS = ["1", "2", "3", "4", "5", "6", "7", "8"]
FILES = ["a", "b", "c", "d", "e", "f", "g", "h"]


class Board():

    def __init__(self):
        self._BOARD = []
        colour = "dark"
        for i, rank in enumerate(RANKS):
            _strip = []
            for file in FILES:
                if i % 2:
                    colour = "light"
                pos = Location(file, rank)
                _square = Square(colour, pos)
                _strip.append(_square)
            self._BOARD.append(_strip)

    def __repr__(self):
        return self._BOARD

    def row(self, row):
        return self._BOARD[row]

    def coloum(self, col):
        pass

    @property
    def board(self):
        return np.array(self._BOARD)


b = Board()
print(b.row(2))
