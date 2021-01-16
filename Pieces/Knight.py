import logic
from AbstractPiece import AbstractPiece
from Files import Color
from Location import Location


class Knight(AbstractPiece):

    def __init__(self, pieceColor, name="knight"):
        super().__init__(name, pieceColor)

    def getValidMoves(self, board):
        moveCandidates = []
        current = self.location
        choices = [2, -2, 1, -1]
        for i in choices:
            for j in choices:
                if abs(j) == abs(i):
                    continue

                nextMove = logic.build(current, i, j)
                while board.map.get(nextMove):
                    if board.map.get(nextMove).isOccupied:
                        if board.map.get(nextMove).currentPiece.color == self.color:
                            break
                        moveCandidates.append(nextMove)
                        break
                    moveCandidates.append(nextMove)
                    nextMove = logic.build(nextMove, i, j)
        return moveCandidates

    def getAttackMoves(self, board):
        return self.getValidMoves(board)
