from collections import namedtuple
from dataclasses import dataclass, field

import pygame
from AbstractPiece import AbstractPiece
from Squares import Square

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

    def __init__(self) -> None:
        self._commands = {}
        self._history = []
        self._history_position = 0

    def undo(self):
        if not self._history_position > 0:
            print("Nothing to undo")
            return
        self._history_position += 1
        self._commands[
            self._history[self._history_position][1]
        ].undo(self._history[self._history_position][2])
