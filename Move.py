import types
from dataclasses import dataclass, field

from constants import Color
from Squares import Square


@dataclass
class Move:

    fromSq: Square
    toSq: Square
    capture: bool = field(init=False)

    def __post_init__(self):
        self.capture = self.toSq.isOccupied

    def __hash__(self):
        return hash((self.fromSq, self.toSq, self.capture) )

    @property
    def squares(self):
        return (self.fromSq, self.toSq)


class MoveHandler:

    def __init__(self, board, whiteToMove=True):
        self.board = board
        self.turn = Color.LIGHT if whiteToMove else Color.DARK
        self.lKing = [x for x in self.board.lightPieces if x.name == "king"][0]
        self.DKing = [x for x in self.board.darkPieces if x.name == "king"][0]
        self._pin_moves = []
        self.lights_moves = []
        self.darks_moves = []
        self._undo_stack = []
        self._redo_stack = []

    def try_move(self, move):

        fromSq, toSq = move.squares
        turn = self.turn
        board = self.board

        if piece := fromSq.currentPiece:
            if piece.color != turn or toSq.location not in piece.getValidMoves(board):
                self.reset()
                return 
            piece.moveToSquare(toSq, board)
            self.turn = Color.DARK if self.turn == Color.LIGHT else Color.LIGHT
            self.endTurn()
            self._undo_stack.append(move)
    
    def undo_move(self, move):
        pass

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

    def endTurn(self):
        self.board.deselect()
        self.generate_moves()
        self.highlight_attacked()

    def reset(self):
        self.board.deselect()

def main():
    print("testing")

if __name__ == '__main__':
    main()