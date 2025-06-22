import pygame
from src.utils.constants import FONT_NAME


class RenderSystem:
    def __init__(self):
        self.font = pygame.font.Font(FONT_NAME, 30)

    def draw_background(self, screen, background):
        screen.blit(background, (0, 0))

    def draw_health_bar(self, screen, player_hp, base_hp):
        # Параметры "сердечек"
        heart_width = 30
        heart_height = 30
        spacing = 10
        start_x = 20
        start_y = 20

        # Отрисовка
        for i in range(base_hp):
            x = start_x + i * (heart_width + spacing)
            color = (255, 0, 0) if i < player_hp else (100, 100, 100)
            pygame.draw.rect(screen, color, (x, start_y, heart_width, heart_height))
            pygame.draw.rect(screen, (0, 0, 0), (x, start_y, heart_width, heart_height), 2)

    def draw_coins(self, screen, coin_img, coins_count):
        coin_img = pygame.transform.scale(coin_img, (30, 40))
        start_x = 20
        start_y = 60
        screen.blit(coin_img, (start_x, start_y))
        text = self.font.render(f": {coins_count}", True, (255, 215, 0))
        screen.blit(text, (start_x + coin_img.get_width() + 5, start_y))

    def draw_player(self, screen, player):
        # Отрисовка атаки
        if player.is_attacking:
            if player.key_stay == 'stay_down':
                screen.blit(player.attack_down[player.attack_frame], (player.x, player.y))
            elif player.key_stay == 'stay_left':
                screen.blit(player.attack_left[player.attack_frame], (player.x - 45, player.y))
            elif player.key_stay == 'stay_right':
                screen.blit(player.attack_right[player.attack_frame], (player.x, player.y))
            elif player.key_stay == 'stay_up':
                screen.blit(player.attack_up[player.attack_frame], (player.x, player.y - 40))
        # Отрисовка ходьбы/стояния
        else:
            keys = pygame.key.get_pressed()
            if keys[pygame.K_LEFT]:
                screen.blit(player.walk_left[player.walk_count], (player.x, player.y))
            elif keys[pygame.K_RIGHT]:
                screen.blit(player.walk_right[player.walk_count], (player.x, player.y))
            elif keys[pygame.K_UP]:
                screen.blit(player.walk_up[player.walk_count], (player.x, player.y))
            elif keys[pygame.K_DOWN]:
                screen.blit(player.walk_down[player.walk_count], (player.x, player.y))
            else:
                screen.blit(player.stay[player.key_stay], (player.x, player.y))

    def draw_enemies(self, screen, enemies):
        for enemy in enemies:
            screen.blit(enemy.image, (enemy.x, enemy.y))

    def draw_menu(self, screen, state_manager):
        # Если не живой
        if not state_manager.alive:
            screen.blit(state_manager.bg_died, (0, 0))
            text = state_manager.menu.font.render('GAME OVER', True, (255, 0, 0))
        # Если живой
        else:
            screen.blit(state_manager.bg_start, (0, 0))
            text = state_manager.menu.font.render('MegaGame', True, (255, 0, 0))

        screen.blit(text, (350, 100))
        state_manager.menu.draw(screen, 100, 175, 75)