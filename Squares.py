from Location import Location
from Files import Files, Color, RANKS
import pygame
from Files import WIDTH, HEIGHT, DIMENSIONS, SQ_SIZE


class Square(pygame.sprite.Sprite):

    def __init__(self, SquareColor, pos, rect):
        pygame.sprite.Sprite.__init__(self)
        if not isinstance(pos, Location):
            raise ValueError("please pass pos, as class Location")
        self._SquareColor = SquareColor
        self._Location = pos
        self._isOccupied = False
        self._piece = None

        self.image = pygame.Surface([WIDTH, HEIGHT])
        color = (232, 235, 239) if SquareColor == Color.LIGHT else (
            125, 135, 150)
        self.image.fill(color)
        self.rect = rect

        self._selected = False

    def __eq__(self, other):
        return (isinstance(other, Square) and
                other._SquareColor == self._SquareColor and
                other._Location == self._Location
                )

    def __hash__(self):
        return hash((self._SquareColor, self._Location))

    def reset(self):
        self._piece = None
        self._isOccupied = False

    def update(self):
        if self._selected:
            self.image.fill((255, 255, 0))
        self.image

    @property
    def isOccupied(self):
        return self._isOccupied

    @property
    def currentPiece(self):
        return self._piece

    @currentPiece.setter
    def currentPiece(self, value):
        self._piece = value
        self._isOccupied = True

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
        self._selected = True

    def deselect(self):
        self._selected = False

    def __repr__(self):
        return (f'{self.__class__.__name__}(COLOR={self._SquareColor.name},'
                f'{self._Location}), {self._isOccupied})')
