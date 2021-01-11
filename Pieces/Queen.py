from AbstractPiece import AbstractPiece


class Queen(AbstractPiece):

    def __init__(self, pieceColor, name="Queen"):
        super().__init__(name, pieceColor)

    def getValidMoves(self, board, square):
        pass
