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

r = Rook(Color.DARK)
r.square = Location(Files.H, 1)
print(r.getValidMoves(game.board))
