import logic
from AbstractPiece import AbstractPiece
from Files import IMAGES, Color


class King(AbstractPiece):

    def __init__(self, pieceColor, name="King"):
        img = IMAGES['bK'] if pieceColor == Color.DARK else IMAGES['wK']
        super().__init__(name, pieceColor, image=img)
        self.castling = False
        self.rookSquare = None

    def moveToSquare(self, square, moves, board=None):
        if not moves:
            raise ValueError("No possible moves!")

        # Check if castling
        if self.castling and self.isFirstMove:
            currentFile = self.square.file.value
            destFile = square.file.value

            if abs(currentFile - destFile) > 1:
                rook = self.rookSquare.currentPiece
                rook.castle(board)

        if square.location in moves:
            self.square.reset()
            self.square = square
            square.currentPiece = self
            self.isFirstMove = False
            self.rect.center = square.rect.center

    def getValidMoves(self, board):
        moveCandidates = []
        current = self.location
        choices = [1, 0, -1]
        m = board.map

        # Castling
        if self.isFirstMove:
            move = logic.build(current, 2, 0)
            square = board.map.get(move)
            rookSquare = board.getFileUp(square)

            if rookSquare.currentPiece.name == "Rook":
                moveCandidates.append(move)
                self.rookSquare = rookSquare
                self.castling = True

        for i in choices:
            for j in choices:
                rejected = False
                if (i == j == 0):
                    continue

                nextMove = logic.build(current, i, j)
                nextSquare = board.map.get(nextMove)
                if nextSquare:
                    if nextSquare.isOccupied:
                        if nextSquare.currentPiece.color == self.color:
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
