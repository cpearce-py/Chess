import logic
from Files import Color, Files
from AbstractPiece import AbstractPiece
from Location import Location


class Bishop(AbstractPiece):

    def __init__(self, pieceColor, name="Bishop"):
        super().__init__(name, pieceColor)

    def getValidMoves(self, board):
        moveCandidates = []
        _map = board.map
        current = self.square
        self._getDiagonalCandidates(moveCandidates, _map, current, 1, 1)
        self._getDiagonalCandidates(moveCandidates, _map, current, 1, -1)
        self._getDiagonalCandidates(moveCandidates, _map, current, -1, -1)
        self._getDiagonalCandidates(moveCandidates, _map, current, -1, 1)
        return moveCandidates
