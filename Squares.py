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

   # def __array__(self):
   #     return np.array([self._Location.file, self._Location.rank])

    @property
    def SquareColor(self):
        return self._SquareColor

    @property
    def Location(self):
        return self._Location

    def __repr__(self):
        return f'{self.__class__.__name__}({self._SquareColor}, {self._Location}, {self._isOccupied})'
