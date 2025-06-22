import pygame
from src.utils.constants import FONT_NAME, FONT_SIZE


class Menu:
    def __init__(self):
        self._option_surfaces = []
        self._callbacks = []
        self._current_option_index = 0
        self.font = pygame.font.Font(FONT_NAME, FONT_SIZE)

    def append_option(self, option, callback):
        self._option_surfaces.append(self.font.render(option, True, (102, 50, 168)))
        self._callbacks.append(callback)

    def switch(self, direction):
        self._current_option_index = max(0, min(self._current_option_index + direction, len(self._option_surfaces) - 1))

    def select(self):
        self._callbacks[self._current_option_index]()

    def draw(self, surf, x, y, option_y_padding):
        for i, option in enumerate(self._option_surfaces):
            option_rect = option.get_rect()
            option_rect.topleft = (x, y + i * option_y_padding)
            if i == self._current_option_index:
                pygame.draw.rect(surf, (35, 200, 110), option_rect)
            surf.blit(option, option_rect)