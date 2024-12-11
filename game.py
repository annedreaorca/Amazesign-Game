import pygame
from menu import *

class Game:
    def __init__(self):
        pygame.init()
        pygame.mixer.init()

        self.running, self.playing = True, False
        self.UP_KEY, self.DOWN_KEY, self.START_KEY, self.BACK_KEY = False, False, False, False

        self.DISPLAY_W, self.DISPLAY_H = pygame.display.Info().current_w, pygame.display.Info().current_h

        self.window_caption = "AMAZESIGN"
        self.window = pygame.display.set_mode((self.DISPLAY_W, self.DISPLAY_H), pygame.FULLSCREEN)
        pygame.display.set_caption(self.window_caption)

        self.display = pygame.Surface((self.DISPLAY_W, self.DISPLAY_H))

        self.font_name = 'assets/fonts/Square Game.otf'
        self.BLACK, self.WHITE = (0, 0, 0), (255, 255, 255)

        self.button_sfx = pygame.mixer.Sound("assets/sfx/button-sfx.mp3")
        pygame.mixer.music.load("assets/musics/bg-main-music.mp3")
        pygame.mixer.music.set_volume(0.5)
        pygame.mixer.music.play(loops=-1, start=0.0)

        self.main_menu = MainMenu(self)
        self.curr_menu = self.main_menu

    def check_events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.running, self.playing = False, False
                self.curr_menu.run_display = False
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_RETURN:
                    self.START_KEY = True
                if event.key == pygame.K_BACKSPACE:
                    self.BACK_KEY = True
                if event.key == pygame.K_DOWN:
                    self.DOWN_KEY = True
                if event.key == pygame.K_UP:
                    self.UP_KEY = True

    def reset_keys(self):
        self.UP_KEY, self.DOWN_KEY, self.START_KEY, self.BACK_KEY = False, False, False, False

    def draw_text(self, text, size, x, y):
        font = pygame.font.Font(self.font_name, size)
        text_surface = font.render(text, True, self.WHITE)
        text_rect = text_surface.get_rect()
        text_rect.center = (x, y)
        self.display.blit(text_surface, text_rect)

    def play_sound(self, sound):
        """Play a sound effect."""
        sound.play()

    def game_loop(self):
        while self.playing:
            self.check_events()
            self.display.fill(self.BLACK)
            self.window.blit(self.display, (0, 0)) 
            pygame.display.update()
            self.reset_keys()
