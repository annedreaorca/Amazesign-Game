import pygame
import random

class LightningParticle:
    def __init__(self, x, y, size, color, velocity, lifetime=30):
        self.x = x
        self.y = y
        self.size = size
        self.color = color
        self.velocity = velocity
        self.lifetime = lifetime
        self.alpha = 255  # Full opacity for lightning effect

    def update(self):
        self.x += self.velocity[0]
        self.y += self.velocity[1]

        self.size = max(self.size - 0.2, 0)  # Lightning fades quickly
        self.alpha = max(self.alpha - 15, 0)  # Quick fade-out effect

    def draw(self, screen):
        if self.lifetime > 0 and self.alpha > 0:
            pygame.draw.circle(screen, (self.color[0], self.color[1], self.color[2], self.alpha),
                               (int(self.x), int(self.y)), int(self.size))
            # Optional: Add "spark" effect to simulate lightning strike
            for offset in range(1, 5):
                spark_color = (self.color[0], self.color[1], self.color[2], max(self.alpha - offset * 40, 0))
                pygame.draw.circle(screen, spark_color, (int(self.x + random.randint(-2, 2)), 
                                                         int(self.y + random.randint(-2, 2))), int(self.size // 2))

class Player:
    def __init__(self, screen, startPos: (), size=20, sprite_path="assets/sprite.png"):  
        self.screen = screen
        self.size = size  
        self.startPos = startPos
        self.x, self.y = startPos  
        self.move_direction = 5
        self.particles = [] 

        if sprite_path:
            self.sprite = pygame.image.load(sprite_path)
            self.sprite = pygame.transform.scale(self.sprite, (self.size * 5, self.size * 5))  
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
            self.screen.blit(self.sprite, (self.x - self.size * 2.5, self.y - self.size * 2.5)) 
        else:
            pygame.draw.circle(self.screen, "#ffffff", (self.x, self.y), self.size)


    def getCollider(self):
        sr = self.size * 5
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
        self.create_trail_particles()
        
        self.collider = self.getCollider() 
        self.draw()

    def create_trail_particles(self):
        # Cap the number of particles to prevent slowdowns
        if len(self.particles) > 100:  # Adjust the number as necessary
            self.particles.pop(0)  # Remove the oldest particle

        particle_color = (247, 102, 215)
        particle_size = random.randint(2, 4)
        particle_velocity = [random.uniform(-3, 3), random.uniform(-2, 2)]
        particle_lifetime = 30
        particle = LightningParticle(self.x, self.y, particle_size, particle_color, particle_velocity, particle_lifetime)
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
