from Location import Location
from Files import Files, Color, RANKS


class Square:

    def __init__(self, SquareColor, pos):
        if not isinstance(pos, Location):
            raise ValueError("please pass pos, as class Location")
        self._SquareColor = SquareColor
        self._Location = pos
        self._isOccupied = False
        self._piece = None

    def reset(self):
        self._piece = None
        self._isOccupied = False

    def __eq__(self, other):
        return (isinstance(other, Square) and
                other._SquareColor == self._SquareColor and
                other._Location == self._Location
                )

    def __hash__(self):
        return hash((self._SquareColor, self._Location))

    @property
    def isOccupied(self):
        return self._isOccupied

    @property
    def currentPiece(self):
        return self._piece

    @currentPiece.setter
    def currentPiece(self, value):
        self._piece = value
        self._isOccupied = True

    @property
    def location(self):
        return self._Location

    @property
    def file(self):
        return self._Location.file

    @property
    def rank(self):
        return self._Location.rank

    @property
    def color(self):
        return self._SquareColor

    def __repr__(self):
        return (f'{self.__class__.__name__}(COLOR={self._SquareColor.name},'
                f'{self._Location}), {self._isOccupied})')
