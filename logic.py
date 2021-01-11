from Location import Location
from Files import Files, RANKS


def build(current, fileOffset, rankOffset):
    if not isinstance(current, Location):
        raise ValueError("Please pass current position as Location class")
    currentFile = current.file.value
    return Location(Files(currentFile + fileOffset),
                    current.rank + rankOffset)
