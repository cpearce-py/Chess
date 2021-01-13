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
game.board.printBoard()

p1 = game.board.map.get(Location(Files.A, 2)).currentPiece
p = game.board.map.get(Location(Files.B, 7)).currentPiece
print(p1.getValidMoves(game.board))
