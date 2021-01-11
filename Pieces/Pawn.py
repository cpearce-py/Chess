from AbstractPiece import AbstractPiece
from Location import Location
from LocationFactory import LocationFactory


class Pawn(AbstractPiece):

    def __init__(self, pieceColor, name="Pawn"):
        super().__init__(name, pieceColor)

    def getValidMoves(self, board):

        moveCandidates = []
        moveCandidates.append(LocationFactory.build(self.square, fileOffset=0,
                                                    rankOffset=1))
        if self._isFirstMove:
            moveCandidates.append(LocationFactory.build(self.square,
                                                        fileOffset=0,
                                                        rankOffset=2))
        moveCandidates.append(LocationFactory.build(self.square, fileOffset=1,
                                                    rankOffset=1))
        moveCandidates.append(LocationFactory.build(self.square, fileOffset=-1,
                                                    rankOffset=1))
#        possibleMoves = []
#        if candidate in moveCandidates:
#            if board.map.get(candidate):
#                possibleMoves.append(candidate)

        filter(lambda x: board.map.get(x), moveCandidates)
        return moveCandidates
