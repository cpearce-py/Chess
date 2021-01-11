from AbstractPiece import AbstractPiece


class Knight(AbstractPiece):

    def __init__(self, pieceColor, name="Knight"):
        super().__init__(name, pieceColor)
