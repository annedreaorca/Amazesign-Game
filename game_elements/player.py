import pygame
import random

class Particle:
    def __init__(self, x, y, size, color, lifetime=30):
        self.x = x
        self.y = y
        self.size = size
        self.color = color
        self.lifetime = lifetime
        self.velocity = [random.uniform(-1, 1), random.uniform(-1, 1)]
    
    def update(self):
        self.x += self.velocity[0]
        self.y += self.velocity[1]
        
        self.lifetime -= 1
        
        self.size = max(self.size - 0.1, 0)
        self.color = (self.color[0], self.color[1], self.color[2], max(self.color[3] - 5, 0))

    def draw(self, screen):
        if self.lifetime > 0:
            pygame.draw.circle(screen, self.color, (int(self.x), int(self.y)), int(self.size))

class Player:
    def __init__(self, screen, startPos: (), size=20, sprite_path="assets/character.png"):  
        self.screen = screen
        self.size = size  
        self.startPos = startPos
        self.x, self.y = startPos  
        self.move_direction = 5
        self.particles = [] 

        if sprite_path:
            self.sprite = pygame.image.load(sprite_path)
            self.sprite = pygame.transform.scale(self.sprite, (self.size * 3, self.size * 3))  
        else:
            self.sprite = None  

        self.collider = self.getCollider()

    def reset(self):
        """Reset the player's position, particles, and collider."""
        self.x, self.y = self.startPos  
        self.particles = [] 
        self.collider = self.getCollider()

    def draw(self):
        for particle in self.particles[:]:
            particle.update()
            particle.draw(self.screen)
            if particle.lifetime <= 0:  
                self.particles.remove(particle)

        if self.sprite:
            self.screen.blit(self.sprite, (self.x - self.size * 1.5, self.y - self.size * 1.5)) 
        else:
            pygame.draw.circle(self.screen, "#ffffff", (self.x, self.y), self.size)

    def getCollider(self):
        sr = self.size * 3
        self.collider = pygame.Rect(self.x - sr / 2, self.y - sr / 2, sr, sr)
        return self.collider

    def parse_input_and_draw(self, gestureList): 
        if not gestureList:
            return
        last_gesture = gestureList[-1]['Name']
        
        if last_gesture == "Closed_Fist":
            self.x += self.move_direction 
        elif last_gesture == "Open_Palm":
            self.x -= self.move_direction  
        elif last_gesture == "Thumb_Up":
            self.y -= self.move_direction 
        elif last_gesture == "Thumb_Down":
            self.y += self.move_direction 
        elif last_gesture == "ILoveYou":
            self.x = self.startPos[0]
            self.y = self.startPos[1]
        
        self.prevent_out_of_bounds()

        self.create_particle()

        self.collider = self.getCollider()
        self.draw()

    def create_particle(self):
        particle_color = (255, 255, 255, 150) 
        particle_size = random.randint(3, 8) 
        particle_lifetime = random.randint(20, 50)
        particle = Particle(self.x, self.y, particle_size, particle_color, particle_lifetime)
        self.particles.append(particle)

    def prevent_out_of_bounds(self):
        screen_width, screen_height = self.screen.get_size()
        
        if self.x - self.size * 1.5 < 0:
            self.x = self.size * 1.5 
        elif self.x + self.size * 1.5 > screen_width:
            self.x = screen_width - self.size * 1.5  
    
        if self.y - self.size * 1.5 < 0:
            self.y = self.size * 1.5 
        elif self.y + self.size * 1.5 > screen_height:
            self.y = screen_height - self.size * 1.5  

    def collided(self, rect, outOfBounds=False):
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

        if index == 0:
            self.y -= self.move_direction  
        elif index == 1:
            self.y += self.move_direction  
        elif index == 2:
            self.x -= self.move_direction  
        elif index == 3:
            self.x += self.move_direction  
