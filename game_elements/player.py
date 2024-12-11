import pygame

class Player:
    def __init__(self, screen, startPos: (), size=20, sprite_path="assets/character.png"):  
        self.screen = screen
        self.size = size  
        self.position = startPos 
        self.x, self.y = startPos 
        self.move_direction = 5

        # Load sprite if available
        if sprite_path:
            self.sprite = pygame.image.load(sprite_path)
            self.sprite = pygame.transform.scale(self.sprite, (self.size * 3, self.size * 3))  
        else:
            self.sprite = None  

        self.collider = self.getCollider()

    def draw(self): 
        """Draw player on the screen."""
        if self.sprite:
            self.screen.blit(self.sprite, (self.position[0] - self.size * 1.5, self.position[1] - self.size * 1.5)) 
        else:
            pygame.draw.circle(self.screen, "#ffffff", self.position, self.size)

    def getCollider(self):
        """Update and return the player's collider (rectangular area for collision detection)."""
        sr = self.size * 3
        self.collider = pygame.Rect(self.position[0] - sr / 2, self.position[1] - sr / 2, sr, sr)
        return self.collider

    def parse_input_and_draw(self, gestureList): 
        """Process gesture inputs to move player."""
        if not gestureList: return
        last_gesture = gestureList[-1]['Name']
        
        # Update position based on the latest gesture
        if last_gesture == "Closed_Fist":
            self.position = (self.position[0] + self.move_direction, self.position[1])
        elif last_gesture == "Open_Palm":
            self.position = (self.position[0] - self.move_direction, self.position[1])  
        elif last_gesture == "Thumb_Up":
            self.position = (self.position[0], self.position[1] - self.move_direction) 
        elif last_gesture == "Thumb_Down":
            self.position = (self.position[0], self.position[1] + self.move_direction) 
        elif last_gesture == "ILoveYou":
            self.position = self.startPos  # Reset to start position
        
        self.prevent_out_of_bounds()
        self.collider = self.getCollider()
        self.draw()

    def prevent_out_of_bounds(self):
        """Ensure the player doesn't move out of the screen boundaries."""
        screen_width, screen_height = self.screen.get_size()
        
        if self.position[0] - self.size * 1.5 < 0:
            self.position = (self.size * 1.5, self.position[1])
        elif self.position[0] + self.size * 1.5 > screen_width:
            self.position = (screen_width - self.size * 1.5, self.position[1])
    
        if self.position[1] - self.size * 1.5 < 0:
            self.position = (self.position[0], self.size * 1.5)
        elif self.position[1] + self.size * 1.5 > screen_height:
            self.position = (self.position[0], screen_height - self.size * 1.5)

    def collided(self, rect, outOfBounds=False):
        """Check for collisions and adjust player's position accordingly."""
        diffList = []
        if not outOfBounds:
            diffList = [
                self.collider.midbottom[1] - rect.midtop[1],
                rect.midbottom[1] - self.collider.midtop[1],
                self.collider.midright[0] - rect.midleft[0],
                rect.midright[0] - self.collider.midleft[0]
            ]
        else:
            diffList = [
                self.collider.midbottom[1] - rect.midbottom[1],
                rect.midtop[1] - self.collider.midtop[1],
                self.collider.midright[0] - rect.midright[0],
                rect.midleft[0] - self.collider.midleft[0]
            ]

        absDiff = [abs(difference) for difference in diffList]
        index = absDiff.index(min(absDiff)) 

        # Adjust position based on collision
        if index == 0:
            self.position = (self.position[0], self.position[1] - self.move_direction)
        elif index == 1:
            self.position = (self.position[0], self.position[1] + self.move_direction)
        elif index == 2:
            self.position = (self.position[0] - self.move_direction, self.position[1])
        elif index == 3:
            self.position = (self.position[0] + self.move_direction, self.position[1])

