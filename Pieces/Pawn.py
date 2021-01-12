from AbstractPiece import AbstractPiece
from Location import Location
import logic
from Files import Color, Files


class Pawn(AbstractPiece):

    def __init__(self, pieceColor, name="Pawn"):
        super().__init__(name, pieceColor)

    def getValidMoves(self, board):

        moveCandidates = []
        moveCandidates.append(logic.build(
            self.square, fileOffset=0, rankOffset=1))

        if self._isFirstMove:
            moveCandidates.append(logic.build(
                self.square, fileOffset=0, rankOffset=2))

        moveCandidates.append(logic.build(
            self.square, fileOffset=1, rankOffset=1))

        moveCandidates.append(logic.build(
            self.square, fileOffset=-1, rankOffset=1))

        # Filter out None (s)
        # Leaves only valid Board squares
        moveCandidates = list(
            filter(lambda x: board.map.get(x, False), moveCandidates))

        # Check board if there is a piece in the way.
        moveCandidates = list(
            filter(lambda x: x.file == self.square.file and not board.map.get(x).isOccupied, moveCandidates))

        moveCandidates = list(
            filter(lambda x: board.map.get(x).currentPiece.color == self.color, moveCandidates))

        return moveCandidates
