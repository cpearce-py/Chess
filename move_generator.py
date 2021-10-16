from typing import List

import logic
from move import Move
from constants import Color


class MoveGenerator:

    def __init__(self, board):
        self.board = board
        self.moves: List[Move] = set()

        self.isWhiteMove = board.isWhiteMove

        self.generate_moves()

    def generate_moves(self) -> List[Move]:
        board = self.board

        self.init()

        self.calculate_attacks()

        # If King in Double Check, only King moves are valid so we can 
        # return out.
        if self.inDoubleCheck:
            return self.moves

    def calculate_attacks(self):
        """
        Calculate all attacks aimed at the King. 
        """
        board = self.board
        king = board.king(Color.LIGHT)
        king_square = king.square
        moves = self.moves

        opponent_col = self.opponent_colour
        friendly_col = self.friendly_colour

        first_friendly_on_ray = True

        if not board.queen(opponent_col):

            if board.rooks(opponent_col):
                nextMove = logic.build(king_square.loc, 1, 0)
                while nextMove := board.map.get(nextMove):
                    if piece := nextMove.piece:
                        if piece.colour == friendly_col:
                            if not first_friendly_on_ray:
                                first_friendly_on_ray = False
                            else:
                                break
                        else:
                            break

                self._getFileAttacks()
                self._getRankAttacks()
            if board.bishops(opponent_col):
                self._getDiagonalAttacks()

    def init(self):
        board = self.board
        self.moves = set()
        self.inCheck = False
        self.inDoubleCheck = False
        self.pinsExistInPosition = False

        self.isWhiteMove = self.board.whiteToMove
        self.friendly_colour = Color.LIGHT if board.isWhiteMove else Color.DARK
        self.opponent_colour = Color.DARK if board.isWhiteMove else Color.LIGHT


if __name__ == '__main__':
    import Board
    b = Board.Board().init()
    m = MoveGenerator(b)
