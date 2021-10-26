from typing import List, Set

import logic
from move import Move
from constants import Color


class MoveGenerator:

    def __init__(self, board):
        self.board = board
        self.moves: Set[Move] = set()

        self.generate_moves()

    def generate_moves(self) -> List[Move]:

        # Re-initalise to a clean state
        self.init()

        # Calculate all attacks mode on the king, including pins
        self.calculate_attacks()

        # Generate possible king moves.
        self.generate_king_moves()


        # If King in Double Check, only King moves are valid so we can 
        # return out. (But we need to get the king moves first)
        if self.inDoubleCheck:
            return self.moves

        # Now we can calculate all other possible moves. 
        # self.generate_sliding_moves()
        # self.generate_knight_moves()
        # self.generate_pawn_moves()


        # Method to highlight squares, for visual testing.
        self.highlight()

        return self.moves

    def generate_king_moves(self):
        king = self.board.king(self.friendly_colour)
        current = king.location
        choices = [1, 0, -1]

        for i in choices:
            for j in choices:
                if (i == j == 0):
                    continue

                move = logic.build(current, i, j)
                if nextSquare := self.board.map.get(move):
                    pass

    def calculate_attacks(self):
        """
        Calculate all attacks aimed at the King. 
        """
        board = self.board

        
        opponent_col = self.opponent_colour
        friendly_col = self.friendly_colour

        king = board.king(friendly_col)
        king_square = king.square


        self.pinsExistInPosition = False

        self.pinMoves = []
        self.pinRays = []

        directions = self._get_sliding_directions(board, opponent_col)
        for direction in directions:
            # Check sliding attacks 
            ray = []
            x, y = direction
            possible_pin = False
            friendly_on_ray = False
            nextMove = logic.build(king.location, x, y)
            while nextMove := board.map.get(nextMove):
                ray.append(nextMove)
                if piece := nextMove.piece:
                    if piece.color == friendly_col:
                        # Check for pin
                        if not friendly_on_ray:
                            friendly_on_ray = True
                        else: # 2nd friendly on ray therefore no pin
                            break

                    else: # Is enemy piece
                        if (
                            abs(direction[0]) == abs(direction[1]) and 
                            piece.name in ['queen', 'bishop']) or (
                            abs(direction[0]) != abs(direction[1]) and 
                            piece.name in ['queen', 'rook']
                            ):
                            possible_pin = True
                            if friendly_on_ray:
                                self.pinsExistInPosition = True
                                self.pinMoves.append(nextMove)
                                break
                            else:
                                # if already in check, then this is double check.
                                self.inDoubleCheck = self.inCheck 
                                self.inCheck = True
                                break
                nextMove = logic.build(nextMove.location, x, y)

            if possible_pin:
                self.pinRays.append(ray)   
            if self.inDoubleCheck:
                break

        # Check knight attacks
        knights = board.knights(opponent_col)
        self.isKnightCheck = False
        for knight in knights:
            if king_square.location in knight.getAttackMoves(board):
                self.isKnightCheck = True
                self.inDoubleCheck = self.inCheck
                self.inCheck = True

        # Check pawn attacks
        pawns = board.pawns(opponent_col)
        self.isPawnCheck = False
        for pawn in pawns:
            if king_square.location in pawn.getAttackMoves(board):
                self.isPawnCheck = True
                self.inDoubleCheck = self.inCheck
                self.inCheck = True

    def _get_sliding_directions(self, board, opponent_col):
        """ Setting up directions to check for pins. If there's a queen, we check
        for both diagonal and rook based pins. Otherwise, check for 
        bishops or rooks  on the board and their relative directions. """
        directions = []
        if board.queen(opponent_col):
            directions.extend([(1,1), (-1,1), (1,-1), (-1,-1)])
            directions.extend([(1,0), (-1,0), (0,1), (0,-1)])
        else:
            if board.rooks(opponent_col):
                directions.extend([(1,0), (-1,0), (0,1), (0,-1)])
            if board.bishops(opponent_col):
                directions.extend([(1,1), (-1,1), (1,-1), (-1,-1)])
        return directions

    def init(self):
        self.moves = set()
        self.inCheck = False
        self.inDoubleCheck = False
        self.pinsExistInPosition = False

        self.isWhiteMove = self.board.whiteToMove
        self.friendly_colour = self.board.color_to_move
        self.opponent_colour = Color.DARK if self.friendly_colour == Color.LIGHT else Color.LIGHT

        self.pinRays = []

    def highlight(self):
        for ray in self.pinRays:
            for square in ray:
                square.isAttacked = True

if __name__ == '__main__':
    import Board
    b = Board.Board().init()
    m = MoveGenerator(b)