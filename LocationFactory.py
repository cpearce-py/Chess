from Location import Location
from Files import Files, RANKS


class LocationFactory:

    @staticmethod
    def build(current, fileOffset, rankOffset):
        if not isinstance(current, Location):
            raise ValueError("Please pass current position as Location class")
        currentFile = current.file
        return Location(Files(currentFile + fileOffset).name,
                        current.rank + rankOffset)
