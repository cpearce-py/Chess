import logic
from AbstractPiece import AbstractPiece
from constants import IMAGES, Color

def _check_square(sqr):
    if sqr.isOccupied:
        return False
    return True


class King(AbstractPiece):

    def __init__(self, pieceColor, name="King"):
        img = IMAGES['bK'] if pieceColor == Color.DARK else IMAGES['wK']
        super().__init__(name, pieceColor, image=img)
        self.castling = False

    def moveToSquare(self, square, moves, board=None):
        if not moves:
            raise ValueError("No possible moves!")

        if square.location not in moves:
            raise ValueError("Can't move")

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

        self.forceMove(square)

    def clear_space(self, board):
        loc = board.map.get(self.location)
        loc.currentPiece = None

    def checkCastling(self, map):
        """
        Method to check castling possibilities.
        If King can successfully castle, will return the possible squares (of 2)
        he can move too. Otherwise will return an empty array.
        """
        moveCandidates = []

        if not self.isFirstMove:
            return moveCandidates
        
        current = self.location

        for pos in [1,2,3]:
            square = map.get(logic.build(current, pos, 0))
            if square.isOccupied:
                if pos != 3:
                    break
                if square.currentPiece.isFirstMove:
                    moveCandidates.append(logic.build(current, 2, 0))
                    
        for pos in [-1, -2, -3, -4]:
            square = map.get(logic.build(current, pos, 0))
            if square.isOccupied:
                if pos != -4:
                    break
                if square.currentPiece.isFirstMove:
                    moveCandidates.append(logic.build(current, -2, 0))

        return moveCandidates

    def getAttackMoves(self, board):
        moveCandidates = []
        current = self.location
        choices = [1, 0, -1]
        m = board.map

        castling_moves = self.checkCastling(m)

        moveCandidates.extend(castling_moves)
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
