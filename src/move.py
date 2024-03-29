"""
Base move module
"""

from __future__ import annotations
import logging
from dataclasses import dataclass
from enum import Enum, auto
from typing import (
    TYPE_CHECKING,
    Optional,
    cast,
)

import logic
import constants as c
from squares import Square
from abstract_piece import AbstractPiece

if TYPE_CHECKING:
    from Pieces import Rook

__all__ = ("Move", "MoveHandler", "Flag", "EnpassantMove", "CastleMove")

logger = logging.getLogger(__file__)
f_handler = logging.FileHandler("chess.log")
logger.addHandler(f_handler)


class Flag(Enum):
    """Different move types"""

    MOVE = auto()
    CAPTURE = auto()
    ENPASSANT = auto()
    CASTLE = auto()
    PROMOTE = auto()
    CHECK = auto()
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
    _captured_piece: Optional[AbstractPiece] = None

    @property
    def captured_piece(self) -> Optional[AbstractPiece]:
        """Captured piece"""
        return self._captured_piece

    @captured_piece.setter
    def captured_piece(self, piece) -> None:
        self._captured_piece = piece
        self._captured_piece_attrs = _clean(**piece.__dict__.copy())


class Move:
    def __init__(self, from_sq: Square, to_sq: Square, flag: Flag = Flag.MOVE):
        self.from_sq = from_sq
        self.to_sq = to_sq
        self.flag = flag
        _moved_piece = cast(AbstractPiece, from_sq.piece)
        self.pieces = MovePieceHolder(_moved_piece)
        self.piece_attrs = _clean(**_moved_piece.__dict__.copy())
        self.turn = _moved_piece.color
        if self.to_sq.piece:
            _captured_piece = self.to_sq.piece
            self.pieces.captured_piece = _captured_piece

    def __hash__(self):
        return hash((self.from_sq, self.to_sq))

    def __eq__(self, other):
        return (
            self.to_sq.location == other.to_sq.location
            and self.from_sq.location == other.from_sq.location
        )

    def perform(self, board):
        logger.info("Performing move")
        self.pieces.moved_piece.moveToSquare(self.to_sq, board)

    @property
    def squares(self):
        """Return squares involved in move"""
        return (self.from_sq, self.to_sq)

    @property
    def moved_piece(self):
        """Moved piece"""
        return self.pieces.moved_piece

    @property
    def captured_piece(self):
        """Captured piece"""
        return self.pieces.captured_piece

    def __repr__(self):
        attrs = (
            ("from", self.from_sq.location),
            ("to", self.to_sq.location),
            ("piece", self.pieces.moved_piece.name),
        )
        inners = ", ".join("%s=%r" % t for t in attrs)
        return f"<{self.__class__.__name__} {inners}>"


class CastleMove(Move):
    """Castling move"""

    def __init__(self, from_sq: Square, to_sq, rook_sq: Square, rook: Rook) -> None:
        super().__init__(from_sq, to_sq, Flag.CASTLE)
        self.from_sq = from_sq
        self.to_sq = to_sq
        self.rook_sq = rook_sq
        self.rook = rook

    def perform(self, board):
        """Plays the instance of `Move` on the given board"""
        super().perform(board)
        rook = self.rook
        rook.moveToSquare(self.rook_sq)


class EnpassantMove(Move):
    def __init__(self, from_sq: Square, to_sq: Square, enpassanted_square: Square):
        super().__init__(from_sq, to_sq, Flag.ENPASSANT)
        self.enpassented_square = enpassanted_square

    def perform(self, board):
        super().perform(board)
        self.enpassented_square.piece.kill()
        self.enpassented_square.clear()


class PromoteMove(Move):
    def __init__(self, from_sq: Square, to_sq: Square):
        super().__init__(from_sq, to_sq, Flag.PROMOTE)

    def perform(self, board):
        super().perform(board)


class MoveHandler:
    def __init__(self, board, white_to_move=True):
        self.board = board
        self.turn = c.Color.LIGHT if white_to_move else c.Color.DARK
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

        piece_captured = move.captured_piece
        if piece_captured:
            piece_captured.set_attrs_from_dict(**move.pieces.captured_piece_attrs)

        self.board.set_piece(piece_moved, move.from_sq)
        self.board.set_piece(piece_captured, move.to_sq)

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
            side = self.lights_moves if self.turn == c.Color.LIGHT else self.darks_moves

        for loc in side:
            if square := board.map.get(loc):
                square.isAttacked = True

    def endTurn(self):
        self.board.deselect()
        self.generate_moves()
        # self.highlight_attacked()

    def reset(self):
        self.board.deselect()
