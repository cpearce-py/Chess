from __future__ import annotations

from enum import Enum
from typing import TYPE_CHECKING, Optional

import pygame

from constants import HEIGHT, WIDTH, Color
from location import Location

if TYPE_CHECKING:
    from abstract_piece import AbstractPiece


class Square(pygame.sprite.Sprite):
    def __init__(self, SquareColor: Color, pos: Location, rect: pygame.Rect):
        pygame.sprite.Sprite.__init__(self)

        assert isinstance(pos, Location)

        self._SquareColor = SquareColor
        self._Location = pos
        self._isOccupied = False
        self._piece = None
        self.isAttacked = False
        self.image = pygame.Surface([WIDTH, HEIGHT])
        self._attacked_color = (
            (252, 115, 120) if SquareColor == Color.LIGHT else (145, 62, 75)
        )
        self._orig_color = (
            (232, 235, 239) if SquareColor == Color.LIGHT else (125, 135, 150)
        )
        self.image.fill(self._orig_color)
        self.rect = rect

        self._selected = False

    def __eq__(self, other: Square):
        return (
            isinstance(other, Square)
            and other._SquareColor == self._SquareColor
            and other._Location == self._Location
        )

    def __hash__(self):
        return hash((self._SquareColor, self._Location))

    def clear(self) -> None:
        """Empty square and reset attributes, doesn't deal with killing pieces."""
        self._piece = None
        self._isOccupied = False
        self.isAttacked = False
        self._selected = False

    def update(self):
        self.updateColor()

    def updateColor(self):
        if self._selected:
            self.image.fill((255, 255, 0))
        elif self.isAttacked:
            self.image.fill(self._attacked_color)
        else:
            self.image.fill(self._orig_color)

    @property
    def isOccupied(self) -> bool:
        return self._isOccupied

    @property
    def piece(self) -> Optional[AbstractPiece]:
        return self._piece

    @piece.setter
    def piece(self, piece: AbstractPiece) -> None:
        self._piece = piece
        self._isOccupied = True if piece else False
        if piece and piece.square != self:
            piece.square = self

    @property
    def location(self) -> Location:
        return self._Location

    @property
    def file(self) -> Enum:
        return self._Location.file

    @property
    def rank(self) -> int:
        return self._Location.rank

    @property
    def color(self) -> Color:
        return self._SquareColor

    @property
    def isSelected(self) -> bool:
        return self._selected

    @isSelected.setter
    def isSelected(self, value: bool):
        self._selected = value

    def select(self) -> None:
        if self.piece:
            self.piece.selected = True
        self._selected = True

    def deselect(self) -> None:
        if self.piece:
            self.piece.selected = False
        self._selected = False

    def __repr__(self) -> str:
        return (
            f"{self.__class__.__name__}(COLOR={self._SquareColor.name},"
            f"{self._Location}), {self._isOccupied})"
        )
