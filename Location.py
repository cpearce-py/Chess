class Location():
    """Base location class."""

    def __init__(self, file, rank):
        self._file = file
        self._rank = rank

    def __repr__(self):
        return f'Location({self._file},{self._rank})'

    @property
    def file(self):
        return self._file

    @property
    def rank(self):
        return self._rank
