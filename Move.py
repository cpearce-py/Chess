from dataclasses import dataclass
import types
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
        self.lKing = [x for x in self.board.lightPieces if x.name == "king"][0]
        self.DKing = [x for x in self.board.darkPieces if x.name == "king"][0]
        self._pin_moves = []
        self.lights_moves = []
        self.darks_moves = []

    def move(self, move):

        if not isinstance(move, Move):
            raise ValueError("Move must be of type, Move")

        board = self.board
        fromSq = move.fromSq
        toSq = move.toSq

    def generate_moves(self, piece=None):
        board = self.board
        self.darks_moves = []
        self.lights_moves = []

        for piece in self.board.darkPieces:
            piece_moves = piece.getAttackMoves(board)
            if isinstance(piece_moves, types.GeneratorType):
                for move in piece_moves:
                    self.darks_moves.append(move)
            else:
                self.darks_moves.extend(piece.getAttackMoves(board))

        for piece in self.board.lightPieces:
            piece_moves = piece.getAttackMoves(board)
            if isinstance(piece_moves, types.GeneratorType):
                for move in piece_moves:
                    self.lights_moves.append(move)
            else:
                self.lights_moves.extend(piece.getAttackMoves(board))

    def highlight_attacked(self, turn=True):

        board = self.board
        board.reset_squares()

        if not turn:
            side = self.lights_moves + self.darks_moves
        else:
            side = self.lights_moves if self.turn == Color.LIGHT else self.darks_moves

        for loc in side:
            if (square := board.map.get(loc)):
                square.isAttacked = True
