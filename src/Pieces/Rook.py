import logic
from abstract_piece import AbstractPiece
import constants as c

class Rook(AbstractPiece):
    def __init__(self, pieceColor, name="Rook"):
        img = c.IMAGES["bR"] if pieceColor == c.Color.DARK else c.IMAGES["wR"]
        super().__init__(name, pieceColor, image=img)

    def getValidMoves(self, board):
        moveCandidates = []
        _map = board.map
        current = self.location
        self._getFileCandidates(moveCandidates, _map, current, offset=1)
        self._getFileCandidates(moveCandidates, _map, current, offset=-1)
        self._getRankCandidates(moveCandidates, _map, current, offset=1)
        self._getRankCandidates(moveCandidates, _map, current, offset=-1)
        return moveCandidates

    def getAttackMoves(self, board):
        return self.getValidMoves(board)

    def castle(self, board):
        curSquare = self.square
        if curSquare.location.file.name == "H":
            destLoc = logic.build(curSquare.location, -2, 0)
            destSquare = board.map.get(destLoc)
            self.forceMove(destSquare)
        elif curSquare.location.file.name == "A":
            destLoc = logic.build(curSquare.location, 3, 0)
            destSquare = board.map.get(destLoc)
            self.forceMove(destSquare)
        else:
            return False

    def new_getValidMoves(self, board):
        moveCandidates = []
        _map = board.map
        current = self.location
        self._getFileCandidates(moveCandidates, _map, current, offset=1)
        self._getFileCandidates(moveCandidates, _map, current, offset=-1)
        self._getRankCandidates(moveCandidates, _map, current, offset=1)
        self._getRankCandidates(moveCandidates, _map, current, offset=-1)
        return moveCandidates
