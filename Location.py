from Files import Files
from enum import Enum


class Location:
    """Base location class."""

    def __init__(self, file, rank):
        if not isinstance(file, Enum):
            raise ValueError("Please pass file arg as Files. Enum")
        self._file = file
        self._rank = rank

    def __repr__(self):
        return f'{self.__class__.__name__}(FILE={self._file.name}, RANK={self._rank})'

    def __eq__(self, other):
        return isinstance(other, Location) and other.file == self.file and other.rank == self.rank

    def __hash__(self):
        return hash((self._file, self._rank))

    @property
    def file(self):
        return self._file

    @property
    def rank(self):
        return self._rank
