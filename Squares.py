from Location import Location


class Square:

    Color = ['DARK', 'LIGHT']

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
    def color(self):
        return self._SquareColor

    def __repr__(self):
        return (f'{self.__class__.__name__}(COLOR={self._SquareColor.name},'
                f'{self._Location}), {self._isOccupied})')
