import pygame

from constants import HEIGHT, WIDTH, Color
from location import Location


class Square(pygame.sprite.Sprite):
    def __init__(self, SquareColor, pos, rect):
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

    def __eq__(self, other):
        return (
            isinstance(other, Square)
            and other._SquareColor == self._SquareColor
            and other._Location == self._Location
        )

    def __hash__(self):
        return hash((self._SquareColor, self._Location))

    def reset(self):
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
    def isOccupied(self):
        return self._isOccupied

    @property
    def piece(self):
        return self._piece

    @piece.setter
    def piece(self, piece):
        self._piece = piece
        self._isOccupied = True if piece else False
        if piece and piece.square != self:
            piece.square = self

    @property
    def location(self):
        return self._Location

    @property
    def file(self):
        return self._Location.file

    @property
    def rank(self):
        return self._Location.rank

    @property
    def color(self):
        return self._SquareColor

    @property
    def isSelected(self):
        return self._selected

    @isSelected.setter
    def isSelected(self, value):
        self._selected = value

    def select(self):
        try:
            self.piece.selected = True
        except AttributeError:
            pass
        self._selected = True

    def deselect(self):
        try:
            self.piece.selected = False
        except AttributeError:
            pass
        self._selected = False

    def __repr__(self):
        return (
            f"{self.__class__.__name__}(COLOR={self._SquareColor.name},"
            f"{self._Location}), {self._isOccupied})"
        )
