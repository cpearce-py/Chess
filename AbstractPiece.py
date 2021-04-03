import logic
from abc import abstractmethod, ABC
from Files import Color
from Location import Location
from Squares import Square
import pygame


class AbstractPiece(ABC, pygame.sprite.Sprite):
    """
    Base Piece class.

    :param name: `String` used to store name of subclassed pieces.
    :param pieceColor: `Color` Enum. (Color.LIGHT/Color.DARK).
    """

    def __init__(self, name, pieceColor, image):
        pygame.sprite.Sprite.__init__(self)
        self._name = name
        self._pieceColor = pieceColor

        self.image = image
        self.rect = self.image.get_rect(center=[100, 100])

        self._square = None
        self._isFirstMove = True
        self._selected = False

    def __repr__(self):
        return (f'{self.__class__.__name__}({self._pieceColor},'
                f' {self._square})')

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
    def square(self, value):
        self._square = value

    def forceMove(self, square):
        self.square.reset()
        self.square = square
        square.currentPiece = self
        self.isFirstMove = False
        self.rect.center = square.rect.center

    def moveToSquare(self, square, moves, board=None):
        """Move current piece to given square. Deals with cleanup.

        :param square: Instance of :class:`Square` square to move to.
        :returns: ValueError if piece cannot move to given square.
        """
        if not moves:
            raise ValueError("No possible moves!")
        if square.location in moves:
            self.square.reset()
            self.square = square
            square.currentPiece = self
            self.isFirstMove = False
            self.rect.center = square.rect.center
        else:
            raise ValueError("Piece cannot move to that square.")

    @abstractmethod
    def getValidMoves(self, board):
        """ Method to get available moves. MUST be used in each subclass."""
        raise NotImplementedError

    def _getDiagonalCandidates(self, moves, boardMap,
                               current, rankOffset, fileOffset):
        """
        Method to append possible diagonal moves.
        Offset determines forward or backwards direction (1 or -1)

        :param moves: type `list` moves appended to this object.
        :param _boardMap: type `dict`
        :param current: type `Location` Current Pieces square.
        :param rankOffset: type `Int` + or - 1 for direction.
        :param fileOffset: type `Int` + or - 1 for direction.

        """
        nextMove = logic.build(current, fileOffset, rankOffset)
        while boardMap.get(nextMove):
            if boardMap.get(nextMove).isOccupied:
                if boardMap.get(nextMove).currentPiece.color == self.color:
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
        :param _boardMap: type `dict`
        :param current: type `Location` Current Pieces square.
        :param offset: type `Int` + or - 1 for direction.
        """
        nextMove = logic.build(current, offset, rankOffset=0)
        while boardMap.get(nextMove):
            if boardMap.get(nextMove).isOccupied:
                if boardMap.get(nextMove).currentPiece.color == self.color:
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
        :param _boardMap: type `dict`
        :param current: type `Location` Current Pieces square.
        :param offset: type `Int` + or - 1 for direction.
        """
        nextMove = logic.build(current, 0, offset)
        while boardMap.get(nextMove):
            if boardMap.get(nextMove).isOccupied:
                if boardMap.get(nextMove).currentPiece.color == self.color:
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
        :param _boardMap: type `dict` Board.Map
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
                    if square.isOccupied and square.currentPiece.color == self.color:
                        raise ValueError("Same piece color")
                    moves.append(nextMove)
                except:
                    continue

    def update(self):
        if self._selected:
            self.rect.center = pygame.mouse.get_pos()
        else:
            self.rect.center
