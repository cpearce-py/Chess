from AbstractPiece import AbstractPiece


class Pawn(AbstractPiece):

    def __init__(self, pieceColor, name="Pawn"):
        super().__init__(name, pieceColor)
