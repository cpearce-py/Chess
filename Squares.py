from Location import Location


class Square:

    Color = ['DARK', 'LIGHT']

    def __init__(self, SquareColor, pos):
        if not isinstance(pos, Location):
            raise ValueError("please pass pos, as class Location")
        self._SquareColor = SquareColor
        self._Location = pos
        self._isOccupied = False

    def reset(self):
        self._isOccupied = False

    @property
    def pos(self):
        return f'{self._Location.file}{self._Location.rank}'

    @property
    def color(self):
        return self._SquareColor

    def __repr__(self):
        return f'{self.__class__.__name__}(COLOR={self._SquareColor}, {self._Location}), {self._isOccupied}'
