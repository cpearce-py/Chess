from Board import Board
from Pieces import Pawn, Queen, King, Knight, Rook, Bishop
from Location import Location
from Files import Files


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
p = Pawn("light")
pos = Location(Files.F, 5)
p.square = pos
print(p.getValidMoves(game.board))
