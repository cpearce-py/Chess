from dataclasses import dataclass

from Squares import Square
from Location import Location
from constants import Color


@dataclass
class Move:

    fromSq: Location = None
    targetSq: Location = None


class MoveHandler:

    def __init__(self, board):
        self.board = board
        self.lPieces = self.board.lightPieces
        self.dPieces = self.board.darkPieces
        self.lKing = [x for x in self.lPieces if x.name == "King"][0]
        self.DKing = [x for x in self.dPieces if x.name == "King"][0]
        self._pin_moves = []
        self.lights_moves = []
        self.darks_moves = []

    def move(self, move):

        if not isinstance(move, Move):
            raise ValueError("Move must be of type, Move")

    def generate_moves(self, turn):
        self.darks_moves = []
        self.lights_moves = []
        for piece in self.board.darkPieces:
            self.darks_moves.extend(piece.getValidMoves(self.board))

        for piece in self.board.lightPieces:
            self.lights_moves.extend(piece.getValidMoves(self.board))


        return True

def main():
    handler = MoveHandler(board)
    handler.generate_moves()

if __name__ == '__main__':
    main()
