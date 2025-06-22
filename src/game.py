import pygame
from src.entities.player import Player
from src.managers.enemy_manager import EnemyManager
from src.managers.game_state_manager import GameStateManager
from src.systems.render_system import RenderSystem
from src.utils.constants import PLAYER_SPEED, FPS, PLAYER_BASE_HP, PLAYER_X, PLAYER_Y


class Game:
    def __init__(self, screen, clock):
        self.screen = screen
        self.clock = clock

        self.state = GameStateManager(self.reset_game, quit)
        self.player = Player(PLAYER_X, PLAYER_Y, PLAYER_SPEED)
        self.enemy_manager = EnemyManager(self.player)
        self.render_system = RenderSystem()

        self.coin_img = pygame.image.load('assets/images/other/coin.png').convert_alpha()

    def update_menu_callbacks(self):
        self.state.menu._callbacks = [self.reset_game, quit]

    def reset_game(self):
        self.player.reset()
        self.enemy_manager = EnemyManager(self.player)
        self.state.reset_game()

    def run(self):
        while self.state.running:
            self.handle_events()
            self.update()
            self.draw()
            self.clock.tick(FPS)

    def handle_events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.state.running = False

            elif event.type == pygame.KEYDOWN:
                # кнопка атаки
                if self.state.gameplay and event.key == pygame.K_z and not self.player.is_attacking:
                    self.player.is_attacking = True
                    self.player.attack_frame = 0
                    self.player.last_attack_time = pygame.time.get_ticks()
                    self.player.sound_attack.play()

                if not self.state.gameplay:
                    self.state.handle_menu_events(event)

            if (event.type == getattr(self.enemy_manager, 'enemy_timer', None) and self.state.gameplay):
                self.enemy_manager.spawn_enemy()

    def update(self):
        if self.state.gameplay:
            self.player.update(pygame.key.get_pressed())
            self.enemy_manager.update()

            if not self.enemy_manager.handle_collisions(self.player):
                self.state.alive = False
                self.state.gameplay = False
                self.state.game_over()

    def draw(self):
        if self.state.gameplay:
            self.render_system.draw_background(self.screen, self.state.bg)
            self.render_system.draw_health_bar(self.screen, self.player.hp, PLAYER_BASE_HP)
            self.render_system.draw_coins(self.screen, self.coin_img, self.player.coins)
            self.render_system.draw_player(self.screen, self.player)
            self.render_system.draw_enemies(self.screen, self.enemy_manager.enemies)
        else:
            self.render_system.draw_menu(self.screen, self.state)

        pygame.display.flip()