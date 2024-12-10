from GestureDetection import GestureDetector
from game_elements import *

import pygame
import pygame_widgets
from pygame_widgets.button import Button


class GestureScreen: 
    def __init__(self, game):
        pygame.init()

        self.game = game  # Store the game instance
        self.screen = self.game.window  # Use the game's window for rendering
        pygame.display.set_caption(self.game.window_caption)  # Use the game's caption


        self.clock = pygame.time.Clock()
        self.running = True
        self.gd = GestureDetector(10)

        self.player: Player = None
        self.mg: MazeGen = None
        self.canGenerate: bool = False
        self.generating: bool = False

        self.streamArea: pygame.Surface = None
        self.gestureIconLayout: pygame.Surface = None
        self.buttonSurface: pygame.Surface = None
        self.grid: Grid = None
        
        self.font = pygame.font.SysFont("Serif", 32)
        self.text = None
        self.canUpdateTitle = False  # Changes title from default val to boolean controlled val

        self.gameFinishedOverlay: pygame.Surface = None

        self.iconOffset: int = None  # icon spacing
        self.heightOffset: int = None  # divider from the stream and the game

         # Initialize UI here
        self.initUI(gap=10)  # Example gap value

    def initUI(self, gap):  # Initializes the UI and all necessary components
        self.gd.initStream()  # Must run in order to get the camera properties from the stream

        # Gesture icon layout width calculation
        gestureLayoutWidth = (((self.gd.height / 4) + gap) * len(self.gd.possibleGestures)) - gap  # 7 gap sizes and 8 icon sizes
        self.streamArea = pygame.Surface((self.gd.width, self.gd.height))  # Gesture stream surface

        # Layout for gesture icons
        self.gestureIconLayout = pygame.Surface((gestureLayoutWidth, self.gd.height / 4))
        self.gestureIconLayout.fill("purple")  # Color of the gesture icon layout

        # Offset below the stream area and icon layout
        self.heightOffset = self.gd.height + self.gestureIconLayout.get_height() + 10 + 20

        # Status text
        self.text = self.font.render(f"Status: Not Generated", True, "purple")

        # Set grid width and height to 720
        grid_size = 720

        # Dynamically set shrinkRatio based on grid size (720x720)
        sr = grid_size // 20  # This ensures the grid cells fit within 720x720

        # Create grid with dynamically calculated shrinkRatio
        self.grid = Grid((grid_size, grid_size), sr)

        # Game overlay surface
        self.gameFinishedOverlay = pygame.Surface(
            (self.screen.get_width(), self.screen.get_height() - self.heightOffset))

        # Initialize maze generator
        self.mg = MazeGen(self.grid)

        # Gesture icon layout offset
        self.iconOffset = gap + (self.gd.height / 4)

        # Automatically start maze generation
        self.canGen()


    def addStream(self):
        addedOffset = 0
        self.gestureIconLayout.fill("white")
        for gesture in self.gd.possibleGestures:
            name = gesture
            if self.gd.gestures != []:
                if self.gd.gestures[-1]["Name"] == gesture:
                    name = gesture + "_f"  # filled
            img = pygame.image.load(f"icons/{name}.png").convert_alpha()
            rect = pygame.Rect(addedOffset, 0, self.gd.height / 4, self.gd.height / 4)

            img = pygame.transform.scale(img, (self.gd.height / 4, self.gd.height / 4))

            self.gestureIconLayout.blit(img, rect)
            addedOffset += self.iconOffset

        currentFrame = self.gd.getCurrentFrame()
        # code from https://stackoverflow.com/questions/19306211/opencv-cv2-image-to-pygame-image
        img = pygame.image.frombuffer(currentFrame.tostring(), currentFrame.shape[1::-1],
                                      "BGR")

        self.screen.fill("white")
        self.screen.blit(self.gestureIconLayout, (0, self.gd.height + 10))
        self.screen.blit(self.streamArea, (0, 0))
        self.streamArea.blit(img, (0, 0))

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

    def addGameContent(self):
        if self.canGenerate:
            self.canGenerate = self.mg.generate()  # coordinates are stored in self.mg
        else:
            self.grid.resetColorMarkers()
            if self.mg.coordinates == []:
                if self.canUpdateTitle: self.mg.addStartAndEnd()
                self.generating = False

        if not self.generating and self.canUpdateTitle:
            self.grid.generateGrid(self.player)
            self.player.parse_input_and_draw(self.gd.gestures)
            # if player isn't fully a part of the grid
            if not self.grid.get_rect().contains(self.player.collider):
                self.player.collided(self.grid.get_rect(), outOfBounds=True)

        self.screen.blit(self.text, (self.gd.width * 1.75, (self.heightOffset / 2) + 75))
        self.screen.blit(self.grid, (0, self.heightOffset))

    def addGameFinishedOverlay(self):
        self.gameFinishedOverlay.set_alpha(150)
        finishedTxt = self.font.render("Finished!", True, "green")

        txt_offset_w = finishedTxt.get_width() / 2
        txt_offset_h = finishedTxt.get_height() / 2
        overlay_offset_w = self.gameFinishedOverlay.get_width() / 2
        overlay_offset_h = self.gameFinishedOverlay.get_height() / 2

        r = pygame.Rect(overlay_offset_w - txt_offset_w, (overlay_offset_h - txt_offset_h)+self.heightOffset, finishedTxt.get_width(),
                        finishedTxt.get_height())

        self.screen.blit(self.gameFinishedOverlay, (0, self.heightOffset))
        pygame.draw.rect(self.screen, "white", r.inflate(20, 20), border_radius=50)
        self.screen.blit(finishedTxt,
                         (overlay_offset_w - txt_offset_w, (overlay_offset_h - txt_offset_h) + self.heightOffset))

    def display(self):
        if self.canUpdateTitle:
            self.text = self.font.render(f"Status: {'Generated' if not self.generating else 'Generating'}", True,
                                         "green" if not self.generating else "purple")
        self.addStream()

        # Rect Order  -> (top_left_x, top_left_y, ending_x, ending_y)
        pygame.draw.rect(self.screen, "purple",
        pygame.Rect(0, self.heightOffset - 10, self.screen.get_width(), 10))  # dividing line
        self.addGameContent()

        if self.grid.completed:
            self.addGameFinishedOverlay()

        events = pygame.event.get()
        for event in events:
            if event.type == pygame.QUIT:
                self.running = False
                break

        pygame_widgets.update(events)

        pygame.display.flip()
        self.clock.tick(60)