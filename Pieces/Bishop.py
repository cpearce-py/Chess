import logic
from constants import Color, Files, IMAGES
from AbstractPiece import AbstractPiece
from Location import Location


class Bishop(AbstractPiece):

    def __init__(self, pieceColor, name="Bishop"):
        img = IMAGES['bB'] if pieceColor == Color.DARK else IMAGES['wB']
        super().__init__(name, pieceColor, image=img)

    def getValidMoves(self, board):
        moveCandidates = []
        _map = board.map
        current = self.location
        self._getDiagonalCandidates(moveCandidates, _map, current, 1, 1)
        self._getDiagonalCandidates(moveCandidates, _map, current, 1, -1)
        self._getDiagonalCandidates(moveCandidates, _map, current, -1, -1)
        self._getDiagonalCandidates(moveCandidates, _map, current, -1, 1)
        return moveCandidates

    def getAttackMoves(self, board):
        return self.getValidMoves(board)
