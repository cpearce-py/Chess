# Fen Utilities
from dataclasses import dataclass, field

from Pieces import *
from constants import Color, Files
from Location import Location

START_FEN = "rnbqkbnr/pppppppp/8/8/8/8/PPPPPPPP/RNBQKBNR w KQkq - 0 1"
FEN1 = "rnbqkbnr/pp1ppppp/8/2p5/4P3/5N2/PPPP1PPP/RNBQKB1R b KQkq - 1 2 "

pieceTypeFromSymbol = {
    'k': King,
    'p': Pawn,
    'n': Knight,
    'b': Bishop,
    'r': Rook,
    'q': Queen
}


@dataclass
class PositionInfo:

    squares: dict = field(default_factory=dict, repr=False)
    whiteCastleKingSide: bool = False
    whiteCastleQueenSide: bool = False
    blackCastleKingSide: bool = False
    blackCastleQueenSide: bool = False
    whiteToMove: bool = True

def load_from_fen(fen):
    loadedPositionInfo = PositionInfo()

    sections = fen.split(' ')
    file = 0
    rank = 7

    for symbol in sections[0]:
        if symbol == '/':
            file = 0
            rank -= 1
        else:
            if symbol.isnumeric():
                file += int(symbol)
            else:
                pieceColour = Color.LIGHT if symbol.isupper() else Color.DARK
                pieceType = pieceTypeFromSymbol.get(symbol.lower())
                loc = Location(Files(file+1), rank+1)
                loadedPositionInfo.squares[loc] = pieceType(pieceColour)
                file += 1

    loadedPositionInfo.whiteToMove = (sections[1] == "w")

    castlingRights = sections[2]
    loadedPositionInfo.whiteCastleKingSide = ("K" in castlingRights)
    loadedPositionInfo.whiteCastleQueenSide = ("Q" in castlingRights)
    loadedPositionInfo.blackCastleKingSide = ("k" in castlingRights)
    loadedPositionInfo.blackCastleQueenSide = ("q" in castlingRights)

    return loadedPositionInfo


def main():
    pos = load_from_fen(FEN1)
    print(pos)

if __name__ == '__main__':
    main()
