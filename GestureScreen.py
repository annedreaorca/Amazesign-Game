from GestureDetection import GestureDetector
from game_elements import *
from pygame_widgets.button import Button

import pygame
import pygame_widgets

class ButtonWithVisibility(Button):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.visible = True 

    def setVisibility(self, visible: bool):
        """Set the visibility of the button."""
        self.visible = visible

    def draw(self):
        """Override draw method to only draw the button if visible."""
        if self.visible:
            super().draw()

class GestureScreen:
    def __init__(self, game):
        pygame.init()

        self.game = game
        self.screen = self.game.window
        pygame.display.set_caption(self.game.window_caption)

        self.background_image = pygame.image.load("assets/backgrounds/main-background-menu.jpeg").convert()
        self.background_image = pygame.transform.scale(self.background_image, (self.screen.get_width(), self.screen.get_height()))

        self.clock = pygame.time.Clock()
        self.running = True
        self.gd = GestureDetector(20)

        self.player: Player = None
        self.mg: MazeGen = None
        self.canGenerate: bool = False
        self.generating: bool = False

        self.streamArea: pygame.Surface = None
        self.gestureIconLayout: pygame.Surface = None
        self.buttonSurface: pygame.Surface = None
        self.grid: Grid = None
        
        self.font = pygame.font.SysFont('assets/fonts/Square Game.otf', 32)
        self.canUpdateTitle = False

        self.gameFinishedOverlay: pygame.Surface = None

        self.iconOffset: int = None
        self.heightOffset: int = None

        self.game_over = False
        self.restart_button = None
        self.main_menu_button = None

        self.initUI(gap=0)

    def initUI(self, gap):
        self.gd.initStream()

        gestureLayoutWidth = (((self.gd.height / 4) + gap) * len(self.gd.possibleGestures)) - gap  
        self.streamArea = pygame.Surface((self.gd.width, self.gd.height))

        self.gestureIconLayout = pygame.Surface((gestureLayoutWidth, self.gd.height / 4))
        self.gestureIconLayout.fill("purple")

        self.heightOffset = 10

        sr = 120
        self.grid = Grid((1080, 720), sr)

        self.gameFinishedOverlay = pygame.Surface(
            (self.screen.get_width(), self.screen.get_height() - self.heightOffset))

        self.mg = MazeGen(self.grid)

        self.iconOffset = gap + (self.gd.height / 4)

        self.canGen()

    def initButtons(self):
        button_width = 200
        button_height = 50
        button_gap = 20

        screen_center_x = self.screen.get_width() // 2
        screen_center_y = self.screen.get_height() // 2

        self.restart_button = ButtonWithVisibility(
            self.screen, screen_center_x - button_width // 2, screen_center_y - button_height - button_gap,
            button_width, button_height, text="Restart",
            fontSize=32, margin=10, inactiveColour=(127, 17, 224, 230), hoverColour=(11, 0, 16, 100),
            pressedColour=(11, 0, 16, 100), onClick=self.restartGame
        )

        self.main_menu_button = ButtonWithVisibility(
            self.screen, screen_center_x - button_width // 2, screen_center_y + button_gap,
            button_width, button_height, text="Main Menu",
            fontSize=32, margin=10, inactiveColour=(127, 17, 224, 230), hoverColour=(11, 0, 16, 100),
            pressedColour=(11, 0, 16, 100), onClick=self.goToMainMenu
        )

    def restartGame(self):
        self.game_over = False
        self.grid.resetAll()
        self.player.reset() 
        self.canGenerate = False
        self.generating = False
        self.initUI(gap=40)  
        self.running = True

        self.restart_button.setVisibility(False)  
        self.main_menu_button.setVisibility(False)  
    def goToMainMenu(self):
        self.running = False
        self.game.curr_menu = self.game.main_menu  
        self.restart_button.setVisibility(False) 
        self.main_menu_button.setVisibility(False) 


    def canGen(self):
        self.canUpdateTitle = True
        if self.generating == False:
            self.grid.resetAll()
            start = self.mg.findStart(False)

            sr = self.grid.shrinkRatio
            playerStart = ((start[0] * sr) + (sr / 2), (start[1] * sr) + (sr / 2))
            self.player = Player(self.grid, playerStart, size=9)

            self.canGenerate = True
            self.generating = True

    def addStream(self):
        scale_factor = 3.5

        total_available_height = self.screen.get_height() - self.heightOffset - self.streamArea.get_height() - self.gestureIconLayout.get_height() - 20
        grid_y = (total_available_height - self.grid.get_height()) // 2
        available_height = self.screen.get_height() - (grid_y + self.grid.get_height()) - self.heightOffset
        stream_y = (available_height - self.streamArea.get_height()) // 2 + grid_y + self.grid.get_height()

        stream_x = (self.screen.get_width() - self.streamArea.get_width()) // 2

        icon_size = int(self.gd.height / 4 * scale_factor)

        left_gesture_icon_layout_width = len(self.gd.possibleGestures[:3]) * icon_size + (len(self.gd.possibleGestures[:3]) - 1) * self.iconOffset
        right_gesture_icon_layout_width = len(self.gd.possibleGestures[3:]) * icon_size + (len(self.gd.possibleGestures[3:]) - 1) * self.iconOffset

        left_gesture_icon_layout = pygame.Surface((left_gesture_icon_layout_width, icon_size), pygame.SRCALPHA)
        right_gesture_icon_layout = pygame.Surface((right_gesture_icon_layout_width, icon_size), pygame.SRCALPHA)

        addedOffset = 0
        left_gestures = self.gd.possibleGestures[:3]
        for i, gesture in enumerate(left_gestures):
            name = gesture
            if self.gd.gestures and self.gd.gestures[-1]["Name"] == gesture:
                name = gesture + "_f"

            img = pygame.image.load(f"icons/left/{name}.png").convert_alpha()
            img = pygame.transform.scale(img, (icon_size, icon_size))
            rect = pygame.Rect(addedOffset, 0, icon_size, icon_size)
            left_gesture_icon_layout.blit(img, rect)
            addedOffset += icon_size + self.iconOffset

        addedOffset = 0
        right_gestures = self.gd.possibleGestures[3:]
        for i, gesture in enumerate(right_gestures):
            name = gesture
            if self.gd.gestures and self.gd.gestures[-1]["Name"] == gesture:
                name = gesture + "_f"

            img = pygame.image.load(f"icons/right/{name}.png").convert_alpha()
            img = pygame.transform.scale(img, (icon_size, icon_size))
            rect = pygame.Rect(addedOffset, 0, icon_size, icon_size)
            right_gesture_icon_layout.blit(img, rect)
            addedOffset += icon_size + self.iconOffset

        currentFrame = self.gd.getCurrentFrame()
        if currentFrame is not None:
            print(f"Captured frame shape: {currentFrame.shape}")
            img = pygame.image.frombuffer(currentFrame.tostring(), currentFrame.shape[1::-1], "BGR")
            img = pygame.transform.scale(img, (self.streamArea.get_width(), self.streamArea.get_height()))
            self.streamArea.blit(img, (0, 0))
        else:
            print("Error: No frame captured.")
        self.screen.blit(self.grid, ((self.screen.get_width() - self.grid.get_width()) // 2, grid_y))
        self.screen.blit(self.streamArea, (stream_x, stream_y))

        icon_layout_y = stream_y + (self.streamArea.get_height() - left_gesture_icon_layout.get_height()) // 2
        left_icon_x = stream_x - left_gesture_icon_layout.get_width() - 25
        right_icon_x = stream_x + self.streamArea.get_width() + 25

        self.screen.blit(left_gesture_icon_layout, (left_icon_x, icon_layout_y))
        self.screen.blit(right_gesture_icon_layout, (right_icon_x, icon_layout_y))

    def addGameContent(self):
        if self.game_over:
            return

        if self.canGenerate:
            self.canGenerate = self.mg.generate()
        else:
            self.grid.resetColorMarkers()
            if self.mg.coordinates == []:
                if self.canUpdateTitle: self.mg.addStartAndEnd()
                self.generating = False

        if not self.generating and self.canUpdateTitle:
            self.grid.generateGrid(self.player)
            self.player.parse_input_and_draw(self.gd.gestures)
            if not self.grid.get_rect().contains(self.player.collider):
                self.player.collided(self.grid.get_rect(), outOfBounds=True)

    def addGameFinishedOverlay(self):
        self.gameFinishedOverlay.set_alpha(150)
        finishedTxt = self.font.render("Maze Completed", True, "pink")

        # Calculate the vertical position for the text to align with the buttons
        screen_center_y = self.screen.get_height() // 2
        text_offset_h = finishedTxt.get_height() // 2
        text_y_position = screen_center_y - text_offset_h

        self.screen.blit(self.gameFinishedOverlay, (0, self.heightOffset))
        self.screen.blit(finishedTxt, 
                        (self.screen.get_width() // 2 - finishedTxt.get_width() // 2, text_y_position))

        if self.restart_button is None or self.main_menu_button is None:
            self.initButtons()

        if self.game_over:
            self.restart_button.setVisibility(True)
            self.main_menu_button.setVisibility(True)

        self.restart_button.listen(pygame.event.get())
        self.restart_button.draw()
        self.main_menu_button.listen(pygame.event.get())
        self.main_menu_button.draw()


    def display(self):
        self.screen.blit(self.background_image, (0, 0))
        self.addStream()
        self.addGameContent()

        if self.grid.completed:
            self.game_over = True
            self.addGameFinishedOverlay()

        events = pygame.event.get()
        for event in events:
            if event.type == pygame.QUIT:
                self.running = False
                break

        pygame_widgets.update(events)

        pygame.display.flip()
        self.clock.tick(60)