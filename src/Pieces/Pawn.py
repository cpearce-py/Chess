import logic
from AbstractPiece import AbstractPiece
import constants as c

from Pieces.Queen import Queen
from move import Move, Flag


class Pawn(AbstractPiece):
    def __init__(self, pieceColor, name="Pawn"):
        img = c.IMAGES["bp"] if pieceColor == c.Color.DARK else c.IMAGES["wp"]
        super().__init__(name, pieceColor, image=img)
        self.enpassant_able = False

    def __repr__(self):
        return AbstractPiece().__repr__().join(f" enpassant_able={self.enpassant_able}")

    def moveToSquare(self, square, board=None):
        if self.isFirstMove:
            sqr_rank = square.location.rank
            piece_rank = self.location.rank
            rank_diff = max(sqr_rank, piece_rank) - min(sqr_rank, piece_rank)
            if rank_diff > 1:
                self.enpassant_able = True
        else:
            self.enpassant_able = False

        # Check for promotion
        if square.location.rank in [1, 8]:
            # btn = Button("Queen", 200, 50, 100, 50)
            self.promote()
        self.forceMove(square)

    def promote(self, piece=Queen):
        """
        Method to promote current instance of `Pawn` to given piece

        :param piece: Callable class of piece to promote too.
        :type piece: Subclass of `AbstractPiece`
        default = Queen.
        """
        # Clean up required for sprite.GroupSingle
        # Store groups Pawn was in, and then kill itself.
        groups = self.groups()
        self.kill()
        square = self.square
        # Changing our class and initalising...
        self.__class__ = piece
        self.__init__(self.color)
        # Add new Piece to the previous pieces groups!
        self.add(groups)

        square.reset()
        self.square = square

    def getValidMoves(self, board):

        moveCandidates = []

        for move in self._getAllValidMoves(board):
            if not board.map.get(move):  # Loc not on board ie. at edge.
                continue
            # check enpassant
            if (
                move.file != self.square.file and not board.map.get(move).isOccupied
            ):  # Diagonal move but no capture
                continue
            if move.file == self.square.file and board.map.get(move).isOccupied:
                continue
            if move.file != self.square.file and board.map.get(move).isOccupied:
                if board.map.get(move).piece.color == self.color:
                    continue

            moveCandidates.append(move)

        for pos in [-1, 1]:
            enpassant_left = logic.build(self.location, pos, 0)
            square = board.map.get(enpassant_left)
            if not square:
                continue
            piece = square.piece
            if not piece:
                continue
            if piece.name == "pawn" and piece.color != self.color:
                if piece.enpassant_able:
                    enpassant_attack = logic.build(self.location, pos, 1)
                    enpassant_sqr = board.get(enpassant_attack)
                    moveCandidates.append(enpassant_attack)
                    move = Move(self.square, enpassant_sqr, flag=Flag.ENPASSANT)
                    moveCandidates.append(move)

        return moveCandidates

    def _getAllValidMoves(self, board):

        if self._pieceColor == c.Color.LIGHT:
            if self.isFirstMove:
                yield logic.build(self.location, fileOffset=0, rankOffset=2)

            yield logic.build(self.location, fileOffset=0, rankOffset=1)
            yield logic.build(self.location, fileOffset=1, rankOffset=1)
            yield logic.build(self.location, fileOffset=-1, rankOffset=1)

        else:
            if self.isFirstMove:
                yield logic.build(self.location, fileOffset=0, rankOffset=-2)

            yield logic.build(self.location, fileOffset=0, rankOffset=-1)
            yield logic.build(self.location, fileOffset=1, rankOffset=-1)
            yield logic.build(self.location, fileOffset=-1, rankOffset=-1)

    def getAttackMoves(self, board):
        """
        Get all attack moves for a pawn. Check for possible enpassant moves also.
        """

        if self._pieceColor == c.Color.LIGHT:
            move1 = logic.build(self.location, fileOffset=1, rankOffset=1)
            move2 = logic.build(self.location, fileOffset=-1, rankOffset=1)
            return [move1, move2]

        else:
            move1 = logic.build(self.location, fileOffset=1, rankOffset=-1)
            move2 = logic.build(self.location, fileOffset=-1, rankOffset=-1)
            return [move1, move2]
