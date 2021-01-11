from AbstractPiece import AbstractPiece
from Location import Location
import logic


class Pawn(AbstractPiece):

    def __init__(self, pieceColor, name="Pawn"):
        super().__init__(name, pieceColor)

    def getValidMoves(self, board):

        moveCandidates = []
        moveCandidates.append(logic.build(self.square, fileOffset=0,
                                          rankOffset=1))
        if self._isFirstMove:
            moveCandidates.append(logic.build(self.square,
                                              fileOffset=0,
                                              rankOffset=2))
        moveCandidates.append(logic.build(self.square, fileOffset=1,
                                          rankOffset=1))
        moveCandidates.append(logic.build(self.square, fileOffset=-1,
                                          rankOffset=1))

        # Filter out only valid moves
        filter(lambda x: board.map.get(x), moveCandidates)
        return moveCandidates
