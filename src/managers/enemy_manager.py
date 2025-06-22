import pygame
import random
from src.entities.enemy import Enemy
from src.utils.constants import ENEMY_TIMER, SCREEN_WIDTH, SCREEN_HEIGHT


class EnemyManager:
    def __init__(self, player):
        self.enemies = []
        self.player = player
        self.enemy_timer = pygame.USEREVENT + 1
        pygame.time.set_timer(self.enemy_timer, ENEMY_TIMER)
        self.min_spawn_distance = 150
        self.sound_hit_player = pygame.mixer.Sound('assets/sounds/hit_player.mp3')

    def spawn_enemy(self):
        # поиск безопасных зон
        spawn_zones = self._get_spawn_zones()

        # Выбор зоны
        zone = random.choice(spawn_zones)
        spawn_x = random.randint(zone["left"], zone["right"])
        spawn_y = random.randint(zone["top"], zone["bottom"])

        # Создаём врага
        enemy = Enemy(random.choice(['ghost', 'zombie']), spawn_x, spawn_y, self.player)
        self.enemies.append(enemy)

    def _get_spawn_zones(self):
        zones = []
        player_rect = pygame.Rect(
            self.player.x - self.min_spawn_distance,
            self.player.y - self.min_spawn_distance,
            self.min_spawn_distance * 2,
            self.min_spawn_distance * 2
        )

        # Зона слева от игрока
        if player_rect.left > 0:
            zones.append({
                "left": 0,
                "top": 0,
                "right": player_rect.left,
                "bottom": SCREEN_HEIGHT
            })

        # Зона справа
        if player_rect.right < SCREEN_WIDTH:
            zones.append({
                "left": player_rect.right,
                "top": 0,
                "right": SCREEN_WIDTH,
                "bottom": SCREEN_HEIGHT
            })

        # Зона сверху
        if player_rect.top > 0:
            zones.append({
                "left": 0,
                "top": 0,
                "right": SCREEN_WIDTH,
                "bottom": player_rect.top
            })

        # Зона снизу
        if player_rect.bottom < SCREEN_HEIGHT:
            zones.append({
                "left": 0,
                "top": player_rect.bottom,
                "right": SCREEN_WIDTH,
                "bottom": SCREEN_HEIGHT
            })

        return zones

    def update(self):
        for enemy in self.enemies:
            enemy.update()

    def handle_collisions(self, player):
        for enemy in self.enemies[:]:
            # Атака игрока
            if player.rect_attack.colliderect(enemy.rect) and player.is_attacking:
                self.enemies.remove(enemy)
                player.coins += 1

            # Атака врага
            elif player.rect.colliderect(enemy.rect) and not player.is_attacking:
                player.hp -= enemy.damage
                self.enemies.remove(enemy)
                self.sound_hit_player.play()

                if player.hp <= 0:
                    return False
        return True