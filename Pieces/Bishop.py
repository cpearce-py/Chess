from AbstractPiece import AbstractPiece


class Bishop(AbstractPiece):

    def __init__(self, pieceColor, name="Bishop"):
        super().__init__(name, pieceColor)

    def getValidMoves(self, board):
        moveCandidates = []
        _map = board.map
        current = self.square
        self.getMoves(moveCandidates, _map, current,
                      rankOffset=1, fileOffset=0)
        self.getMoves(moveCandidates, _map, current,
                      rankOffset=-1, fileOffset=0)
        self.getMoves(moveCandidates, _map, current,
                      rankOffset=0, fileOffset=1)

    def getMoves(candidates, _map, current, fileOffset, rankOffset):
        nextMove = logic.build(current, fileOffset, rankOffset)
        while _map.get(nextMove):
            if _map.get(nextMove).isOccupied:
                if _map.get(nextMove).currentPiece.color == self.colour:
                    break
                candidates.append(nextMove)
                break
            candidates.append(nextMove)
            try:
                logic.build(nextMove, fileOffset, rankOffset)
            except ValueError:
                break
