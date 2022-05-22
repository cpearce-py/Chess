from enum import Enum


class GameState(Enum):
    QUIT = -1
    TITLE = 0
    GAME = 1
    SETTINGS = 2
