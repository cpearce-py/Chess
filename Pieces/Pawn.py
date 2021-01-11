from AbstractPiece import AbstractPiece
from Location import Location


class Pawn(AbstractPiece):

    def __init__(self, pieceColor, name="Pawn"):
        super().__init__(name, pieceColor)

    def getValidMoves(self, board):
        moveCandidates = []
        if self._isFirstMove:
            moveCandidates.append(LocationFactory.build(self.square,
                                                        fileOffset=0,
                                                        rankOffset=1))
            moveCandidates.append(LocationFactory.build(self.square,
                                                        fileOffset=0,
                                                        rankOffset=2))
