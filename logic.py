from typing import List
from location import Location
from constants import Files, Color
from move import Move

__all__ = ("build", "switch_turn")


def build(current, fileOffset, rankOffset):
    """
    Generates a new Location class for where a given Location will end up
    based on a given file and rank offset.

    current: Location(Files.FILES, int Rank})
    fileOffset: Int
    rankOffset: Int

    returns: Location()
    """
    if not isinstance(current, Location):
        raise ValueError("Please pass current position as Location class")
    currentFile = current.file.value

    # To avoid Enums ValueError if file not located.
    try:
        return Location(Files(currentFile + fileOffset), current.rank + rankOffset)
    except ValueError:
        return None


def switch_turn(turn):
    return {Color.LIGHT: Color.DARK, Color.DARK: Color.LIGHT}.get(turn)


def convert(moves: List, piece, board):
    piece_square = piece.square
    for move in moves:
        toSq = board.map.get(move)
        yield Move(piece_square, toSq)
