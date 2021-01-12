from Location import Location
from Files import Files, RANKS


def build(current, fileOffset, rankOffset):
    """
    Generates a new Location class for where a given Location will end up
    based on a given file and rank offset.
    """
    if not isinstance(current, Location):
        raise ValueError("Please pass current position as Location class")
    currentFile = current.file.value
    newFile = currentFile + fileOffset
    newRank = current.rank + rankOffset
    if newFile == 0:
        return None
    else:
        return Location(Files(currentFile + fileOffset),
                        current.rank + rankOffset)