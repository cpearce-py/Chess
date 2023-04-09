import constants as c
from pieces import AbstractPiece


class Bishop(AbstractPiece):
    def __init__(self, pieceColor, name="Bishop"):
        img = c.IMAGES["bB"] if pieceColor == c.Color.DARK else c.IMAGES["wB"]
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
