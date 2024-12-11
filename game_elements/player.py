import pygame

class Player:
    def __init__(self, screen, startPos: (), size=20, sprite_path="assets/character.png"):  
        self.screen = screen
        self.size = size  
        self.startPos = startPos
        self.x, self.y = (startPos[0], startPos[1])
        self.move_direction = 5

        if sprite_path:
            self.sprite = pygame.image.load(sprite_path)
            self.sprite = pygame.transform.scale(self.sprite, (self.size * 2, self.size * 2)) 
        else:
            self.sprite = None  
        
        self.collider = self.getCollider()

    def draw(self): 
        if self.sprite:
            self.screen.blit(self.sprite, (self.x - self.size, self.y - self.size))
        else:
            pygame.draw.circle(self.screen, "#ffffff", (self.x, self.y), self.size)
        self.getCollider()

    def getCollider(self):
        sr = self.screen.shrinkRatio
        self.collider = pygame.Rect(self.x - sr / 2, self.y - sr / 2, sr, sr).inflate(-5, -5)
        return self.collider

    def parse_input_and_draw(self, gestureList): 
        if not gestureList: return
        if gestureList[-1]['Name'] == None:
            pass
        elif gestureList[-1]["Name"] == "Closed_Fist":
            self.x += self.move_direction 
        elif gestureList[-1]["Name"] == "Open_Palm":
            self.x += -self.move_direction  
        elif gestureList[-1]["Name"] == "Thumb_Up":
            self.y += -self.move_direction 
        elif gestureList[-1]["Name"] == "Thumb_Down":
            self.y += self.move_direction 
        elif gestureList[-1]["Name"] == "ILoveYou":
            self.x = self.startPos[0]
            self.y = self.startPos[1]
        self.draw()

    def collided(self, rect, outOfBounds=False):
        diffList = []
        if not outOfBounds:
            diffList = [self.collider.midbottom[1] - rect.midtop[1],
                        rect.midbottom[1] - self.collider.midtop[1],
                        self.collider.midright[0] - rect.midleft[0],
                        rect.midright[0] - self.collider.midleft[0]]
        else:
            diffList = [self.collider.midbottom[1] - rect.midbottom[1],
                        rect.midtop[1] - self.collider.midtop[1],
                        self.collider.midright[0] - rect.midright[0],
                        rect.midleft[0] - self.collider.midleft[0]]

        absDiff = [abs(difference) for difference in diffList]
        index = absDiff.index(min(absDiff)) 

        if index == 0:
            self.y -= self.move_direction  
        elif index == 1:
            self.y += self.move_direction  
        elif index == 2:
            self.x -= self.move_direction  
        elif index == 3:
            self.x += self.move_direction 
