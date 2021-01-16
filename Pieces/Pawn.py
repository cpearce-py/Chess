import logic
from AbstractPiece import AbstractPiece
from Files import Color, Files
from Location import Location


class Pawn(AbstractPiece):

    def __init__(self, pieceColor, name="Pawn"):
        super().__init__(name, pieceColor)

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
