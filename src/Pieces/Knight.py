from abstract_piece import AbstractPiece
import constants as c


class Knight(AbstractPiece):
    def __init__(self, pieceColor, name="knight"):
        img = c.IMAGES["bN"] if pieceColor == c.Color.DARK else c.IMAGES["wN"]
        super().__init__(name, pieceColor, image=img)

    def getValidMoves(self, board):
        moveCandidates = []
        current = self.location
        boardMap = board.map
        self._getKnightsMove(moveCandidates, boardMap, current)
        return moveCandidates

    def getAttackMoves(self, board):
        return self.getValidMoves(board)
