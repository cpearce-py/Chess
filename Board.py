from Squares import Square
from Location import Location
from Files import Files, RANKS, Color


class Board():

    def __init__(self):
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
        return f'{self.__class__.__name__}'

    def rank(self, row):
        i = len(self._BOARD) - row
        return self._BOARD[i]

    def file(self, col):
        file = []
        for row in self._BOARD:
            file.append(row[col])
        return file

    def printBoard(self):
        for i in range(len(self._BOARD)):
            line = " "
            line += f'{len(self._BOARD) - i} '
            for j in range(len(self._BOARD[i])):
                if self._BOARD[i][j].isOccupied:
                    piece = self._BOARD[i][j].currentPiece
                    line += f'{piece.name[0]} '
                else:
                    # Empty Square
                    line += f'- '
            print(line)
        line = "   "
        for file in Files:
            line += f'{file.name} '
        print(line)

    @property
    def map(self):
        return self._map

    @property
    def board(self):
        return self._BOARD
