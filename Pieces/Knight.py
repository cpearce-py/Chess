from AbstractPiece import AbstractPiece
from constants import Color, IMAGES


class Knight(AbstractPiece):
    def __init__(self, pieceColor, name="knight"):
        img = IMAGES["bN"] if pieceColor == Color.DARK else IMAGES["wN"]
        super().__init__(name, pieceColor, image=img)

    def getValidMoves(self, board):
        moveCandidates = []
        current = self.location
        boardMap = board.map
        self._getKnightsMove(moveCandidates, boardMap, current)
        return moveCandidates

    def getAttackMoves(self, board):
        return self.getValidMoves(board)
