from Board import Board


class Game():

    def __init__(self):
        self._board = Board()

    @property
    def board(self):
        return self._board


game = Game()
print(game.board)
