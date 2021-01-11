from AbstractPiece import AbstractPiece


class King(AbstractPiece):

    def __init__(self, pieceColor, name="King"):
        super().__init__(name, pieceColor)
