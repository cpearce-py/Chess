import logic
from AbstractPiece import AbstractPiece
from Files import Color, Files, IMAGES
from Location import Location


class Rook(AbstractPiece):

    def __init__(self, pieceColor, name="Rook"):
        img = IMAGES['bR'] if pieceColor == Color.DARK else IMAGES['wR']
        super().__init__(name, pieceColor, image=img)

    def getValidMoves(self, board):
        moveCandidates = []
        _map = board.map
        current = self.location
        self._getFileCandidates(
            moveCandidates, _map, current, offset=1)
        self._getFileCandidates(
            moveCandidates, _map, current, offset=-1)
        self._getRankCandidates(
            moveCandidates, _map, current, offset=1)
        self._getRankCandidates(
            moveCandidates, _map, current, offset=-1)
        return moveCandidates

    def getAttackMoves(self, board):
        return self.getValidMoves(board)
