import logic
from AbstractPiece import AbstractPiece
from Files import Color
from Location import Location


class Knight(AbstractPiece):

    def __init__(self, pieceColor, name="Knight"):
        super().__init__(name, pieceColor)

    def getValidMoves(self, board):
        moveCandidates = []
        _map = board.map
        current = self.square
        choices = [2, -2, 1, -1]
        for i in choices:
            for j in choices:
                if abs(j) == abs(i):
                    continue

                nextMove = moveCandidates.append(
                    logic.build(current, i, j))

        return moveCandidates
