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
r.square = Location(Files.C, 4)

b = Bishop(Color.DARK)
b.square = Location(Files.D, 3)
print(r.getValidMoves(game.board))
print(b.getValidMoves(game.board))

p = Pawn(Color.LIGHT)
p.square = Location(Files.D, 2)
p.isFirstMove = False
# print(p.getValidMoves(game.board))
