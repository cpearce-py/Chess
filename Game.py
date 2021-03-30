import sys

import pygame

from Board import Board
from Files import Color, Files
from Location import Location
from Pieces import Bishop, King, Knight, Pawn, Queen, Rook


class Game():

    def __init__(self):
        self._board = Board()

    def play(self):
        _running = True
        while _running:
            self.board.printBoard()
            print("")
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

            try:
                possibleMoves = piece.getValidMoves(self.board)
                piece.moveTo(toSq, possibleMoves)
            except ValueError:
                print(f"{piece.name} cannot move to that square. ")

    @property
    def board(self):
        return self._board

    @staticmethod
    def printPieces(*piece):
        print(*piece)


game = Game()
game.play()
