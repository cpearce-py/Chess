from abc import ABC, abstractmethod

import pygame
from pygame.locals import *

import logic



class AbstractPiece(ABC, pygame.sprite.Sprite):
    """
    Base Piece class.

    :param name: `String` used to store name of subclassed pieces.
    :param pieceColor: `Color` Enum. (Color.LIGHT/Color.DARK).
    """

    def __init__(self, name, pieceColor, image, square=None, *groups):
        super(AbstractPiece, self).__init__()
        self._name = name.lower()
        self._pieceColor = pieceColor
        try:
            self.image = image.convert_alpha()
        except pygame.error:
            self.image = image

        self.rect = self.image.get_rect(center=[100, 100])
        self._square = None
        self._isFirstMove = True
        self._selected = False
        self._layer = 0
        self._alive = True

        if groups:
            self.add(groups, layer=self._layer)

    def __repr__(self):
        return (f'{self.__class__.__name__}({self._pieceColor},'
                f' {self._square.location})')

    @property
    def alive(self):
        return self._alive

    @alive.setter
    def alive(self, value):
        self._alive = value

    @property
    def layer(self):
        return self._layer

    @layer.setter
    def layer(self, value):
        self._layer = value

    @property
    def isFirstMove(self):
        return self._isFirstMove

    @isFirstMove.setter
    def isFirstMove(self, value):
        self._isFirstMove = value

    @property
    def selected(self):
        return self._selected

    @selected.setter
    def selected(self, value):
        if not isinstance(value, bool):
            raise ValueError(f"{self} selected attribute must be of type Bool")
        layer_group = [group for group in self.groups()
                        if isinstance(group, pygame.sprite.LayeredUpdates)][0]
        layer = 1 if value else 0
        layer_group.change_layer(self, layer)
        self._selected = value

    @property
    def name(self):
        return self._name

    @property
    def color(self):
        return self._pieceColor

    @property
    def location(self):
        """Property returns `Location` object for current square."""
        return self._square.location

    @property
    def square(self):
        """ Property for what Square the piece is on.
        Returns: :class:`Square`."""
        return self._square

    @square.setter
    def square(self, square):
        self._square = square
        if not square.piece == self:
            square.piece = self
        self.rect.center = square.rect.center

    def set_attrs_from_dict(self, **attrs):
        for key, value in attrs.items():
            if key == "_Sprite__g":
                pass
            setattr(self, key, value)

    def forceMove(self, square):
        """
        This method shouldn't be overwritten! 
        It deals with cleanup and the basic process of moving a piece to a 
        square. Any checks should be done prior.

        :param square: Instance of :class:`Square` square to move to.
        """
        if (piece := square.piece):
            piece.alive = False
            piece.kill()
        self.square.reset()
        square.piece = self
        self.square = square
        self.isFirstMove = False
        self.rect.center = square.rect.center

    def moveToSquare(self, square, board=None):
        """
        Method is aimed at being overwritten when certain requirements
        are needed. Ie. pawn promotion. """
        self.forceMove(square)

    @abstractmethod
    def getValidMoves(self, board):
        """ Method to get available moves. MUST be used in each subclass."""
        raise NotImplementedError

    def _getDiagonalCandidates(self, moves, boardMap,
                               current, rankOffset=0, fileOffset=0):
        """
        Method to append possible diagonal moves.
        Offset determines forward or backwards direction (1 or -1)

        :param moves: type `list` moves appended to this object.
        :param boardMap: type `dict`
        :param current: type `Location` Current Pieces square.
        :param rankOffset: type `Int` + or - 1 for direction.
        :param fileOffset: type `Int` + or - 1 for direction.

        """
        nextMove = logic.build(current, fileOffset, rankOffset)
        while boardMap.get(nextMove):
            if boardMap.get(nextMove).isOccupied:
                if boardMap.get(nextMove).piece.color == self.color:
                    break
                moves.append(nextMove)
                break
            moves.append(nextMove)
            nextMove = logic.build(nextMove, fileOffset, rankOffset)

    def _getFileCandidates(self, moves, boardMap, current, offset):
        """
        Method to append a position, type:`Location`, to given list.
        Offset determines forward or backwards direction from piece.

        :param moves: type `list` moves appended to this object.
        :param boardMap: type `dict`
        :param current: type `Location` Current Pieces square.
        :param offset: type `Int` + or - 1 for direction.
        """
        nextMove = logic.build(current, offset, rankOffset=0)
        while boardMap.get(nextMove):
            if boardMap.get(nextMove).isOccupied:
                if boardMap.get(nextMove).piece.color == self.color:
                    break
                moves.append(nextMove)
                break
            moves.append(nextMove)
            nextMove = logic.build(nextMove, offset, rankOffset=0)

    def _getRankCandidates(self, moves, boardMap, current, offset):
        """
        Method to append a position, type:`Location`, to given list.
        Offset determines forward or backwards direction from piece.

        :param moves: type `list` moves appended to this object.
        :param boardMap: type `dict`
        :param current: type `Location` Current Pieces square.
        :param offset: type `Int` + or - 1 for direction.
        """
        nextMove = logic.build(current, 0, offset)
        while boardMap.get(nextMove):
            if boardMap.get(nextMove).isOccupied:
                if boardMap.get(nextMove).piece.color == self.color:
                    break
                moves.append(nextMove)
                break
            moves.append(nextMove)
            nextMove = logic.build(nextMove, 0, offset)

    def _getKnightsMove(self, moves, boardMap, current):
        """
        Method to append a position, type:`Location`, to given list. Based on
        a knights movement.

        :param moves: type `list` moves appended to this object.
        :param boardMap: type `dict` Board.Map
        :param current: type `Location` Current Pieces square.
        """
        choices = [2, -2, 1, -1]
        for i in choices:
            for j in choices:
                if abs(j) == abs(i):
                    continue

                nextMove = logic.build(current, i, j)
                try:
                    square = boardMap.get(nextMove)
                    if square.isOccupied and square.piece.color == self.color:
                        raise ValueError("Same piece color")
                    moves.append(nextMove)
                except:
                    continue

    def update(self):
        self.rect.center = pygame.mouse.get_pos() if self._selected else self.square.rect.center
        self.updateAlive()

    def draw(self, surface):
        surface.blit(self.image, self.rect)

    def updateAlive(self):
        if self.alive == False:
            print(f'{self.name} is dead')
            self.kill()
