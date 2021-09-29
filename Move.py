from dataclasses import dataclass

from Squares import Square
from Location import Location
from constants import Color


@dataclass
class Move:

    fromSq: Location = None
    toSq: Location = None


class MoveHandler:

    def __init__(self, board, load_position):
        self.board = board
        self.turn = Color.LIGHT if load_position.whiteToMove else Color.DARK
        self.lKing = [x for x in self.board.lightPieces if x.name == "King"][0]
        self.DKing = [x for x in self.board.darkPieces if x.name == "King"][0]
        self._pin_moves = []
        self.lights_moves = []
        self.darks_moves = []

    def move(self, move):
        """
        Performs a given move.
        """
        if not isinstance(move, Move):
            raise ValueError("Move must be of type, Move")

        board = self.board
        fromSq = move.fromSq
        toSq = move.toSq

    def generate_moves(self):
        board = self.board
        self.darks_moves = []
        self.lights_moves = []
        for piece in self.board.darkPieces:
            if piece.name.lower() == "king":
                self.darks_moves.extend(piece.getValidMoves(board))

        for piece in self.board.lightPieces:
            if piece.name.lower() == "king":
                self.lights_moves.extend(piece.getValidMoves(board))

        return True

    def moves(self, turn=False):
        pass

    def highlight_attacked(self, turn=False):
        board = self.board
        board.reset_squares()

        if not turn:
            print("Showing attacked moves for both sides")
            side = self.lights_moves + self.darks_moves
        else:
            print(f'Showing attacked moves for {self.turn}')
            side = self.lights_moves if self.turn == Color.LIGHT else self.darks_moves

        for loc in side:
            square = board.map.get(loc)
            square.isAttacked = True
