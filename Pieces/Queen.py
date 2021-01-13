import logic
from AbstractPiece import AbstractPiece
from Files import Color, Files
from Location import Location


class Queen(AbstractPiece):

    def __init__(self, pieceColor, name="Queen"):
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
        self._getDiagonalCandidates(moveCandidates, _map, current, 1, 1)
        self._getDiagonalCandidates(moveCandidates, _map, current, 1, -1)
        self._getDiagonalCandidates(moveCandidates, _map, current, -1, -1)
        self._getDiagonalCandidates(moveCandidates, _map, current, -1, 1)
        return moveCandidates
