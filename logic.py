from Location import Location
from Files import Files, RANKS, Color
from Pieces import *


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
    newFile = currentFile + fileOffset
    newRank = current.rank + rankOffset

    # To avoid Enums ValueError if file not located.
    try:
        return Location(Files(currentFile + fileOffset), current.rank + rankOffset)
    except ValueError:
        return None


def initialize():
    pieces = {}

    # Rooks
    pieces[Location(Files.A, 1)] = Rook(Color.LIGHT)
    pieces[Location(Files.H, 1)] = Rook(Color.LIGHT)
    pieces[Location(Files.A, 8)] = Rook(Color.DARK)
    pieces[Location(Files.H, 8)] = Rook(Color.DARK)

    # Knights
    pieces[Location(Files.B, 1)] = Knight(Color.LIGHT)
    pieces[Location(Files.G, 1)] = Knight(Color.LIGHT)
    pieces[Location(Files.B, 8)] = Knight(Color.DARK)
    pieces[Location(Files.G, 8)] = Knight(Color.DARK)

    # Bishops
    pieces[Location(Files.C, 1)] = Bishop(Color.LIGHT)
    pieces[Location(Files.F, 1)] = Bishop(Color.LIGHT)
    pieces[Location(Files.C, 8)] = Bishop(Color.DARK)
    pieces[Location(Files.F, 8)] = Bishop(Color.DARK)

    # Queens
    pieces[Location(Files.D, 1)] = Queen(Color.LIGHT)
    pieces[Location(Files.D, 8)] = Queen(Color.DARK)

    # Kings
    pieces[Location(Files.E, 1)] = King(Color.LIGHT)
    pieces[Location(Files.E, 8)] = King(Color.DARK)

    # Pawns
    for file in Files:
        pieces[Location(file, 2)] = Pawn(Color.LIGHT)
        pieces[Location(file, 7)] = Pawn(Color.DARK)

    return pieces
