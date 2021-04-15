import pygame
from ui import Button

WHITE = (255, 255, 255)
BLACK = (0, 0, 0)

SCREEN_WIDTH  = 600
SCREEN_HEIGHT = 400

pygame.init()

screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
screen_rect = screen.get_rect()

clock = pygame.time.Clock()
is_running = False

btn1 = Button('Hello', 200, 50, 100, 50)

is_running = True

while is_running:

    for event in pygame.event.get():

        if event.type == pygame.QUIT:
            is_running = False
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                is_running = False

        btn1.handle_event(event)

    btn1.update()

    screen.fill(BLACK)

    btn1.draw(screen)

    pygame.display.update()

    clock.tick(25)

pygame.quit()
