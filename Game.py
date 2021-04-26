import pygame
from pygame.locals import *
from Pieces import Bishop
from constants import Color, WIDTH, HEIGHT
from Board import Board
from events.event_handler import EventHandler

class Game:

    def __init__(self, WIDTH=512, HEIGHT=512):
        self.clock = pygame.time.Clock()
        self.screen = pygame.display.set_mode(
            (WIDTH, HEIGHT), pygame.RESIZABLE)
        self.board = Board()
        self.running = False
        self.event_handler = EventHandler(self.board)

    def play(self):

        pygame.init()
        self.running = True

        screen = self.screen
        board = self.board

        while self.running:

            # Clock tick
            self.clock.tick(60)

            # Handle Events
            for event in pygame.event.get():
                self.event_handler.handle_events(event)

            # Update States
            self.board.update()

            # Render States
            screen.fill((0,0,0))
            self.board.draw(screen)

            pygame.display.update()

if __name__ == '__main__':
    game = Game()
    game.play()
