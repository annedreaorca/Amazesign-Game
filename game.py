import pygame
from menu import *

class Game():
    def __init__(self):
        pygame.init()
        pygame.mixer.init()  # Initialize the mixer for sound effects

        # General game states
        self.running, self.playing = True, False
        self.UP_KEY, self.DOWN_KEY, self.START_KEY, self.BACK_KEY = False, False, False, False

        # Display settings
        self.DISPLAY_W, self.DISPLAY_H = 1280, 720
        self.window_caption = "AMAZESIGN"  # Window caption
        self.display = pygame.Surface((self.DISPLAY_W, self.DISPLAY_H))  # Off-screen rendering
        self.window = pygame.display.set_mode((self.DISPLAY_W, self.DISPLAY_H))  # Main game window
        pygame.display.set_caption(self.window_caption)

        # Fonts and colors
        self.font_name = 'assets/fonts/KARNIBLA-black.ttf'
        self.BLACK, self.WHITE = (0, 0, 0), (255, 255, 255)

        # Load sound effects
        self.button_sfx = pygame.mixer.Sound("assets/sfx/button-sfx.mp3")

        # Load and play background music
        pygame.mixer.music.load("assets/musics/bg-main-music.mp3")
        pygame.mixer.music.set_volume(0.5)  # Set volume (0.0 to 1.0)
        pygame.mixer.music.play(loops=-1, start=0.0)  # Play the music in a loop (-1 means loop forever)

        self.main_menu = MainMenu(self)
        self.options = OptionsMenu(self)
        self.credits = CreditsMenu(self)
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