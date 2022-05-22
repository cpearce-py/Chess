from __future__ import annotations
import logging
from typing import (
    TYPE_CHECKING,
    cast,
    Iterator,
    List,
    Tuple,
    Iterable,
    Optional,
    Mapping,
)

import logic
from squares import Square
from move import Move, EnpassantMove, PromoteMove
import constants as c
from Pieces import Pawn

if TYPE_CHECKING:
    from board import Board
    from location import Location
    DirectionTuple = Tuple[int, int]


log = logging.getLogger(__name__)
f_handler = logging.FileHandler("chess.log")
log.addHandler(f_handler)
log.log(logging.INFO, "Setting up move_gen.")



"""
Current methodology is this:
    - re-initalise instance to clear state (no moves calculated) [x]
    - calculate all attacks on friendly king, including pins. We can store these
    as simple location classes (don't need to generate moves etc.) [x]
    - calculate all possible king moves. This will need to be done creating
    `Move` instances, which we can add to our moves attribute.
    - if in double check we just return King moves, as they're the only legal moves
    - if not, generate all other moves. Again, as instances of `Move`. We need
    to also calculate the Flag type for each move. This will be used later to
    trigger certain events in the game loop ie. End Screen for Checkmate, Promotions etc.
    - We'll then create a simple `Move` instance for the User's attempted move.
    - If that move is in our set of possible moves, we allow the move to occur.
"""

DIR_FOR_PIECE: Mapping[str, List[DirectionTuple]] = {
    "queen":[(1, 1), (1, -1), (-1, -1), (-1, 1), (0, 1), (1, 0), (-1, 0), (0, -1)],
    "rook": [(0, 1), (1, 0), (-1, 0), (0, -1)],
    "bishop": [(1, 1), (1, -1), (-1, -1), (-1, 1)]
}


class MoveGenerator:
    """Class for generating available moves"""

    def __init__(self, board: Board) -> None:
        self.board = board
        self.moves: List[Move] = []
        self.can_queenside_castle = False
        self.can_kingside_castle = False
        self.is_white_move = board.white_to_move
        self.friendly_colour = cast(c.Color, board.color_to_move)
        self.opponent_colour = logic.switch_turn(self.friendly_colour)
        self.generate_moves()
        self.__cached_move: Move
        self.pin_with_direction: Mapping[Location, DirectionTuple] = {}

    def __contains__(self, item: Move) -> bool:
        for move in self.moves:
            if move.squares == item.squares:
                self.__cached_move = move
                return True
        return False

    @property
    def castle_rights(self):
        return (self.can_kingside_castle, self.can_queenside_castle)

    @castle_rights.setter
    def castle_rights(self, rights):
        """Set castle rights for the current state of the generator.
        param rights: `tuple` or `list`
        param rights: `tuple` or `list`
        """
        self.can_kingside_castle = rights[0]
        self.can_queenside_castle = rights[1]

    def get_move(self, temp_move: Move) -> Optional[Move]:
        if self.__cached_move:
            return self.__cached_move
        for move in self.moves:
            if move.squares == temp_move.squares:
                return move

    def generate_moves(self) -> List[Move]:
        """
        Function to generate all the possible moves for the current board
        position. This must be called after each move of a board when in playing
        state.

        Logic is:
            - re-initalise instance to clear state
            - calculate all attacks on friendly king, including pins
            - calculate all possible king moves.
            - if in double check we just return King moves, as they're the only legal moves
            - if not, generate all other moves.

        Function returns a set() of moves. This set can also be accessed from
        the instances moves attribute, but this will only be correct if
        generate_moves() is run, in the boards current position.
        """

        self.init()
        self.generate_attacks_on_king()
        self.generate_king_moves()
        if self.inDoubleCheck:
            return self.moves

        for pawn in self.board.pawns(self.friendly_colour):
            if pawn.location in self.pin_with_direction:
                dir = self.pin_with_direction[pawn.location]
                if abs(dir[0]) == abs(dir[1]):
                    # diagonal pin
                    continue
                if pawn.color == c.Color.LIGHT and dir == (0, 1):
                    continue
                elif pawn.color == c.Color.DARK and dir == (0, -1):
                    continue
                else:
                    pass
            self.get_pawn_moves(pawn)

        for piece in self.board.get_sliding(self.friendly_colour):
            directions = DIR_FOR_PIECE[piece.name]
            if piece.location in self.pin_with_direction:
                dir = self.pin_with_direction[piece.location]
                opposite_dir = (-dir[0], -dir[1])
                directions = [dir, opposite_dir]
            self.get_sliding_moves(piece.square, directions)

        self.highlight(self.moves)

        return self.moves

    def generate_king_moves(self):
        """
        Generate all possible king moves. This also deals with triggering
        generation of opponent attacks. Might change this logic later as this
        method is now dealing with a lot of other logic... will see.
        """
        board = self.board
        king = board.king(self.friendly_colour)
        self.generate_opponent_attacks()
        moves = king.converted_moves(board)
        for move in moves:
            self.moves.append(move)
        self.castle_rights = king.castle_rights

    def generate_attacks_on_king(self):
        board = self.board
        opponent_col = self.opponent_colour
        friendly_col = self.friendly_colour

        king = board.king(friendly_col)
        king_square = king.square


        self.pin_with_direction = {}
        self.pin_moves = []
        self.pin_rays = []

        directions = self._get_sliding_directions(board, opponent_col)
        for direction in directions:
            # Check sliding attacks
            ray = []
            x, y = direction
            possible_pin = False
            friendly_on_ray = False
            next_move = logic.build(king.location, x, y)
            while next_move := board.map.get(next_move):
                ray.append(next_move)
                if piece := next_move.piece:
                    if piece.color == friendly_col:
                        # Check for pin
                        if not friendly_on_ray:
                            friendly_on_ray = True
                        else:  # 2nd friendly on ray therefore no pin
                            break

                    else:  # Is enemy piece
                        if (
                            abs(direction[0]) == abs(direction[1])
                            and piece.name in ["queen", "bishop"]
                        ) or (
                            abs(direction[0]) != abs(direction[1])
                            and piece.name in ["queen", "rook"]
                        ):
                            possible_pin = True
                            if friendly_on_ray:
                                self.pin_moves.append(next_move)
                                break
                            else:
                                # if already in check, then this is double check.
                                self.inDoubleCheck = self.inCheck
                                self.inCheck = True
                                break
                next_move = logic.build(next_move.location, x, y)

            if possible_pin:
                for sqr in ray:
                    self.pin_with_direction[sqr.location] = direction
                self.pin_rays.extend(ray)
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
            attacks = pawn.getAttackMoves(board)
            if king_square.location in attacks:
                self.isPawnCheck = True
                self.inDoubleCheck = self.inCheck
                self.inCheck = True

    def _get_sliding_directions(self, board: Board, opponent_col: c.Color) -> Iterable[DirectionTuple]:
        """
        Setting up directions to check for pins. If there's a queen, we check
        for both diagonal and rook based pins. Otherwise, check for
        bishops or rooks  on the board and their relative directions.
        """
        directions = []
        if board.queen(opponent_col):
            directions.extend([(1, 1), (-1, 1), (1, -1), (-1, -1)])
            directions.extend([(1, 0), (-1, 0), (0, 1), (0, -1)])
        else:
            if board.rooks(opponent_col):
                directions.extend([(1, 0), (-1, 0), (0, 1), (0, -1)])
            if board.bishops(opponent_col):
                directions.extend([(1, 1), (-1, 1), (1, -1), (-1, -1)])
        return directions

    def generate_opponent_attacks(self):
        opponent_col = self.opponent_colour
        board = self.board

        for piece in board.pieces(opponent_col):
            for loc in piece.getAttackMoves(board):
                if loc is None:
                    continue
                square = board.map.get(loc)
                self.opponent_attacks.add(square)

    def init(self):
        self.moves = []
        self.opponent_attacks = set()
        self.opponent_sliding_attacks = set()
        self.opponent_pawn_attacks = set()

        self.inCheck = False
        self.inDoubleCheck = False

        self.is_white_move = self.board.white_to_move
        self.friendly_colour = cast(c.Color, self.board.color_to_move)
        self.opponent_colour = logic.switch_turn(self.friendly_colour)
        self.pin_rays = []

    def highlight(self, set_of_moves=None):
        if not set_of_moves:
            return
        for x in set_of_moves:
            if isinstance(x, Square):
                x.isAttacked = True
            elif isinstance(x, Move):
                x.to_sq.isAttacked = True
            elif isinstance(x, list):  # pinRays
                for x_2 in x:
                    x_2.isAttacked = True
            else:
                log.error("Can't highlight % as an attackable", x)
                print(f"Can't highlight {x} as an attackable.")

    def _getKnightsMove(self, current: Location):
        """
        Method to append a position, type:`Location`, to given list. Based on
        a knights movement.
        """
        board = self.board
        choices = [2, -2, 1, -1]
        for i in choices:
            for j in choices:
                if abs(j) == abs(i):
                    continue

                next_location = logic.build(current, i, j)
                if not next_location:
                    continue

                sqr_attempt = board.get(next_location)
                if sqr_attempt.piece:
                    if sqr_attempt.piece.color == self.friendly_colour:
                        break
                    yield sqr_attempt
                    break
                yield sqr_attempt

    def check_ray(self, ray: List[Location]) -> Iterator[Square]:
        """
        Generator method that moves along a given ray, checking if a square is
        safe to move too. If so, yields the square (typically to be used in
        generation of a `Move` class).
        """
        board = self.board
        friendly_colour = self.friendly_colour
        for loc in ray:
            square = board.get(loc)
            if square.piece:
                if square.piece.color == friendly_colour:
                    break
                else:
                    yield square
                    break
            else:
                yield square

    def get_sliding_moves(self, start_square: Square, directions: List[DirectionTuple]):
        """
        Method to create list of `Moves` from a given start square, based on a direction.
        """
        for direction in directions:
            ray = logic.ray_from(start_square, direction)
            for square in self.check_ray(ray):
                move = Move(start_square, square)
                self.moves.append(move)

    def get_pawn_moves(self, pawn: Pawn) -> List[Move]:
        start_square = pawn.square
        moves = []

        # Check enpassant:
        for pos in [-1, 1]:
            # Make sure we're not out of the boards range
            if start_square.file.value + pos in [0, 9]:
                continue
            adjacent_loc = logic.build(pawn.location, pos, 0)
            adjacent_square = self.board.get(adjacent_loc)  # type: ignore
            if not adjacent_square:
                continue
            piece = adjacent_square.piece
            if not piece:
                continue
            if (
                isinstance(piece, Pawn)
                and piece.color != pawn.color
                and piece.enpassant_able
            ):
                if pawn.color == c.Color.LIGHT:
                    enpassant_attack = logic.build(pawn.location, pos, 1)
                else:
                    enpassant_attack = logic.build(pawn.location, pos, -1)
                enpassant_square = self.board.get(enpassant_attack)  # type: ignore

                enpas_move = EnpassantMove(
                    start_square, enpassant_square, adjacent_square
                )
                moves.append(enpas_move)

        for loc in pawn._getAllValidMoves(self.board):
            to_sq = self.board.get(loc)  # type: ignore

            # Check if attack:
            if loc.file != pawn.location.file:
                if not to_sq.piece:
                    continue
                else:
                    if to_sq.piece.color == self.friendly_colour:
                        continue

            if loc.rank in [1, 8]:  # type:ignore # Checking for promotions
                move = PromoteMove(start_square, to_sq)
                moves.append(move)
                continue

            moves.append(Move(start_square, to_sq))

        self.moves.extend(moves)
        return moves
