import pygame
import random
from game_elements.player import Player


class Grid(pygame.Surface):
    def __init__(self, size: (), shrinkRatio, theme="default"):
        super().__init__(size)
        self.shrinkRatio = shrinkRatio
        self.grid_w = int(self.get_width() / shrinkRatio)
        self.grid_h = int(self.get_height() / shrinkRatio)
        self.states = [["black" for _ in range(self.grid_w)] for _ in range(self.grid_h)]
        self.completed = False
        self.theme = theme
        self.textures = {}
        self.loadTheme(theme)
        self.generateGrid()

    def loadTheme(self, theme: str):
        try:
            self.textures["wall"] = pygame.image.load(f'assets/wall.png')
            self.textures["path"] = pygame.image.load(f'assets/path.png')
            self.textures["start"] = pygame.image.load(f'assets/start.png')
            self.textures["end"] = pygame.image.load(f'assets/end.png')
        except FileNotFoundError as e:
            print("Error: One or more asset files are missing in the 'assets' directory!")
            raise e

    def generate_random_maze(self, maze_width, maze_height):
        """Generate a random maze and update the grid."""
        self.grid_w = maze_width
        self.grid_h = maze_height
        self.states = [["black" for _ in range(self.grid_w)] for _ in range(self.grid_h)]

        visited = [[False for _ in range(self.grid_w)] for _ in range(self.grid_h)]
        stack = []

        start_x = random.randint(1, self.grid_w - 2)
        start_y = random.randint(1, self.grid_h - 2)
        stack.append((start_x, start_y))
        visited[start_y][start_x] = True

        while stack:
            current_x, current_y = stack[-1]
            self.states[current_y][current_x] = "white"

            neighbors = []
            for dx, dy in [(-2, 0), (2, 0), (0, -2), (0, 2)]:
                nx, ny = current_x + dx, current_y + dy
                if 0 < nx < self.grid_w and 0 < ny < self.grid_h and not visited[ny][nx]:
                    neighbors.append((nx, ny))

            if neighbors:
                nx, ny = random.choice(neighbors)
                self.states[(current_y + ny) // 2][(current_x + nx) // 2] = "white"
                visited[ny][nx] = True
                stack.append((nx, ny))
            else:
                stack.pop()

        self.states[start_y][start_x] = "start"
        end_x, end_y = self.grid_w - 2, self.grid_h - 2
        self.states[end_y][end_x] = "end"

        self.generateGrid()

    def generateGrid(self, player: Player = None):
        for v_layer in range(self.grid_h):
            for h_layer in range(self.grid_w):
                rect = pygame.Rect(h_layer * self.shrinkRatio, v_layer * self.shrinkRatio, self.shrinkRatio, self.shrinkRatio)

                if self.states[v_layer][h_layer] == "black":
                    self.blit(pygame.transform.scale(self.textures["wall"], rect.size), rect.topleft)
                elif self.states[v_layer][h_layer] == "white":
                    self.blit(pygame.transform.scale(self.textures["path"], rect.size), rect.topleft)
                elif self.states[v_layer][h_layer] == "yellow": 
                    self.blit(pygame.transform.scale(self.textures["start"], rect.size), rect.topleft)
                
                if player:
                    if self.get((h_layer, v_layer)) == "black" and rect.colliderect(player.collider):
                        player.collided(rect)
                    elif self.get((h_layer, v_layer)) == "yellow" and rect.colliderect(player.collider):
                        self.completed = True


    def switchTheme(self, new_theme):
        self.loadTheme(new_theme)
        self.generateGrid()

    def set(self, pos: (int, int), color: str):
        if pos[0] < 0 or pos[1] < 0:
            return
        self.states[pos[1]][pos[0]] = color.lower()
        self.generateGrid()

    def get(self, pos: (int, int)):
        if pos[0] < 0 or pos[1] < 0:
            raise IndexError
        return self.states[pos[1]][pos[0]]

    def resetColorMarkers(self):
        for yval, y_list in enumerate(self.states):
            for index, color in enumerate(y_list):
                if color in {"green", "purple"}:
                    self.states[yval][index] = "black"
                    self.set((index, yval), "black")

    def resetAll(self):
        for yval, y_list in enumerate(self.states):
            for index, color in enumerate(y_list):
                self.states[yval][index] = "black"
                self.set((index, yval), "black")
        self.completed = False
        self.generateGrid()
