import logic
from AbstractPiece import AbstractPiece
from Files import Color, Files
from Location import Location


class Rook(AbstractPiece):

    def __init__(self, pieceColor, name="Rook"):
        super().__init__(name, pieceColor)

    def getValidMoves(self, board):
        moveCandidates = []
        _map = board.map
        current = self.square
        self._getFileCandidates(
            moveCandidates, _map, current, offset=1)
        self._getFileCandidates(
            moveCandidates, _map, current, offset=-1)
        self._getRankCandidates(
            moveCandidates, _map, current, offset=1)
        self._getRankCandidates(
            moveCandidates, _map, current, offset=-1)
        return moveCandidates

    def _getFileCandidates(self, moves, _map, current, offset):
        """
        Method to append a position, type:`Location`, to given list.
        Offset determines forward or backwards direction from piece.

        moves: type `list`
        Yeild: Location
        """
        nextMove = logic.build(current, offset, rankOffset=0)
        while _map.get(nextMove):
            if _map.get(nextMove).isOccupied:
                if _map.get(nextMove).currentPiece.color == self.color:
                    break
                moves.append(nextMove)
                break
            moves.append(nextMove)
            try:
                nextMove = logic.build(nextMove, offset, rankOffset=0)
            except ValueError:
                break

    def _getRankCandidates(self, moves, _map, current, offset):
        """
        Method to append a position, type:`Location`, to given list.
        Offset determines forward or backwards direction from piece.

        moves: type `list`
        Offset determines forward or backwards direction from piece.
        """
        nextMove = logic.build(current, 0, offset)
        while _map.get(nextMove):
            if _map.get(nextMove).isOccupied:
                if _map.get(nextMove).currentPiece.color == self.color:
                    break
                moves.append(nextMove)
                break
            moves.append(nextMove)
            try:
                nextMove = logic.build(nextMove, 0, offset)
            except ValueError:
                break
