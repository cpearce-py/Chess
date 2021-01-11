from Files import Files


class Location:
    """Base location class."""

    def __init__(self, file, rank):
        self._file = file
        self._rank = rank

    def __repr__(self):
        return f'{self.__class__.__name__}(FILE={self._file}, RANK={self._rank})'

    @property
    def file(self):
        return self._file

    @property
    def rank(self):
        return self._rank

    @property
    def pos(self):
        return [self._file, self._rank]
