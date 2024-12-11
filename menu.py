import pygame
from ffpyplayer.player import MediaPlayer
import time  # Import time for frame timing control

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
        self.startx, self.starty = self.mid_w, self.mid_h + -20
        self.howtoplayx, self.howtoplayy = self.mid_w, self.mid_h + 100
        self.quitx, self.quity = self.mid_w, self.mid_h + 220
        self.cursor_rect.midtop = (self.startx + self.offset, self.starty)

        # Initialize video player
        self.video_path = "assets/backgrounds/game-background-menu.mp4"
        self.video_player = MediaPlayer(self.video_path)
        self.frame = None

        # Control video playback speed
        self.playback_speed = 1.0
        self.last_frame_time = 0

        # Load the logo image
        self.logo = pygame.image.load("assets/amazesign-logo.png")
        self.logo = pygame.transform.scale(self.logo, (350, 150))

    def display_menu(self):
        self.run_display = True
        while self.run_display:
            self.game.check_events()
            self.check_input()

            # Retrieve and display video frame
            current_time = time.time()
            if current_time - self.last_frame_time >= (1 / 30) / self.playback_speed:  # Adjust frame rate
                self.get_video_frame()
                self.last_frame_time = current_time

            if self.frame is not None:
                video_surface = pygame.image.frombuffer(
                    self.frame.to_bytearray()[0],
                    self.frame.get_size(),
                    "RGB"
                )

                # Scale the video surface to fit the full screen
                video_surface = pygame.transform.scale(video_surface, (self.game.DISPLAY_W, self.game.DISPLAY_H))

                # Draw the video surface
                self.game.display.blit(video_surface, (0, 0))

            # Draw the logo
            logo_x = self.mid_w - self.logo.get_width() / 2
            logo_y = 100
            self.game.display.blit(self.logo, (logo_x, logo_y))

            # Draw menu buttons
            self.draw_button("Start Game", self.startx, self.starty, self.state == "Start")
            self.draw_button("How to Play", self.howtoplayx, self.howtoplayy, self.state == "How to Play")
            self.draw_button("Quit", self.quitx, self.quity, self.state == "Quit")
            self.blit_screen()

    def get_video_frame(self):
        """Retrieve the next frame from the video."""
        frame, val = self.video_player.get_frame()
        if frame:
            self.frame = frame[0]
        if val == 'eof':  # Loop the video when it ends
            self.video_player = MediaPlayer(self.video_path)

    def draw_button(self, text, x, y, is_selected):
        """Draw a button with a styled appearance."""
        font = pygame.font.Font(self.game.font_name, 40)
        text_surface = font.render(text, True, self.game.WHITE)

        # Define padding inside the button
        padding_x = 40
        padding_y = 20

        # Calculate button dimensions
        text_width, text_height = text_surface.get_size()
        button_width = text_width + 2 * padding_x
        button_height = text_height + 2 * padding_y
        button_x = x - button_width // 2
        button_y = y - button_height // 2

        # Draw the button background
        surface = pygame.Surface((button_width, button_height), pygame.SRCALPHA)
        bg_color = (204, 204, 204, 230) if is_selected else (11, 0, 16, 230)
        pygame.draw.rect(surface, bg_color, (0, 0, button_width, button_height), border_radius=50)
        pygame.draw.rect(surface, (204, 204, 204), (0, 0, button_width, button_height), width=1, border_radius=50)
        self.game.display.blit(surface, (button_x, button_y))

        # Draw the button text
        text_x = button_x + padding_x
        text_y = button_y + padding_y
        self.game.display.blit(text_surface, (text_x, text_y))

    def move_cursor(self):
        if self.game.DOWN_KEY:
            self.game.play_sound(self.game.button_sfx)
            if self.state == 'Start':
                self.state = 'How to Play'
                self.cursor_rect.midtop = (self.howtoplayx + self.offset, self.howtoplayy)
            elif self.state == 'How to Play':
                self.state = 'Quit'
                self.cursor_rect.midtop = (self.quitx + self.offset, self.quity)
            elif self.state == 'Quit':
                self.state = 'Start'
                self.cursor_rect.midtop = (self.startx + self.offset, self.starty)

        elif self.game.UP_KEY:
            self.game.play_sound(self.game.button_sfx)
            if self.state == 'Start':
                self.state = 'Quit'
                self.cursor_rect.midtop = (self.quitx + self.offset, self.quity)
            elif self.state == 'How to Play':
                self.state = 'Start'
                self.cursor_rect.midtop = (self.startx + self.offset, self.starty)
            elif self.state == 'Quit':
                self.state = 'How to Play'
                self.cursor_rect.midtop = (self.howtoplayx + self.offset, self.howtoplayy)

    def check_input(self):
        self.move_cursor()
        if self.game.START_KEY:
            self.game.play_sound(self.game.button_sfx)
            if self.state == 'Start':
                self.game.playing = True
                self.run_display = False
            elif self.state == 'How to Play':
                self.game.curr_menu = HowToPlayMenu(self.game)
                self.run_display = False
            elif self.state == 'Quit':
                pygame.quit()
                exit()

class HowToPlayMenu(Menu):
    def __init__(self, game):
        super().__init__(game)
        self.state = "HowToPlay"
        self.instructions = [
            "How to Play",
            "Thumbs Up - Move Up",
            "Thumbs Down - Move Down",
            "Closed Fist - Move Right",
            "Open Palm - Move Left",
            "I Love You (ASL) - Reset Position",
        ]

        # Initialize video player
        self.video_path = "assets/backgrounds/game-background-menu.mp4"
        self.video_player = MediaPlayer(self.video_path)
        self.frame = None

        # Control video playback speed
        self.playback_speed = 1.0
        self.last_frame_time = 0

        # Load the logo image
        self.logo = pygame.image.load("assets/amazesign-logo.png")
        self.logo = pygame.transform.scale(self.logo, (350, 150))

    def set_playback_speed(self, speed):
        """Set the playback speed for the video."""
        self.playback_speed = speed

    def display_menu(self):
        self.run_display = True
        while self.run_display:
            self.game.check_events()
            self.check_input()

            # Retrieve and display video frame
            current_time = time.time()
            if current_time - self.last_frame_time >= (1 / 30) / self.playback_speed:  # Adjust frame rate
                self.get_video_frame()
                self.last_frame_time = current_time

            if self.frame is not None:
                video_surface = pygame.image.frombuffer(
                    self.frame.to_bytearray()[0],
                    self.frame.get_size(),
                    "RGB"
                )

                # Scale the video surface to fit the full screen
                video_surface = pygame.transform.scale(video_surface, (self.game.DISPLAY_W, self.game.DISPLAY_H))

                # Draw the video surface
                self.game.display.blit(video_surface, (0, 0))

            # Draw the logo
            logo_x = self.mid_w - self.logo.get_width() / 2
            logo_y = 100
            self.game.display.blit(self.logo, (logo_x, logo_y))

            # Draw the instructions box and button
            self.draw_instructions()
            self.blit_screen()

    def get_video_frame(self):
        """Retrieve the next frame from the video."""
        frame, val = self.video_player.get_frame()
        if frame:
            self.frame = frame[0]
        if val == 'eof':  # Loop the video when it ends
            self.video_player = MediaPlayer(self.video_path)

    def check_input(self):
        keys = pygame.key.get_pressed()

        # Check for Enter or Backspace to return to Main Menu
        if keys[pygame.K_RETURN] or keys[pygame.K_BACKSPACE]:
            self.game.play_sound(self.game.button_sfx)
            self.game.curr_menu = MainMenu(self.game)  # Switch to Main Menu
            self.run_display = False  # Exit the current menu


    def draw_instructions(self):
        """Draw instructions text with a dynamically sized semi-transparent background."""
        text_gap = 50  # Vertical space between lines
        title_gap = 30  # Extra gap between the title and the instructions
        padding_x = 40  # Horizontal padding inside the box
        padding_y = 30  # Vertical padding inside the box
        button_gap = 40  # Gap between the instructions box and the button

        # Calculate the dimensions of the content
        font = pygame.font.Font(self.game.font_name, 40)
        max_text_width = max(font.size(line)[0] for line in self.instructions)
        total_height = (len(self.instructions) - 1) * text_gap + title_gap + font.size(self.instructions[0])[1]

        # Set box dimensions
        box_width = max_text_width + 2 * padding_x
        box_height = total_height + 2 * padding_y
        box_x = self.mid_w - box_width // 2
        box_y = self.mid_h - box_height // 2

        # Draw background box with rounded corners
        surface = pygame.Surface((box_width, box_height), pygame.SRCALPHA)
        pygame.draw.rect(surface, (11, 0, 16, 192), (0, 0, box_width, box_height), border_radius=20)
        self.game.display.blit(surface, (box_x, box_y))

        # Draw the instructions text
        start_y = box_y + padding_y
        for i, line in enumerate(self.instructions):
            size = 50 if i == 0 else 40  # Larger font for the title
            text_surface = font.render(line, True, self.game.WHITE)
            text_x = self.mid_w - text_surface.get_width() // 2

            # Add title gap after the first line
            if i == 0:
                text_y = start_y
            else:
                text_y = start_y + font.size(self.instructions[0])[1] + title_gap + (i - 1) * text_gap

            self.game.display.blit(text_surface, (text_x, text_y))

        # Draw the button with a gap above
        button_y = box_y + box_height + button_gap
        self.draw_return_button(button_y)

    def draw_return_button(self, button_y):
        """Draw the 'Press Enter or Backspace to return' button with padding."""
        font = pygame.font.Font(self.game.font_name, 30)
        button_text = "Press Enter or Backspace to return"
        text_surface = font.render(button_text, True, self.game.WHITE)

        # Define padding inside the button
        padding_x = 30  # Horizontal padding
        padding_y = 20  # Vertical padding

        # Calculate button dimensions
        text_width, text_height = text_surface.get_size()
        button_width = text_width + 2 * padding_x  # Add horizontal padding
        button_height = text_height + 2 * padding_y  # Add vertical padding
        button_x = self.mid_w - button_width // 2

        # Draw the button background with rounded corners
        surface = pygame.Surface((button_width, button_height), pygame.SRCALPHA)
        pygame.draw.rect(surface, (11, 0, 16, 230), (0, 0, button_width, button_height), border_radius=50)
        pygame.draw.rect(surface, (204, 204, 204), (0, 0, button_width, button_height), width=1, border_radius=50)
        self.game.display.blit(surface, (button_x, button_y))

        # Draw the button text with padding
        text_x = button_x + padding_x
        text_y = button_y + padding_y
        self.game.display.blit(text_surface, (text_x, text_y))
