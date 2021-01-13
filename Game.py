import sys
from Board import Board
from Pieces import Pawn, Queen, King, Knight, Rook, Bishop
from Location import Location
from Files import Files, Color


class Game():

    def __init__(self):
        self._board = Board()

    def play(self):

        while True:
            self.board.printBoard()

            start = input("Move square: ")
            file = start[0].upper()
            rank = int(start[1])
            start = Location(Files[file], rank)

            to = input("To Square: ")
            file = to[0].upper()
            rank = int(to[1])
            end = Location(Files[file], rank)

            fromSq = self.board.map.get(start)
            toSq = self.board.map.get(end)
            piece = fromSq.currentPiece

            piece.moveTo(toSq)

            # fromSq.currentPiece.square = toSq
            # toSq.currentPiece = piece

            # fromSq.reset()

    @property
    def board(self):
        return self._board

    @staticmethod
    def printPieces(*piece):
        print(*piece)


game = Game()
game.play()
