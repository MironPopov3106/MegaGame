from src.utils.constants import ENEMY_SPEED, ENEMY_DAMAGE
import pygame
import math


class Enemy:
    def __init__(self, mob, x, y, player):
        self.image_left = pygame.image.load(f'assets/images/mobs/{mob}.png').convert_alpha()
        self.image_right = pygame.transform.flip(self.image_left, True, False)
        self.direction_x = 0

        self.image = self.image_left
        self.rect = self.image_left.get_rect(topleft=(x, y))

        self.speed = ENEMY_SPEED
        self.x = x
        self.y = y
        self.player = player
        self.damage = ENEMY_DAMAGE
        self.direction = self.calculate_direction()

    def calculate_direction(self):
        # Вычисление направления
        dx = self.player.x - self.x
        dy = self.player.y - self.y
        distance = math.hypot(dx, dy)
        return (dx / distance, dy / distance)

    def update(self):
        # Обновление направления
        self.direction = self.calculate_direction()

        # Определяем направление по X
        if self.direction[0] > 0:
            new_direction_x = 1
        else:
            new_direction_x = -1

        # Если направление изменилось, обновляем изображение
        if new_direction_x != self.direction_x:
            self.direction_x = new_direction_x
            self.image = self.image_right if self.direction_x > 0 else self.image_left

        # Обновление позиции
        self.x += self.direction[0] * self.speed
        self.y += self.direction[1] * self.speed

        self.rect.x = self.x
        self.rect.y = self.y