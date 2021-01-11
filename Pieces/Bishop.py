from AbstractPiece import AbstractPiece


class Bishop(AbstractPiece):

    def __init__(self, pieceColor, name="Bishop"):
        super().__init__(name, pieceColor)
