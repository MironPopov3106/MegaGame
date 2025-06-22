from src.utils.constants import PLAYER_BASE_HP
import pygame


class Player:
    def __init__(self, x, y, speed):
        self.x = x
        self.y = y
        self.speed = speed
        self.hp = PLAYER_BASE_HP
        self.walk_count = 0
        self.coins = 0
        self.key_stay = 'stay_down'

        self.sound_attack = pygame.mixer.Sound('assets/sounds/attack.mp3')

        self.walk_left = [pygame.image.load(f'assets/images/player/walk/left_walk/left_{i}.png').convert_alpha() for i in range(1, 7)]
        self.walk_right = [pygame.image.load(f'assets/images/player/walk/right_walk/right_{i}.png').convert_alpha() for i in range(1, 7)]
        self.walk_down = [pygame.image.load(f'assets/images/player/walk/down_walk/down_{i}.png').convert_alpha() for i in range(1, 7)]
        self.walk_up = [pygame.image.load(f'assets/images/player/walk/up_walk/up_{i}.png').convert_alpha() for i in range(1, 7)]
        self.attack_left = [pygame.image.load(f'assets/images/player/attack/left_attack/left_attack_{i}.png').convert_alpha() for i in range(1, 6)]
        self.attack_down = [pygame.image.load(f'assets/images/player/attack/down_attack/down_attack_{i}.png').convert_alpha() for i in range(1, 6)]
        self.attack_right = [pygame.image.load(f'assets/images/player/attack/right_attack/right_attack_{i}.png').convert_alpha() for i in range(1, 6)]
        self.attack_up = [pygame.image.load(f'assets/images/player/attack/up_attack/up_attack_{i}.png').convert_alpha() for i in range(1, 6)]

        self.stay = {
            'stay_left': pygame.image.load('assets/images/player/walk/left_walk/left_stay.png').convert_alpha(),
            'stay_right': pygame.image.load('assets/images/player/walk/right_walk/right_stay.png').convert_alpha(),
            'stay_down': pygame.image.load('assets/images/player/walk/down_walk/down_stay.png').convert_alpha(),
            'stay_up': pygame.image.load('assets/images/player/walk/up_walk/up_stay.png').convert_alpha()
        }

        # Прямоугольники
        self.rect = self.walk_left[0].get_rect(topleft=(self.x, self.y))
        self.rect_attack = self.attack_left[1].get_rect(topleft=(self.x, self.y))

        # Параметры атаки
        self.is_attacking = False
        self.attack_frame = 0
        self.last_attack_time = 0
        self.attack_speed = 40

    def update(self, keys):
        if not self.is_attacking:
            # Вычисление направления игрока
            horizontal = keys[pygame.K_RIGHT] - keys[pygame.K_LEFT]
            vertical = keys[pygame.K_DOWN] - keys[pygame.K_UP]

            # Обновление позиции
            self.x += horizontal * self.speed
            self.y += vertical * self.speed
            self.rect = self.walk_left[0].get_rect(topleft=(self.x, self.y))

            # Ограничения ходьбы
            self.x = max(0, min(self.x, 900))
            self.y = max(150, min(self.y, 390))

            # Определение кадра анимации
            self.walk_count = (self.walk_count + 1) % 6

            # Определение направления и зоны атаки
            if horizontal or vertical:
                if keys[pygame.K_LEFT]:
                    self.key_stay = 'stay_left'
                    self.rect_attack = self.attack_left[1].get_rect(topleft=(self.x - 50, self.y))
                elif keys[pygame.K_RIGHT]:
                    self.key_stay = 'stay_right'
                    self.rect_attack = self.attack_left[1].get_rect(topleft=(self.x, self.y))
                elif keys[pygame.K_UP]:
                    self.key_stay = 'stay_up'
                    self.rect_attack = self.attack_left[1].get_rect(topleft=(self.x - 22, self.y - 32))
                elif keys[pygame.K_DOWN]:
                    self.key_stay = 'stay_down'
                    self.rect_attack = self.attack_left[1].get_rect(topleft=(self.x - 22, self.y + 25))

        # Атака
        else:
            current_time = pygame.time.get_ticks()
            if current_time - self.last_attack_time > self.attack_speed:
                self.attack_frame += 1
                self.last_attack_time = current_time
                if self.attack_frame >= len(self.attack_down):
                    self.is_attacking = False
                    self.attack_frame = 0

    def reset(self):
        self.x = 150
        self.y = 250
        self.coins = 0
        self.hp = PLAYER_BASE_HP
        self.walk_count = 0
        self.key_stay = 'stay_down'
        self.is_attacking = False
        self.attack_frame = 0
        self.last_attack_time = 0
        self.rect = self.walk_left[0].get_rect(topleft=(self.x, self.y))
        self.rect_attack = self.attack_left[1].get_rect(topleft=(self.x, self.y))