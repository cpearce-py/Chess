from Squares import Square
from Location import Location
from Files import Files, RANKS, Color
import logic

from Pieces import *


class Board():

    def __init__(self):
        _BOARD = []
        _pieces = self._initialize()
        _map = {}

        for x, rank in enumerate(RANKS):
            _strip = []
            colour = Color.DARK if not x % 2 == 0 else Color.LIGHT
            for i, file in enumerate(Files):

                pos = Location(file, rank)
                _square = Square(colour, pos)
                if _pieces.get(pos):
                    piece = _pieces.get(pos)
                    _square.currentPiece = piece
                    piece.square = _square
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

    @staticmethod
    def _initialize():
        pieces = {}

        # Rooks
        pieces[Location(Files.A, 1)] = Rook(Color.LIGHT)
        pieces[Location(Files.H, 1)] = Rook(Color.LIGHT)
        pieces[Location(Files.A, 8)] = Rook(Color.DARK)
        pieces[Location(Files.H, 8)] = Rook(Color.DARK)

        # Knights
        pieces[Location(Files.B, 1)] = Knight(Color.LIGHT)
        pieces[Location(Files.G, 1)] = Knight(Color.LIGHT)
        pieces[Location(Files.B, 8)] = Knight(Color.DARK)
        pieces[Location(Files.G, 8)] = Knight(Color.DARK)

        # Bishops
        pieces[Location(Files.C, 1)] = Bishop(Color.LIGHT)
        pieces[Location(Files.F, 1)] = Bishop(Color.LIGHT)
        pieces[Location(Files.C, 8)] = Bishop(Color.DARK)
        pieces[Location(Files.F, 8)] = Bishop(Color.DARK)

        # Queens
        pieces[Location(Files.D, 1)] = Queen(Color.LIGHT)
        pieces[Location(Files.D, 8)] = Queen(Color.DARK)

        # Kings
        pieces[Location(Files.E, 1)] = King(Color.LIGHT)
        pieces[Location(Files.E, 8)] = King(Color.DARK)

        # Pawns
        for file in Files:
            pieces[Location(file, 2)] = Pawn(Color.LIGHT)
            pieces[Location(file, 7)] = Pawn(Color.DARK)

        return pieces
