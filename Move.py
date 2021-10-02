import types
from dataclasses import dataclass, field

import pygame

from constants import Color
from Squares import Square
from AbstractPiece import AbstractPiece

"""
A move encompasses a state change in a game of Chess. Therefore we can simply
store each move and if we want to undo; restore the board to the previous state 
(Move). Ie. the piece from Move.fromSq returns to fromSq etc.
"""

"""
Test the following.
for attribute in piece.attrs:
    self.__addattr__ = attribute

then we return all attributes as a dict. and pass that to the relevant objects.
Ie. pieces! 
"""
@dataclass
class Move:

    fromSq: Square
    toSq: Square
    capture: bool = None
    piece_moved: AbstractPiece = None
    piece_captured: AbstractPiece = None
    captured_groups: pygame.sprite.Group  = None
    turn: bool = field(init=False)
    piece_moved_first_move: bool = field(init=False)

    def __post_init__(self):
        self.piece_moved =  self.fromSq.piece
        self.piece_moved_first_move = self.piece_moved.isFirstMove
        self.turn = self.piece_moved.color
        self.capture = True if self.toSq.piece else False
        if captured_piece := self.toSq.piece:
            self.capture = True
            self.piece_captured = captured_piece
            self.captured_groups = captured_piece.groups()

    def __hash__(self):
        return hash((self.fromSq, self.toSq, self.capture) )

    @property
    def squares(self):
        return (self.fromSq, self.toSq)

    def __repr__(self):
        attrs = (
            ('from', self.fromSq.location), 
            ('to', self.toSq.location),
            ('capture', self.capture),
            ('piece', self.piece_moved),
            ('captured', self.piece_captured)
        )
        inners = ', '.join('%s=%r' % t for t in attrs)
        return f'<{self.__class__.__name__} {inners}>'

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
        
        self._history_position = 0

    def execute():
        pass
    
    def try_move(self, move):
        fromSq, toSq = move.squares
        turn = self.turn
        board = self.board

        if piece := fromSq.piece:
            if piece.color != turn or toSq.location not in piece.getValidMoves(board):
                self.reset()
                return 
            piece.moveToSquare(toSq, board)
            self.turn = Color.DARK if self.turn == Color.LIGHT else Color.LIGHT
            self.endTurn()
            self._undo_stack.append(move)
            self._history_position += 1

    def undo(self):
        if self._history_position > 0:
            self._history_position -= 1
            move = self._undo_stack.pop()
            self._redo_stack.append(move)
            self.turn = move.turn
            piece_moved = move.piece_moved

            self.board.set_piece(piece_moved, move.fromSq)

            piece_captured = move.piece_captured
            self.board.set_piece(piece_captured, move.toSq)

            if piece_captured:
                piece_captured.alive = True
                piece_captured.add(move.captured_groups)

        else:
            print("Nothing to undo")

    def redo(self):
        pass
    
    def generate_moves(self):
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