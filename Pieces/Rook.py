from AbstractPiece import AbstractPiece
from Location import Location
import logic
from Files import Color, Files


class Rook(AbstractPiece):

    def __init__(self, pieceColor, name="Rook"):
        super().__init__(name, pieceColor)

    def getValidMoves(self, board):
        moveCandidates = []

        for x in self._getFileCandidates(board):
            moveCandidates.append(x)
        for x in self._getFileCandidates(board, offset=-1):
            moveCandidates.append(x)
        for x in self._getRankCandidates(board):
            moveCandidates.append(x)
        for x in self._getRankCandidates(board, offset=-1):
            moveCandidates.append(x)

        return moveCandidates

#    def _getFileCandidates(self, board, offset=1):
#        """
#        Method to return available position in a straight file.
#        Offset determines forward or backwards direction from piece.
#
#        Yeild: Location
#        """
#        nextMove = logic.build(
#            self.square, offset, rankOffset=0)
#        while board.map.get(nextMove, False):
#            if board.map.get(nextMove).isOccupied:
#                if board.map.get(nextMove).currentPiece.color == self.color:
#                    break
#                yield nextMove
#                break
#            yield nextMove
#
#            try:
#                nextMove = logic.build(nextMove, offset, rankOffset=0)
#            except ValueError:
#                break
#
#    def _getRankCandidates(self, board, offset=1):
#        """
#        Method to return available position in a straight rank.
#        Offset determines forward or backwards direction from piece.
#
#        Yeild: Location
#        """
#        nextMove = logic.build(
#            self.square, rankOffset=offset, fileOffset=0,)
#        while board.map.get(nextMove, False):
#            if board.map.get(nextMove).isOccupied:
#                if board.map.get(nextMove.currentPiece.color) == self.color:
#                    break
#                yield nextMove
#                break
#            yield nextMove
#
#            try:
#                nextMove = logic.build(
#                    nextMove, fileOffset=0, rankOffset=offset)
#            except ValueError:
#                break
