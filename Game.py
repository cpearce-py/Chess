import pygame

from constants import HEIGHT, WIDTH, FPS
from scenes.scenes import Menu, GameScene


def play_game(starting_scene, WIDTH=512, HEIGHT=512, fps=60):

    pygame.init()
    screen = pygame.display.set_mode((WIDTH, HEIGHT))
    clock = pygame.time.Clock()

    active_scene = starting_scene()

    # Overall game loop
    while active_scene:

        # Handle event
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                return
            active_scene.process_input(event)

        # Update scene states
        active_scene.update()

        # Render states to screen
        active_scene.render(screen)
    
        # Move onto next scene, when ready.
        active_scene = active_scene.next

        # Flip display and tick clock.
        pygame.display.flip()
        clock.tick(fps)

if __name__ == '__main__':
    game = play_game(GameScene, WIDTH, HEIGHT, FPS)
