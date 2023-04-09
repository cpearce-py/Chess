from __future__ import annotations
from typing import TYPE_CHECKING, Iterable, Union, List, Tuple
from location import Location
import constants as c
from move import Move

if TYPE_CHECKING:
    from board import Board
    from squares import Square

__all__ = ("build", "switch_turn", "is_valid")

Direction = Union[Tuple[int, int], List[int]]


def build(current: Location, fileOffset: int, rankOffset: int) -> Location:
    """
    Generates a new Location class for where a given Location will end up
    based on a given file and rank offset.

    returns: Location()
    """
    if not isinstance(current, Location):
        raise ValueError("Please pass current position as Location class")

    new_file = current.file.value + fileOffset
    new_rank = current.rank + rankOffset

    if not is_valid(new_file) or not is_valid(new_rank):
        return None # type: ignore

    return Location(c.Files(new_file), new_rank)


def ray_from(start: Union[Location, Square], direction: Direction):
    """
    Create ray starting a given `Location` or `Square`, going outwards in a given direction.
    Resulting ray does NOT include start square.
    """

    if direction[0] == 0 and direction[1] == 0:
        raise ValueError("Direction iterable cannot only contain 0's.")
    ray = []
    file_dir = direction[0]
    rank_dir = direction[1]

    diagonal_slide = False if (file_dir == 0 or rank_dir == 0) else True

    if diagonal_slide:
        file_end, file_step = (9, 1) if file_dir > 0 else (0, -1)
        rank_end, rank_step = (9, 1) if rank_dir > 0 else (0, -1)
        rank_range = range(start.rank, rank_end, rank_step)
        file_range = range(start.file.value, file_end, file_step)
        for file, rank in zip(file_range, rank_range):
            loc = Location(c.Files(file), rank)
            ray.append(loc)

    else:
        if file_dir == 0:
            end, step = (9, 1) if rank_dir > 0 else (0, -1)
            rank_increments = range(start.rank, end, step)
            for rank in rank_increments:
                loc = Location(start.file, rank)
                ray.append(loc)
        else:
            end, step = (9, 1) if file_dir > 0 else (0, -1)
            file_increments = range(start.file.value, end, step)
            for file in file_increments:
                loc = Location(c.Files(file), start.rank)
                ray.append(loc)

    return ray[1:]


def square_is_capturable(start: Union[Square, Location], direction: Direction, board: Board) -> bool:

    if isinstance(start, Square):
        start = start.location

    file_offset = direction[0]
    rank_offset = direction[1]
    new_square = build(start, rank_offset, file_offset)
    return True


def switch_turn(turn: c.Color) -> c.Color:
    return {c.Color.LIGHT: c.Color.DARK, c.Color.DARK: c.Color.LIGHT}[turn]


def is_valid(loc: int):
    return 1 <= loc <= 8


def convert(moves: Iterable, piece, board):
    piece_square = piece.square
    for move in moves:
        toSq = board.map.get(move)
        yield Move(piece_square, toSq)
