from src.utils.constants import SCREEN_WIDTH, SCREEN_HEIGHT
import pygame
from src.game import Game


def main():
    pygame.init()
    screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
    pygame.display.set_caption('MegaGame')

    icon = pygame.image.load('assets/images/other/icon.png').convert_alpha()
    pygame.display.set_icon(icon)

    clock = pygame.time.Clock()
    game = Game(screen, clock)
    game.run()


if __name__ == "__main__":
    main()
    pygame.quit()