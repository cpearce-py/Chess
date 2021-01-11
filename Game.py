from Board import Board
from Pieces import Pawn, Queen


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
pawn = Pawn("DARK")
q = Queen("LIGHT")
game.printPieces(pawn, q)
