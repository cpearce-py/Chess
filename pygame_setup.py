import pygame
from pygame.locals import *
from Pieces import Bishop
from Files import Color


pygame.init()

clock = pygame.time.Clock()

piece = Bishop(Color.LIGHT)


screen = pygame.display.set_mode((1000, 1000))

pieces_grp = pygame.sprite.Group()
pieces_grp.add(piece)

running = True
clicking = False

while running:

    screen.fill((255, 255, 255))

    pieces_grp.draw(screen)  


    mx, my = pygame.mouse.get_pos()
    # Button events
    for e in pygame.event.get():
        if e.type == QUIT:
            running = False
        if e.type == MOUSEBUTTONDOWN:
            if e.button == 1:
                clicking = True
                pieces_grp.update()
        
        if e.type == MOUSEBUTTONUP:
            if e.button == 1:
                clicking = False



    pygame.display.update()
    clock.tick(60)
