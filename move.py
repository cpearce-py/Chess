"""
Base move module
"""

from dataclasses import dataclass, field
from enum import Enum, auto

import logic
from constants import Color
from squares import Square
from AbstractPiece import AbstractPiece

__all__ = ("Move", "MoveHandler", "Flag")


class Flag(Enum):
    """Different move types"""

    MOVE = auto()
    CAPTURE = auto()
    ENPASSANT = auto()
    CASTLE = auto()
    PROMOTE = auto()
    CHECKMATE = auto()


def _clean(**attrs):
    """private method to reset certain attributes of a piece. Used for Un/Re do."""
    try:
        attrs["_selected"] = False
        attrs["_alive"] = True
    except TypeError as error:
        print(f"Can't unpack due to: {error}")
    return attrs


@dataclass
class MovePieceHolder:
    """
    Storage class for containing what pieces were involved in a move
    Internal to just this module.
    """

    moved_piece: AbstractPiece
    _captured_piece: AbstractPiece = None

    @property
    def captured_piece(self) -> AbstractPiece:
        """Captured piece"""
        return self._captured_piece

    @captured_piece.setter
    def captured_piece(self, piece) -> None:
        self._captured_piece = piece
        self._captured_piece_attrs = _clean(**piece.__dict__.copy())


@dataclass
class Move:
    """Base move class"""

    fromSq: Square
    toSq: Square
    pieces: MovePieceHolder = None
    piece_moved: AbstractPiece = None
    piece_captured: AbstractPiece = None
    piece_attrs: dict = field(init=False)
    captured_piece_attrs: dict = field(init=False)
    flag: Enum = Flag.MOVE

    def __post_init__(self):
        moved_piece = self.fromSq.piece
        self.pieces = MovePieceHolder(moved_piece)
        self.piece_attrs = _clean(**self.fromSq.piece.__dict__.copy())
        self.turn = moved_piece.color
        if captured_piece := self.toSq.piece:
            self.flag = Flag.CAPTURE
            self.pieces.captured_piece = captured_piece

    def __hash__(self):
        return hash((self.fromSq, self.toSq, self.flag.name))

    @property
    def squares(self):
        """Return squares involved in move"""
        return (self.fromSq, self.toSq)

    def __repr__(self):
        attrs = (
            ("from", self.fromSq.location),
            ("to", self.toSq.location),
            ("flag", self.flag.name),
        )
        inners = ", ".join("%s=%r" % t for t in attrs)
        return f"<{self.__class__.__name__} {inners}>"


class MoveHandler:
    def __init__(self, board, whiteToMove=True):
        self.board = board
        self.turn = Color.LIGHT if whiteToMove else Color.DARK
        self.lKing = [x for x in self.board.light_pieces if x.name == "king"][0]
        self.DKing = [x for x in self.board.dark_pieces if x.name == "king"][0]
        self._pin_moves = []
        self.lights_moves = []
        self.darks_moves = []

        self._undo_stack = []
        self._redo_stack = []
        self._history_position = 0

    def try_move(self, move: Move):
        """
        Attempts to make a move. Returns True if move was successful, and False
        if not.
        """
        from_sq, to_sq = move.squares
        if not from_sq.piece:
            return False

        turn = self.turn
        board = self.board
        piece = from_sq.piece
        if piece.color != turn or to_sq.location not in piece.getValidMoves(board):
            self.reset()
            return False
        piece.moveToSquare(to_sq, board)
        self.turn = logic.switch_turn(turn)
        self.endTurn()
        self._undo_stack.append(move)
        self._history_position += 1
        return True

    def undo(self):
        """Undoes a move"""
        if self._history_position <= 0:
            print("Nothing to undo")
            return
        self._history_position -= 1
        move = self._undo_stack.pop()
        self._redo_stack.append(move)

        self.turn = move.turn
        piece_moved = move.pieces.moved_piece
        piece_moved.set_attrs_from_dict(**move.piece_attrs)

        piece_captured = move.piece_captured
        if piece_captured:
            piece_captured.set_attrs_from_dict(**move.captured_piece_attrs)

        self.board.set_piece(piece_moved, move.fromSq)
        self.board.set_piece(piece_captured, move.toSq)

    def redo(self):
        """Replays move if one is available."""
        try:
            move = self._redo_stack.pop()
            self.try_move(move)
        except IndexError:
            print("Nothing to redo")

    def generate_moves(self):
        """Generated possible moves at a given instance - will be removed"""
        board = self.board
        self.darks_moves = []
        self.lights_moves = []

        for piece in self.board.dark_pieces:
            self.darks_moves.extend(piece.getAttackMoves(board))

        for piece in self.board.light_pieces:
            self.lights_moves.extend(piece.getAttackMoves(board))

    def highlight_attacked(self, turn=True):

        board = self.board
        board.reset_squares()

        if not turn:
            side = self.lights_moves + self.darks_moves
        else:
            side = self.lights_moves if self.turn == Color.LIGHT else self.darks_moves

        for loc in side:
            if square := board.map.get(loc):
                square.isAttacked = True

    def endTurn(self):
        self.board.deselect()
        self.generate_moves()
        # self.highlight_attacked()

    def reset(self):
        self.board.deselect()
