from Location import Location
from Files import Files, RANKS, Color

def build(current, fileOffset, rankOffset):
    """
    Generates a new Location class for where a given Location will end up
    based on a given file and rank offset.

    current: Location(Files.FILES, int Rank})
    fileOffset: Int
    rankOffset: Int

    returns: Location()
    """
    if not isinstance(current, Location):
        raise ValueError("Please pass current position as Location class")
    currentFile = current.file.value

    # To avoid Enums ValueError if file not located.
    try:
        return Location(Files(currentFile + fileOffset),
                        current.rank + rankOffset)
    except ValueError:
        return None
