from AbstractPiece import AbstractPiece


class Rook(AbstractPiece):

    def __init__(self, pieceColor, name="Rook"):
        super().__init__(name, pieceColor)
