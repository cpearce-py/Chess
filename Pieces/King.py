import logic
from AbstractPiece import AbstractPiece


class King(AbstractPiece):

    def __init__(self, pieceColor, name="King"):
        super().__init__(name, pieceColor)

    def getValidMoves(self, board):
        moveCandidates = []
        current = self.location
        choices = [1, 0, -1]
        m = board.map

        for i in choices:
            for j in choices:
                rejected = False
                if (i == j == 0):
                    continue

                nextMove = logic.build(current, i, j)
                if board.map.get(nextMove):
                    if board.map.get(nextMove).isOccupied:
                        if board.map.get(nextMove).currentPiece.color == self.color:
                            continue
                        moveCandidates.append(nextMove)
                        continue

                    # If free square, we'll check for attackers
                    attackers = []

                    # Get all possible attacking squares around the free
                    # Square
                    self._getFileCandidates(attackers, m, nextMove, 1)
                    self._getFileCandidates(attackers, m, nextMove, -1)
                    self._getRankCandidates(attackers, m, nextMove, 1)
                    self._getRankCandidates(attackers, m, nextMove, -1)
                    self._getDiagonalCandidates(attackers, m, nextMove, 1, 1)
                    self._getDiagonalCandidates(attackers, m, nextMove, 1, -1)
                    self._getDiagonalCandidates(attackers, m, nextMove, -1, -1)
                    self._getDiagonalCandidates(attackers, m, nextMove, -1, 1)

                    # For each square possible of attacking, we check for
                    # Enemy piece, if so, we can't move there.
                    for square in attackers:
                        if m.get(square).isOccupied:
                            if m.get(square).currentPiece.color != self.color:
                                attacker = m.get(square).currentPiece
                                if nextMove in attacker.getAttackMoves(board):
                                    rejected = True

                if not rejected:
                    moveCandidates.append(nextMove)

        return moveCandidates
