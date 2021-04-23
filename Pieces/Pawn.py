import logic
from AbstractPiece import AbstractPiece
from Files import Color, Files, IMAGES, RANKS
from Location import Location
from Pieces.Bishop import Bishop
from Pieces.Queen import Queen
from Pieces.Knight import Knight
from Pieces.Rook import Rook
from ui import Button
import pygame

CLASSES = {"queen": Queen,
            "rook": Rook,
            "knight": Knight,
            "bishop": Bishop
            }

class Pawn(AbstractPiece):

    def __init__(self, pieceColor, name="Pawn"):
        img = IMAGES['bp'] if pieceColor == Color.DARK else IMAGES['wp']
        super().__init__(name, pieceColor, image=img)

    def moveToSquare(self, square, moves, board=None):
        if not moves:
            raise ValueError("No possible moves!")

        if square.location in moves:

            # Check for promotion
            if square.location.rank in [1, 8]:
                btn = Button("Queen", 200, 50, 100, 50)
                self.promote()

            self.forceMove(square)
        else:
            raise ValueError("Piece cannont move to that square.")

    def promote(self, piece="queen"):
        """
        Method to promote current instance of `Pawn` to given piece.txt

        :param piece: type `str` name of piece to promote too.
        default = queen.
        """
        if not isinstance(piece, str):
            raise ValueError("Pass piece as string.")
        piece = CLASSES.get(piece.lower())
        square = self.square
        self.__class__ = piece
        self.__init__(self.color)
        square.reset()
        self.square = square


    def getValidMoves(self, board):

        moveCandidates = []

        for move in self._getAllValidMoves(board):
            if not board.map.get(move):
                continue
            if (move.file != self.square.file and not
                    board.map.get(move).isOccupied):
                continue
            if (move.file == self.square.file and
                    board.map.get(move).isOccupied):
                continue
            if (move.file != self.square.file and
                    board.map.get(move).isOccupied):
                if board.map.get(move).currentPiece.color == self.color:
                    continue

            moveCandidates.append(move)

        return moveCandidates

    def _getAllValidMoves(self, board):

        if self._pieceColor == Color.LIGHT:
            if self.isFirstMove:
                yield logic.build(self.location, fileOffset=0, rankOffset=2)

            yield logic.build(self.location, fileOffset=0, rankOffset=1)
            yield logic.build(self.location, fileOffset=1, rankOffset=1)
            yield logic.build(self.location, fileOffset=-1, rankOffset=1)

        else:
            if self.isFirstMove:
                yield logic.build(self.location, fileOffset=0, rankOffset=-2)

            yield logic.build(self.location, fileOffset=0, rankOffset=-1)
            yield logic.build(self.location, fileOffset=1, rankOffset=-1)
            yield logic.build(self.location, fileOffset=-1, rankOffset=-1)

    def getAttackMoves(self, board):

        if self._pieceColor == Color.LIGHT:
            yield logic.build(self.location, fileOffset=1, rankOffset=1)
            yield logic.build(self.location, fileOffset=-1, rankOffset=1)

        else:
            yield logic.build(self.location, fileOffset=1, rankOffset=-1)
            yield logic.build(self.location, fileOffset=-1, rankOffset=-1)
