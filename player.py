from ui.gamestates import GameState

class Player:
    def __init__(self, color, board):
        self.color = color
        self.board = board
        self.pieces = self.board.get_pieces_coloured(self.color)
        self._king = [x for x in self.pieces if x.name == 'king'][0]

    @property
    def king(self):
        return self._king

    def check_king(self):
        print(self.king)
