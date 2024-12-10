import pygame
import random
from game_elements.player import Player

class Grid(pygame.Surface):
    def __init__(self, size: (), shrinkRatio):
        super().__init__(size)
        self.shrinkRatio = shrinkRatio
        self.grid_w = int(self.get_width() / shrinkRatio)
        self.grid_h = int(self.get_height() / shrinkRatio)
        self.states = [["black" for _ in range(self.grid_w)] for _ in range(self.grid_h)]  # Initialize the grid
        self.completed = False
        self.generateGrid()  # Draw the initial grid

    def generate_random_maze(self, maze_width, maze_height):
        """Generate a random maze and update the grid."""
        # Resize the grid to the new maze dimensions
        self.grid_w = maze_width
        self.grid_h = maze_height
        self.states = [["black" for _ in range(self.grid_w)] for _ in range(self.grid_h)]  # Reinitialize the grid

        # Randomized DFS or other maze generation logic
        visited = [[False for _ in range(self.grid_w)] for _ in range(self.grid_h)]
        stack = []

        # Start at a random position
        start_x = random.randint(1, self.grid_w - 2)
        start_y = random.randint(1, self.grid_h - 2)
        stack.append((start_x, start_y))
        visited[start_y][start_x] = True

        while stack:
            current_x, current_y = stack[-1]
            self.states[current_y][current_x] = "white"  # Path is white

            # Check for unvisited neighbors
            neighbors = []
            for dx, dy in [(-2, 0), (2, 0), (0, -2), (0, 2)]:
                nx, ny = current_x + dx, current_y + dy
                if 0 < nx < self.grid_w and 0 < ny < self.grid_h and not visited[ny][nx]:
                    neighbors.append((nx, ny))

            if neighbors:
                nx, ny = random.choice(neighbors)
                # Carve a path between the current cell and the neighbor
                self.states[(current_y + ny) // 2][(current_x + nx) // 2] = "white"
                visited[ny][nx] = True
                stack.append((nx, ny))  # Push the neighbor to the stack
            else:
                stack.pop()  # Backtrack

        self.generateGrid()  # Redraw the grid after generating the maze

    def generateGrid(self, player: Player = None):
        """Draw the grid with the maze."""
        for v_layer in range(self.grid_h):  # Loop through each grid cell
            for h_layer in range(self.grid_w):
                rect = pygame.Rect(h_layer * self.shrinkRatio, v_layer * self.shrinkRatio, self.shrinkRatio, self.shrinkRatio)

                if player is not None and self.get((h_layer, v_layer)) == "black":
                    if rect.colliderect(player.collider):
                        player.collided(rect)

                if player is not None and self.get((h_layer, v_layer)) == "yellow":
                    if rect.colliderect(player.collider):
                        self.completed = True

                pygame.draw.rect(self, self.states[v_layer][h_layer], rect)

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
                if color == "green" or color == "purple":
                    self.states[yval][index] = "black"
                    self.set((index, yval), "black")

    def resetAll(self):
        for yval, y_list in enumerate(self.states):
            for index, color in enumerate(y_list):
                self.states[yval][index] = "black"
                self.set((index, yval), "black")
        self.completed = False
        self.generateGrid()
import pygame
import random
from game_elements.player import Player

class Grid(pygame.Surface):
    def __init__(self, size: (), shrinkRatio):
        super().__init__(size)
        self.shrinkRatio = shrinkRatio
        self.grid_w = int(self.get_width() / shrinkRatio)
        self.grid_h = int(self.get_height() / shrinkRatio)
        self.states = [["black" for _ in range(self.grid_w)] for _ in range(self.grid_h)]  # Initialize the grid
        self.completed = False
        self.generateGrid()  # Draw the initial grid

    def generate_random_maze(self, maze_width, maze_height):
        """Generate a random maze and update the grid."""
        # Resize the grid to the new maze dimensions
        self.grid_w = maze_width
        self.grid_h = maze_height
        self.states = [["black" for _ in range(self.grid_w)] for _ in range(self.grid_h)]  # Reinitialize the grid

        # Randomized DFS or other maze generation logic
        visited = [[False for _ in range(self.grid_w)] for _ in range(self.grid_h)]
        stack = []

        # Start at a random position
        start_x = random.randint(1, self.grid_w - 2)
        start_y = random.randint(1, self.grid_h - 2)
        stack.append((start_x, start_y))
        visited[start_y][start_x] = True

        while stack:
            current_x, current_y = stack[-1]
            self.states[current_y][current_x] = "white"  # Path is white

            # Check for unvisited neighbors
            neighbors = []
            for dx, dy in [(-2, 0), (2, 0), (0, -2), (0, 2)]:
                nx, ny = current_x + dx, current_y + dy
                if 0 < nx < self.grid_w and 0 < ny < self.grid_h and not visited[ny][nx]:
                    neighbors.append((nx, ny))

            if neighbors:
                nx, ny = random.choice(neighbors)
                # Carve a path between the current cell and the neighbor
                self.states[(current_y + ny) // 2][(current_x + nx) // 2] = "white"
                visited[ny][nx] = True
                stack.append((nx, ny))  # Push the neighbor to the stack
            else:
                stack.pop()  # Backtrack

        self.generateGrid()  # Redraw the grid after generating the maze

    def generateGrid(self, player: Player = None):
        """Draw the grid with the maze."""
        for v_layer in range(self.grid_h):  # Loop through each grid cell
            for h_layer in range(self.grid_w):
                rect = pygame.Rect(h_layer * self.shrinkRatio, v_layer * self.shrinkRatio, self.shrinkRatio, self.shrinkRatio)

                if player is not None and self.get((h_layer, v_layer)) == "black":
                    if rect.colliderect(player.collider):
                        player.collided(rect)

                if player is not None and self.get((h_layer, v_layer)) == "yellow":
                    if rect.colliderect(player.collider):
                        self.completed = True

                pygame.draw.rect(self, self.states[v_layer][h_layer], rect)

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
                if color == "green" or color == "purple":
                    self.states[yval][index] = "black"
                    self.set((index, yval), "black")

    def resetAll(self):
        for yval, y_list in enumerate(self.states):
            for index, color in enumerate(y_list):
                self.states[yval][index] = "black"
                self.set((index, yval), "black")
        self.completed = False
        self.generateGrid()
