import pygame
from Pieces import Bishop
from Files import Color


pygame.init()
clock = pygame.time.Clock()

piece = Bishop(Color.LIGHT)


screen = pygame.display.set_mode((1000, 1000))

pieces_grp = pygame.sprite.Group()
pieces_grp.add(piece)

running = True

while running:
    for e in pygame.event.get():
        if e.type == pygame.QUIT:
            running = False
        if e.type == pygame.MOUSEBUTTONDOWN:
            print(pygame.mouse.get_pos())
    pygame.display.flip()
    pieces_grp.draw(screen)
    clock.tick(60)
