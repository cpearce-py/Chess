class Player:
    def __init__(self, is_white, board):
        self.is_white: bool = is_white
        self.board = board
        self.pieces = self.board.pieces(self.color)
        self._king = [x for x in self.pieces if x.name == "king"][0]

    @property
    def king(self):
        return self._king

    def check_king(self):
        print(self.king)

    @property
    def is_white(self):
        return self.is_white
