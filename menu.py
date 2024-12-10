import pygame

class Menu():
    def __init__(self, game):
        self.game = game
        self.mid_w, self.mid_h = self.game.DISPLAY_W / 2, self.game.DISPLAY_H / 2
        self.run_display = True
        self.cursor_rect = pygame.Rect(0, 0, 20, 20)  # Cursor rectangle for selection
        self.offset = -150  # Horizontal offset for cursor alignment

    def draw_cursor(self):
        self.game.draw_text('>', 40, self.cursor_rect.x, self.cursor_rect.y)

    def blit_screen(self):
        self.game.window.blit(self.game.display, (0, 0))
        pygame.display.update()
        self.game.reset_keys()

class MainMenu(Menu):
    def __init__(self, game):
        super().__init__(game)
        self.state = "Start"
        self.startx, self.starty = self.mid_w, self.mid_h + 20
        self.optionsx, self.optionsy = self.mid_w, self.mid_h + 70
        self.creditsx, self.creditsy = self.mid_w, self.mid_h + 120
        self.cursor_rect.midtop = (self.startx + self.offset, self.starty)

        try:
            self.background = pygame.image.load("assets/backgrounds/main-background-menu.jpg")
            self.background = pygame.transform.scale(self.background, (self.game.DISPLAY_W, self.game.DISPLAY_H))
        except pygame.error as e:
            print(f"Error loading background image: {e}")
            self.background = pygame.Surface((self.game.DISPLAY_W, self.game.DISPLAY_H))  # Placeholder background

    def display_menu(self):
        self.run_display = True
        while self.run_display:
            self.game.check_events()
            self.check_input()
            self.game.display.blit(self.background, (0, 0))
            self.game.draw_text('AMAZESIGN', 50, self.mid_w, self.mid_h - 100)
            self.game.draw_text("Start Game", 40, self.startx, self.starty)
            self.game.draw_text("Options", 40, self.optionsx, self.optionsy)
            self.game.draw_text("Credits", 40, self.creditsx, self.creditsy)
            self.draw_cursor()
            self.blit_screen()

    def move_cursor(self):
        if self.game.DOWN_KEY:
            self.game.play_sound(self.game.button_sfx)
            if self.state == 'Start':
                self.cursor_rect.midtop = (self.optionsx + self.offset, self.optionsy)
                self.state = 'Options'
            elif self.state == 'Options':
                self.cursor_rect.midtop = (self.creditsx + self.offset, self.creditsy)
                self.state = 'Credits'
            elif self.state == 'Credits':
                self.cursor_rect.midtop = (self.startx + self.offset, self.starty)
                self.state = 'Start'
        elif self.game.UP_KEY:
            self.game.play_sound(self.game.button_sfx)
            if self.state == 'Start':
                self.cursor_rect.midtop = (self.creditsx + self.offset, self.creditsy)
                self.state = 'Credits'
            elif self.state == 'Options':
                self.cursor_rect.midtop = (self.startx + self.offset, self.starty)
                self.state = 'Start'
            elif self.state == 'Credits':
                self.cursor_rect.midtop = (self.optionsx + self.offset, self.optionsy)
                self.state = 'Options'

    def check_input(self):
        self.move_cursor()
        if self.game.START_KEY:
            self.game.play_sound(self.game.button_sfx)
            if self.state == 'Start':
                self.game.playing = True
            elif self.state == 'Options':
                self.game.curr_menu = self.game.options
            elif self.state == 'Credits':
                self.game.curr_menu = self.game.credits
            self.run_display = False

class OptionsMenu(Menu):
    def __init__(self, game):
        super().__init__(game)
        self.state = 'Volume'
        self.volx, self.voly = self.mid_w, self.mid_h + 20
        self.controlsx, self.controlsy = self.mid_w, self.mid_h + 50
        self.cursor_rect.midtop = (self.volx + self.offset, self.voly)

        try:
            self.background = pygame.image.load("assets/backgrounds/front-bg-game.jpeg")
            self.background = pygame.transform.scale(self.background, (self.game.DISPLAY_W, self.game.DISPLAY_H))
        except pygame.error as e:
            print(f"Error loading background image: {e}")
            self.background = pygame.Surface((self.game.DISPLAY_W, self.game.DISPLAY_H))  # Placeholder background

    def display_menu(self):
        self.run_display = True
        while self.run_display:
            self.game.check_events()
            self.check_input()
            self.game.display.blit(self.background, (0, 0))
            self.game.draw_text('Options', 40, self.mid_w, self.mid_h - 40)
            self.game.draw_text("Volume", 30, self.volx, self.voly)
            self.game.draw_text("Controls", 30, self.controlsx, self.controlsy)
            self.draw_cursor()
            self.blit_screen()

    def move_cursor(self):
        if self.game.DOWN_KEY:
            self.game.play_sound(self.game.button_sfx)
            if self.state == 'Volume':
                self.state = 'Controls'
                self.cursor_rect.midtop = (self.controlsx + self.offset, self.controlsy)
            elif self.state == 'Controls':
                self.state = 'Volume'
                self.cursor_rect.midtop = (self.volx + self.offset, self.voly)
        elif self.game.UP_KEY:
            self.game.play_sound(self.game.button_sfx)
            if self.state == 'Volume':
                self.state = 'Controls'
                self.cursor_rect.midtop = (self.controlsx + self.offset, self.controlsy)
            elif self.state == 'Controls':
                self.state = 'Volume'
                self.cursor_rect.midtop = (self.volx + self.offset, self.voly)

    def check_input(self):
        self.move_cursor()
        if self.game.START_KEY or self.game.BACK_KEY:
            self.game.play_sound(self.game.button_sfx)
            self.game.curr_menu = self.game.main_menu
            self.run_display = False

class CreditsMenu(Menu):
    def __init__(self, game):
        super().__init__(game)

        try:
            self.background = pygame.image.load("assets/backgrounds/front-bg-game.jpeg")
            self.background = pygame.transform.scale(self.background, (self.game.DISPLAY_W, self.game.DISPLAY_H))
        except pygame.error as e:
            print(f"Error loading background image: {e}")
            self.background = pygame.Surface((self.game.DISPLAY_W, self.game.DISPLAY_H))  # Placeholder background

    def display_menu(self):
        self.run_display = True
        while self.run_display:
            self.game.check_events()
            if self.game.START_KEY or self.game.BACK_KEY:
                self.game.play_sound(self.game.button_sfx)
                self.game.curr_menu = self.game.main_menu
                self.run_display = False
            self.game.display.blit(self.background, (0, 0))
            self.game.draw_text('Credits', 40, self.mid_w, self.mid_h - 20)
            self.game.draw_text('Made by me', 30, self.mid_w, self.mid_h + 20)
            self.blit_screen()
