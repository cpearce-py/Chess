from __future__ import annotations
from typing import TYPE_CHECKING, Set

import logic
from abstract_piece import AbstractPiece
from constants import IMAGES, Color
from squares import Square
from move import Move, CastleMove

if TYPE_CHECKING:
    from board import Board


class King(AbstractPiece):
    def __init__(self, pieceColor, name="King"):
        img = IMAGES["bK"] if pieceColor == Color.DARK else IMAGES["wK"]
        super().__init__(name, pieceColor, image=img)
        self.castling = False
        self.castle_rook = None
        self.can_kingside_castle = False
        self.can_queenside_castle = False

    @property
    def castle_rights(self):
        return (self.can_kingside_castle, self.can_queenside_castle)

    def moveToSquare(self, square: Square, board=None):

        currentFile = self.square.file.value
        destFile = square.file.value

        # Check if castling
        if self.isFirstMove and abs(destFile - currentFile) not in [1, 0]:
            currentFile = self.square.file.value
            destFile = square.file.value

            if (destFile - currentFile) == 2:
                rook = logic.build(self.location, 3, 0)
            else:  # (destFile - currentFile) == -2:
                rook = logic.build(self.location, -4, 0)

            rook = board.map.get(rook).piece
            rook.castle(board)
            self.castle_rook = rook

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

        for pos in [1, 2, 3]:
            square = map.get(logic.build(current, pos, 0))
            if square.isOccupied:
                if pos != 3:
                    break
                if square.piece.isFirstMove:
                    self.can_kingside_castle = True
                    moveCandidates.append(logic.build(current, 2, 0))

        for pos in [-1, -2, -3, -4]:
            square = map.get(logic.build(current, pos, 0))
            if square.isOccupied:
                if pos != -4:
                    break
                if square.piece.isFirstMove:
                    self.can_queenside_castle = True
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

                if i == j == 0:
                    continue

                nextMove = logic.build(current, i, j)
                if nextSquare := board.map.get(nextMove):
                    if nextSquare.isOccupied:
                        if nextSquare.piece.color == self.color:
                            continue
                        moveCandidates.append(nextMove)
                    moveCandidates.append(nextMove)

        return moveCandidates

    def getValidMoves(self, board: Board) -> Set[Move]:
        """
        Method to return all possible moves king can make.

        :param board: current board state
        :type board: class `Board`
        :return: all possible moves the king can make in current position.
        :rtype: `list` of `Location`
        """
        cur_sqr = self.square
        allMoves = self.getAttackMoves(board)
        possibleMoves = []
        m = board.map
        for move in allMoves:
            if square := board.map.get(move):
                rejected = False
                if square.isOccupied:
                    continue

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
                    if attacker_square := board.get(square):
                        if (
                            attacker_square.piece
                            and attacker_square.piece.color != self.color
                        ):
                            attacker = attacker_square.piece
                            if move in attacker.getAttackMoves(board):
                                rejected = True

                if rejected:
                    continue

                if (move.file.value - cur_sqr.file.value) == 2:
                    rook_loc = logic.build(self.location, 3, 0)
                    rook_piece = board.get(rook_loc).piece
                    CastleMove(cur_sqr, move, rook_piece)  # type: ignore
                else:  # (destFile - currentFile) == -2:
                    rook = logic.build(self.location, -4, 0)  # type: ignore
                move = board.get(move)
                if move:
                    move = Move(cur_sqr, move)
                    possibleMoves.append(move)

        return possibleMoves

    def converted_moves(self, board):
        moves = self.getValidMoves(board)
        return logic.convert(moves, self, board)
