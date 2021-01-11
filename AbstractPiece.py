from Squares import Square
from Location import Location


class AbstractPiece:

    def __init__(self, name, pieceColor):
        self._name = name
        self._pieceColor = pieceColor
        self._square = None

    def __repr__(self):
        return (f'{self.__class__.__name__}({self._name}, {self._pieceColor},'
                f' {self._square})')

    @property
    def name(self):
        return self._name

    @property
    def color(self):
        return self._pieceColor

    @property
    def square(self):
        return self._square

    @square.setter
    def square(self, value):
        if not isinstance(value, Square):
            raise ValueError("Pass Square location as a Location class}")
        self._square = value

    def getValidMoves(self, board, square):
        pass

    def move(self, square):
        pass
