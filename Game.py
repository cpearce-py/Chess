from Board import Board
from Pieces import Pawn, Queen, King, Knight, Rook, Bishop


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
print(game.board.map)
