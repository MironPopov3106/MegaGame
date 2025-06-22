import pygame
from src.utils.menu import Menu
from src.utils.constants import MUSIC_VOLUME, SFX_VOLUME


class GameStateManager:
    def __init__(self, reset_callback, quit_callback):
        self.running = True
        self.gameplay = False
        self.alive = True

        self.reset_callback = reset_callback
        self.quit_callback = quit_callback
        self.menu = self.create_menu()

        self.bg = pygame.image.load('assets/images/backgrounds/background_1.jpg').convert()
        self.bg_died = pygame.image.load('assets/images/backgrounds/background_died.jpg').convert()
        self.bg_start = pygame.image.load('assets/images/backgrounds/background_start.jpg').convert()

        # Загрузка звуков
        pygame.mixer.music.load('assets/sounds/bg_sound.mp3')
        self.sound_option_switch = pygame.mixer.Sound('assets/sounds/options.mp3')
        self.sound_option_select = pygame.mixer.Sound('assets/sounds/select_option.mp3')
        self.sound_game_over = pygame.mixer.Sound('assets/sounds/game_over.mp3')

        # Начальная громкость
        self.music_volume = MUSIC_VOLUME
        self.sfx_volume = SFX_VOLUME
        pygame.mixer.music.set_volume(self.music_volume)
        self.sound_option_switch.set_volume(self.sfx_volume)
        self.sound_option_select.set_volume(self.sfx_volume)
        self.sound_game_over.set_volume(self.sfx_volume)

        pygame.mixer.music.play(-1)

    def create_menu(self):
        menu = Menu()
        # Меню смерти
        if not self.alive:
            menu.append_option('Restart', self.reset_callback)
            menu.append_option('Quit', self.quit_callback)
        # Начальное меню
        else:
            menu.append_option('Start game', self.reset_callback)
            menu.append_option('Quit', self.quit_callback)
        return menu

    def reset_game(self):
        self.gameplay = True
        self.alive = True
        self.menu = self.create_menu()
        pygame.mixer.music.play(-1)

    def handle_menu_events(self, event):
        # Управление меню
        if event.key == pygame.K_UP:
            self.menu.switch(-1)
            self.sound_option_switch.play()
        elif event.key == pygame.K_DOWN:
            self.menu.switch(1)
            self.sound_option_switch.play()
        elif event.key == pygame.K_z:
            self.menu.select()
            self.sound_option_select.play()

    def game_over(self):
        pygame.mixer.music.stop()
        self.sound_game_over.play()
        self.menu = self.create_menu()