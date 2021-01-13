import logic
from Files import Color
from Location import Location
from Squares import Square


class AbstractPiece:

    def __init__(self, name, pieceColor):
        self._name = name
        self._pieceColor = pieceColor
        self._square = None
        self._isFirstMove = True

    def __repr__(self):
        return (f'{self.__class__.__name__}({self._name}, {self._pieceColor},'
                f' {self._square})')

    @property
    def isFirstMove(self):
        return self._isFirstMove

    @isFirstMove.setter
    def isFirstMove(self, value):
        self._isFirstMove = value

    @property
    def name(self):
        return self._name

    @property
    def color(self):
        return self._pieceColor

    @property
    def square(self):
        """ Property for what Square the piece is on.
        Returns: Location(Enum.File, Rank)"""
        return self._square

    @square.setter
    def square(self, value):
        if not isinstance(value, Location):
            raise ValueError("Pass Square location as a Location class}")
        self._square = value

    def _getDiagonalCandidates(self, moves, _map,
                               current, rankOffset, fileOffset):
        """
        Method to append possible diagonal moves. type: `Location`
        Offset determines forward or backwards direction

        moves: type `list`

        """
        nextMove = logic.build(current, fileOffset, rankOffset)
        while _map.get(nextMove):
            if _map.get(nextMove).isOccupied:
                if _map.get(nextMove).currentPiece.color == self.color:
                    break
                moves.append(nextMove)
                break
            moves.append(nextMove)
            try:
                nextMove = logic.build(nextMove, fileOffset, rankOffset)
            except ValueError:
                break

    def _getFileCandidates(self, moves, _map, current, offset):
        """
        Method to append a position, type:`Location`, to given list.
        Offset determines forward or backwards direction from piece.

        moves: type `list`
        Yeild: Location
        """
        nextMove = logic.build(current, offset, rankOffset=0)
        while _map.get(nextMove):
            if _map.get(nextMove).isOccupied:
                if _map.get(nextMove).currentPiece.color == self.color:
                    break
                moves.append(nextMove)
                break
            moves.append(nextMove)
            try:
                nextMove = logic.build(nextMove, offset, rankOffset=0)
            except ValueError:
                break

    def _getRankCandidates(self, moves, _map, current, offset):
        """
        Method to append a position, type:`Location`, to given list.
        Offset determines forward or backwards direction from piece.

        moves: type `list`
        """
        nextMove = logic.build(current, 0, offset)
        while _map.get(nextMove):
            if _map.get(nextMove).isOccupied:
                if _map.get(nextMove).currentPiece.color == self.color:
                    break
                moves.append(nextMove)
                break
            moves.append(nextMove)
            try:
                nextMove = logic.build(nextMove, 0, offset)
            except ValueError:
                break
