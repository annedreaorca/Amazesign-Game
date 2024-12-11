from GestureDetection import GestureDetector
from game_elements import *

import pygame
import pygame_widgets

class GestureScreen: 
    def __init__(self, game):
        pygame.init()

        self.game = game
        self.screen = self.game.window 
        pygame.display.set_caption(self.game.window_caption)  

        self.background_image = pygame.image.load("assets/backgrounds/main-background-menu.jpg").convert()
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
        
        self.font = pygame.font.SysFont("Serif", 32)
        self.canUpdateTitle = False

        self.gameFinishedOverlay: pygame.Surface = None

        self.iconOffset: int = None 
        self.heightOffset: int = None 

        self.game_over = False 
        self.initUI(gap=20) 

    def initUI(self, gap): 
        self.gd.initStream()

        gestureLayoutWidth = (((self.gd.height / 4) + gap) * len(self.gd.possibleGestures)) - gap  
        self.streamArea = pygame.Surface((self.gd.width, self.gd.height))

        self.gestureIconLayout = pygame.Surface((gestureLayoutWidth, self.gd.height / 4))
        self.gestureIconLayout.fill("purple")

        self.heightOffset = 10  

        sr = 60
        self.grid = Grid((1080, 720), sr)

        self.gameFinishedOverlay = pygame.Surface(
            (self.screen.get_width(), self.screen.get_height() - self.heightOffset))

        self.mg = MazeGen(self.grid)

        self.iconOffset = gap + (self.gd.height / 4)

        self.canGen()

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
        # Calculate available space below the maze for positioning
        total_available_height = self.screen.get_height() - self.heightOffset - self.streamArea.get_height() - self.gestureIconLayout.get_height() - 20
        grid_y = (total_available_height - self.grid.get_height()) // 2
        available_height = self.screen.get_height() - (grid_y + self.grid.get_height()) - self.heightOffset
        stream_y = (available_height - self.streamArea.get_height()) // 2 + grid_y + self.grid.get_height()

        # Center the stream horizontally
        stream_x = (self.screen.get_width() - self.streamArea.get_width()) // 2

        # Create separate surfaces for left and right gesture icon layouts
        # Calculate the width of each layout based on the number of icons and the gap
        left_gesture_icon_layout_width = (len(self.gd.possibleGestures[:3]) * (self.gd.height / 4)) + (len(self.gd.possibleGestures[:3]) - 1) * self.iconOffset
        right_gesture_icon_layout_width = (len(self.gd.possibleGestures[3:]) * (self.gd.height / 4)) + (len(self.gd.possibleGestures[3:]) - 1) * self.iconOffset
        
        left_gesture_icon_layout = pygame.Surface((left_gesture_icon_layout_width, self.gd.height / 4))  
        right_gesture_icon_layout = pygame.Surface((right_gesture_icon_layout_width, self.gd.height / 4))  
        
        left_gesture_icon_layout.fill("white")
        right_gesture_icon_layout.fill("white")

        # Left side icons (first three gestures)
        addedOffset = 0
        left_gestures = self.gd.possibleGestures[:3]
        for i, gesture in enumerate(left_gestures):
            name = gesture
            if self.gd.gestures != []:
                if self.gd.gestures[-1]["Name"] == gesture:
                    name = gesture + "_f"
            
            # Load from the left folder
            img = pygame.image.load(f"icons/left/{name}.png").convert_alpha()
            rect = pygame.Rect(addedOffset, 0, self.gd.height / 4, self.gd.height / 4)
            img = pygame.transform.scale(img, (self.gd.height / 4, self.gd.height / 4))
            left_gesture_icon_layout.blit(img, rect)
            addedOffset += self.iconOffset

        # Right side icons (remaining gestures)
        addedOffset = 0
        right_gestures = self.gd.possibleGestures[3:]
        for i, gesture in enumerate(right_gestures):
            name = gesture
            if self.gd.gestures != []:
                if self.gd.gestures[-1]["Name"] == gesture:
                    name = gesture + "_f"
            
            # Load from the right folder
            img = pygame.image.load(f"icons/right/{name}.png").convert_alpha()
            rect = pygame.Rect(addedOffset, 0, self.gd.height / 4, self.gd.height / 4)
            img = pygame.transform.scale(img, (self.gd.height / 4, self.gd.height / 4))
            right_gesture_icon_layout.blit(img, rect)
            addedOffset += self.iconOffset

        # Capture the current frame from the gesture detection stream
        currentFrame = self.gd.getCurrentFrame()

        if currentFrame is not None:
            print(f"Captured frame shape: {currentFrame.shape}")  # Debugging step
            # Convert to a Pygame surface
            img = pygame.image.frombuffer(currentFrame.tostring(), currentFrame.shape[1::-1], "BGR")
            
            # Ensure the image fits within the stream area
            img = pygame.transform.scale(img, (self.streamArea.get_width(), self.streamArea.get_height()))
            self.streamArea.blit(img, (0, 0))
        else:
            print("Error: No frame captured.")  # Debugging step

        # Draw the camera stream and gesture icons
        self.screen.blit(self.grid, ((self.screen.get_width() - self.grid.get_width()) // 2, grid_y))  
        self.screen.blit(self.streamArea, (stream_x, stream_y))  

        # Position the left and right icon layouts horizontally aligned with the stream
        icon_layout_y = stream_y + (self.streamArea.get_height() - left_gesture_icon_layout.get_height()) // 2  # Vertically center icons relative to the stream

        # Centering the icon layouts horizontally with respect to the stream
        left_icon_x = stream_x - left_gesture_icon_layout.get_width() - 10  # Left of the stream
        right_icon_x = stream_x + self.streamArea.get_width() + 10  # Right of the stream
        
        # Blit the left and right icon layouts next to the camera stream
        self.screen.blit(left_gesture_icon_layout, (left_icon_x, icon_layout_y))  # Left side
        self.screen.blit(right_gesture_icon_layout, (right_icon_x, icon_layout_y))  # Right side

    
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