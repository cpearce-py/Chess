from typing import Set

import logic
from move import Move


class MoveGenerator:

    def __init__(self, board):
        self.board = board
        self.moves: Set[Move] = set()
        self.can_queenside_castle = False
        self.can_kingside_castle = False

        self.generate_moves()

    @property
    def castle_rights(self):
        return (self.can_kingside_castle, self.can_queenside_castle)

    @castle_rights.setter
    def castle_rights(self, rights):
        self.can_kingside_castle = rights[0]
        self.can_queenside_castle = rights[1]
    
    def generate_moves(self) -> Set[Move]:
        """
        Function to generate all the possible moves for the current board 
        position. 

        Logic is:
            - re-initalise instance to clear state 
            - calculate all attacks on friendly king, including pins 
            - calculate all possible king moves. 
            - if in double check we just return King moves, as they're the only legal moves
            - if not, generate all other moves. 

        Function returns a set() of moves. This set can also be accessed from 
        the instances moves attribute, but this will only be correct if 
        generate_moves() is run by the instance, in the boards current position. 
        """

        self.init()
        self.calculate_attacks()
        self.generate_king_moves()
        if self.inDoubleCheck:
            return self.moves
        self.highlight(self.pinRays)

        return self.moves

    def generate_king_moves(self):
        king = self.board.king(self.friendly_colour)
        board = self.board
        self.generate_opponent_attacks()
        moves = king.getValidMoves(board)
        self.castle_rights = king.castle_rights


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

    def generate_opponent_attacks(self):
        opponent_col = self.opponent_colour
        board = self.board

        for piece in self.board.pieces(opponent_col):
            for loc in piece.getAttackMoves(board):
                if loc is None:
                    continue
                square = board.map.get(loc)
                self.opponent_attacks.add(square)
        
    def init(self):
        self.moves = set()
        self.opponent_attacks = set()
        self.opponent_sliding_attacks = set()
        self.opponent_pawn_attacks = set()

        self.inCheck = False
        self.inDoubleCheck = False
        self.pinsExistInPosition = False

        self.isWhiteMove = self.board.whiteToMove
        self.friendly_colour = self.board.color_to_move
        self.opponent_colour = logic.switch_turn(self.friendly_colour)
        self.pinRays = []

    def highlight(self, set_of_moves=None):
        if set_of_moves is None:
            return
            
        try:
            for square in set_of_moves:
                square.isAttacked = True 
        except AttributeError: # if pinRays is passed, we need to go 2 levels deep.
            for ray in set_of_moves:
                for square in ray:
                    square.isAttacked = True

if __name__ == '__main__':
    import Board
    b = Board.Board().init()
    m = MoveGenerator(b)