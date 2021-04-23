
class Move:

    def __init__(self, fromSq, destSq):
        self.color = fromSq.currentPiece.color
        self.fromSq = fromSq
        self.destSq = destSq
        self.pieceMoved = fromSq.currentPiece
        self.pieceCaptured = None


class CastleMove(Move):

    def __init__(self, fromSq, destSq, Rook):
        super(CastleMove, self).__init__()
        self.rook = Rook
        self.king = fromSq.currentPiece
