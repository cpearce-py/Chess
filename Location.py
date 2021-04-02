from Files import Files
from enum import Enum


class Location:
    """Base Location class."""

    def __init__(self, file, rank):
        if not isinstance(file, Enum):
            raise ValueError("Please pass file arg as Files. Enum")
        self._file = file
        self._rank = rank
        self._square = None

    def __repr__(self):
        return (f'{self.__class__.__name__}(FILE={self._file.name}, '
                f'RANK={self._rank})')

    def __eq__(self, other):
        """
        Compare with Location.
        :param other: Instance of :class:`Location`
        """
        return (isinstance(other, Location) and
                other.file == self.file and other.rank == self.rank)

    def __hash__(self):
        """Compute hash for location"""
        return hash((self._file, self._rank))

    @property
    def square(self):
        return self._square

    @square.setter
    def square(self, value):
        self._square = value

    @property
    def file(self):
        return self._file

    @property
    def rank(self):
        return self._rank

    def nextRank(self, direction):
        curRank = Files.RANKS.index(self.rank)
        newRank = Files.RANKS[curRank + direction]
        return Location(self.file, newRank)

    def nextRankUp(self):
        self.nextRank(1)

    def nextRankDown(self):
        self.nextRank(-1)
