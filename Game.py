from Board import Board
from Pieces import Pawn, Queen, King, Knight, Rook, Bishop
from Location import Location
from Files import Files, Color


class Game():

    def __init__(self):
        self._board = Board()

    @property
    def board(self):
        return self._board

    @staticmethod
    def printPieces(*piece):
        print(*piece)


game = Game()
p = Pawn(Color.LIGHT)
p.square = Location(Files.A, 2)
print(game.board)
