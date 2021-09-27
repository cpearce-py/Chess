import logic
from AbstractPiece import AbstractPiece
from constants import IMAGES, Color


class King(AbstractPiece):

    def __init__(self, pieceColor, name="King"):
        img = IMAGES['bK'] if pieceColor == Color.DARK else IMAGES['wK']
        super().__init__(name, pieceColor, image=img)
        self.castling = False

    def moveToSquare(self, square, moves, board=None):
        if not moves:
            raise ValueError("No possible moves!")

        currentFile = self.square.file.value
        destFile = square.file.value

        # Check if castling
        if self.isFirstMove and abs(destFile - currentFile ) not in [1, 0]:
            currentFile = self.square.file.value
            destFile = square.file.value

            if (destFile - currentFile ) == 2:
                rook = logic.build(self.location, 3, 0)
            else: #(destFile - currentFile) == -2:
                rook = logic.build(self.location, -4, 0)

            rook = board.map.get(rook).currentPiece
            rook.castle(board)

        if square.location in moves:
            self.forceMove(square)
        else:
            raise ValueError("No moves")

    def clear_space(self, board):
        loc = board.map.get(self.location)
        loc.currentPiece = None

    def getAttackMoves(self, board):
        moveCandidates = []
        current = self.location
        choices = [1, 0, -1]
        m = board.map

        # Castling
        if self.isFirstMove:
            for pos in [2, -2]:
                move = logic.build(current, pos, 0)
                square = board.map.get(move)
                if pos > 0:
                    rookSquare = board.getFileUp(square)
                else:
                    rookSquare = board.getFileDown(square)
                    rookSquare = board.getFileDown(rookSquare)

                if rookSquare.currentPiece.name == "Rook":
                    moveCandidates.append(move)
                    self.castling = True

        for i in choices:
            for j in choices:

                if (i == j == 0):
                    continue

                nextMove = logic.build(current, i, j)
                nextSquare = board.map.get(nextMove)
                if nextSquare:
                    if nextSquare.isOccupied:
                        if nextSquare.currentPiece.color == self.color:
                            continue
                        moveCandidates.append(nextMove)
                    moveCandidates.append(nextMove)

        return moveCandidates


    def getValidMoves(self, board):
        allMoves = self.getAttackMoves(board)
        possibleMoves = []
        m = board.map

        for move in allMoves:
            if board.map.get(move):
                rejected = False
                square = board.map.get(move)
                if not square.isOccupied:

                    # If free square, we'll check for attackers
                    attackers = []

                    # Get all possible attacking squares around the free
                    # Square
                    self._getFileCandidates(attackers, m, move, 1)
                    self._getFileCandidates(attackers, m, move, -1)
                    self._getRankCandidates(attackers, m, move, 1)
                    self._getRankCandidates(attackers, m, move, -1)
                    self._getDiagonalCandidates(attackers, m, move, 1, 1)
                    self._getDiagonalCandidates(attackers, m, move, 1, -1)
                    self._getDiagonalCandidates(attackers, m, move, -1, -1)
                    self._getDiagonalCandidates(attackers, m, move, -1, 1)
                    self._getKnightsMove(attackers, m, move)


                    # For each square possible of attacking, we check for
                    # Enemy piece, if so, we can't move there.

                    for square in attackers:
                        if m.get(square).isOccupied:
                            if m.get(square).currentPiece.color != self.color:
                                attacker = m.get(square).currentPiece
                                if move in attacker.getAttackMoves(board):
                                    rejected = True

                if not rejected:
                    possibleMoves.append(move)

        return possibleMoves
