import pygame

WIDTH = HEIGHT = 500

WIN = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Client")

clientNumber = 0


class Player:
    def __init__(self, x, y, width, height, color):
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.color = color
        self.rect = (x, y, width, height)
        self.vel = 5

    def draw(self, win):
        pygame.draw.rect(win, self.color, self.rect)

    def move(self):
        keys = pygame.key.get_pressed()
        if keys[pygame.K_a]:
            self.x -= self.vel
        if keys[pygame.K_d]:
            self.x += self.vel
        if keys[pygame.K_w]:
            self.y -= self.vel
        if keys[pygame.K_s]:
            self.y += self.vel

        self.rect = (self.x, self.y, self.width, self.height)


def redraw_window(player):
    WIN.fill((255, 255, 255))
    player.draw()
    pygame.display.update()


def main():

    player = Player(50, 50, 100, 100, (0, 255, 0))
    clock = pygame.time.Clock()

    run = True

    while run:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                run = False

        player.move()

        WIN.fill((255, 255, 255))
        player.draw(WIN)
        pygame.display.update()
        clock.tick(60)


if __name__ == "__main__":
    main()
