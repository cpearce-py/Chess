from Squares import Square
from Location import Location
from Files import Color
import logic


class AbstractPiece:

    def __init__(self, name, pieceColor):
        self._name = name
        self._pieceColor = pieceColor
        self._square = None
        self._isFirstMove = True

    def __repr__(self):
        return (f'{self.__class__.__name__}({self._name}, {self._pieceColor},'
                f' {self._square})')

    @property
    def isFirstMove(self):
        return self._isFirstMove

    @isFirstMove.setter
    def isFirstMove(self, value):
        self._isFirstMove = value

    @property
    def name(self):
        return self._name

    @property
    def color(self):
        return self._pieceColor

    @property
    def square(self):
        """ Property for what Square the piece is on.
        Returns: Location(Enum.File, Rank)"""
        return self._square

    @square.setter
    def square(self, value):
        if not isinstance(value, Location):
            raise ValueError("Pass Square location as a Location class}")
        self._square = value
