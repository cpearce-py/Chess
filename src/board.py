from __future__ import annotations
from typing import (
    TYPE_CHECKING,
    Dict,
    Optional,
    Iterable,
)
import pygame

import logic
import constants as c
from location import Location
from squares import Square
from fen import PositionInfo, START_FEN, load_from_fen

if TYPE_CHECKING:
    from abstract_piece import AbstractPiece
    from squares import Square
    from move import Move

start_position = load_from_fen(START_FEN)


class Board(pygame.sprite.Group):
    """
    Representation of Chess Board. Manage piece movement and board display.
    board.map attribute is a dictionary pairing each instance of Location, to
    an instance of a square. This allows us to quickly access information on a
    square by it's given location.

    board.map = {Location(FIlE=A, RANK=1): Square(LOCATION(FILE=A, RANK=1))}

    Example:
        board.map.get(Location(A,1)).currentPiece

    Returns:
        Rook(Color=LIGHT, Location(A,1))

    Board currently tracks which colors turn it is. Not sure I'm fully commited
    to this setup but it's easier to manage as the board is shared between nearly
    all other components. ie. move_gen, move_handler, scene etc.
    """

    def __init__(self):
        super().__init__()

        self._render_pieces = pygame.sprite.LayeredUpdates()
        self._light_pieces = pygame.sprite.Group()
        self._dark_pieces = pygame.sprite.Group()
        self.board_squares = pygame.sprite.Group()
        self._map = {}
        self.all_pieces: Dict[c.Color, Iterable[AbstractPiece]] = {
            c.Color.DARK: self._dark_pieces,
            c.Color.LIGHT: self._light_pieces,
        }
        self.white_to_move = None
        self.color_to_move = None

    def init(self, load_position: PositionInfo = start_position):
        """Initalises board inline."""
        self.white_to_move = load_position.whiteToMove
        self.color_to_move = c.Color.LIGHT if self.white_to_move else c.Color.DARK

        pieces = load_position.squares
        _map = {}

        for x, file in enumerate(c.Files):
            colour = c.Color.DARK if x % 2 == 0 else c.Color.LIGHT
            for y, rank in enumerate(c.RANKS):
                rect = pygame.Rect(x * c.SQ_SIZE, y * c.SQ_SIZE, c.SQ_SIZE, c.SQ_SIZE)

                pos = Location(file, rank)
                square = Square(colour, pos, rect)

                # Add square to the drawable pieces.
                self.board_squares.add(square)

                pos.square = square

                if piece := pieces.get(pos):

                    square.piece = piece
                    piece.square = square

                    self._render_pieces.add(piece, layer=piece.layer)

                    if piece.color == c.Color.DARK:
                        self._dark_pieces.add(piece)
                    else:
                        self._light_pieces.add(piece)

                self.add(square)
                _map[pos] = square
                colour = c.Color.LIGHT if colour == c.Color.DARK else c.Color.DARK

        self._map = _map
        return self

    def __repr__(self) -> str:
        attrs = (
            ("Light Pieces", len(self.light_pieces)),
            ("Dark Pieces", len(self.dark_pieces)),
        )
        inners = ", ".join("%s=%r" % t for t in attrs)
        return f"<{self.__class__.__name__} {inners}>"

    def make_move(self, move: Move):
        move.perform(self)

    def get(self, location: Location) -> Square:
        """Return square from board at given location"""
        return self.map[location]

    def _get_piece(self, name, color) -> Iterable:
        pieces = self.all_pieces.get(color)
        if pieces:
            return list(filter(lambda x: x.name == name, pieces))

    def king(self, color) -> AbstractPiece:
        """Return King piece of given color"""
        return self._get_piece("king", color)[0]

    def queen(self, color):
        """Return List[Queen] piece of given color"""
        return self._get_piece("queen", color)

    def bishops(self, color):
        """Return List[Bishop] pieces of given color"""
        return self._get_piece("bishop", color)

    def rooks(self, color):
        """Return List[Rooks] pieces of given color"""
        return self._get_piece("rook", color)

    def knights(self, color) -> Iterable:
        """Return List[Knight] pieces of given color"""
        return self._get_piece("knight", color)

    def pawns(self, color):
        """Return List[Pawn] pieces of given color"""
        return self._get_piece("pawn", color)

    def pieces(self, color: c.Color) -> Iterable[AbstractPiece]:
        return self.all_pieces.get(color)

    def kill_piece(self, piece):
        piece.kill()

    def reset_squares(self):
        for square in self.board_squares:
            square.isAttacked = False

    def get_piece_from_loc(self, loc):
        return self.map.get(loc).currentPiece

    def getFile(self, square, direction):
        cur_file = c.Files(square.location.file.value)
        new_file = c.Files(cur_file.value + direction)
        new_loc = Location(new_file, square.location.rank)
        return self.map.get(new_loc)

    def getFileUp(self, square):
        return self.getFile(square, 1)

    def getFileDown(self, square):
        return self.getFile(square, -1)

    def draw(self, surface):
        """
        Draw method inherited from pygame.sprite.Group.
        Updates each square and redraws to given surface.

        :param surface: Type `pygame.Surface` surface to draw to
        """
        self.board_squares.draw(surface)
        self._render_pieces.draw(surface)

    def update(self):
        """
        Update method inherited from pygame.sprite.Group.
        Updates each sprite object on board. ie. Squares, pieces etc.
        """
        self._render_pieces.update()
        self.board_squares.update()

    @property
    def map(self) -> Dict[Location, Square]:
        return self._map

    @property
    def light_pieces(self):
        return self._light_pieces

    @property
    def dark_pieces(self):
        return self._dark_pieces

    def deselect(self):
        for sqr in self.sprites():
            sqr.deselect()

    def set_piece(self, piece, square: Square):
        square = self._map.get(square.location)
        square.piece = piece
        if piece:
            self.add_piece(piece)

    def add_piece(self, piece):
        if piece.color == c.Color.DARK:
            self.dark_pieces.add(piece)
        else:
            self.light_pieces.add(piece)
        self._render_pieces.add(piece, layer=0)

    def end_turn(self):
        self.deselect()
        self.reset_squares()
        self.color_to_move = logic.switch_turn(self.color_to_move)
