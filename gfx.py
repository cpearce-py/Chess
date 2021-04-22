import pygame

class GFX:
    def __init__(self):
        self.board = pygame.sprite.Group()
        self.pieces = pygame.sprite.Group()
        self.selected = pygame.sprite.Group()
        self.dead = pygame.sprite.Group()
        self.layers = [self.board,
                       self.pieces,
                       self.selected,
                       self.dead]

    def update(self):
        for layer in self.layers:
            layer.update()

    def render(self, surface):
        for layer in sef.layers:
            layer.draw(surface)
