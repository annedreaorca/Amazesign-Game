from game_elements.grid import Grid
import random


class MazeGen:
    def __init__(self, grid: Grid):
        self.grid = grid
        self.coordinates = []
        self.startPos = ()
        self.endPos = [0, 0]  
        self.width = self.grid.grid_w
        self.height = self.grid.grid_h
        self.startMode = ""  
        print(f"Grid Width: {self.width}, Grid Height: {self.height}")

    def findStart(self, plot=False):
        xCoord, yCoord = 0, 0
        if random.randint(0, 1) == 1: 
            possibleX = [0, self.width - 1]
            xCoord = possibleX[random.randint(0, 1)]
            yCoord = random.randint(0, self.height - 1)
            self.endPos[0] = 0 if xCoord == (self.width - 1) else (self.width - 1)
            self.startMode = "horizontal"
        else:
            possibleY = [0, self.height - 1]
            xCoord = random.randint(0, self.width - 1)
            yCoord = possibleY[random.randint(0, 1)]
            self.endPos[1] = 0 if yCoord == (self.height - 1) else (self.height - 1)
            self.startMode = "vertical"
        coords = (xCoord, yCoord)
        print(f"Starting point: {coords}")

        self.coordinates.append(coords)
        self.startPos = coords
        if plot: self.grid.set(coords, "white")
        return coords

    # Order:
    # 1. find available locations (is the square in front available, if so check if the one in front of that is, then take it)
    # 2. Randomly choose available location to move to, and move
    # 3. Continue, if there are no available locations, backtrack, slowly move down the list, constantly checking for available locations

    def evaluatePossibleCoord(self, coord, visualize,
                              originalVector) -> bool:
        vector_1 = (originalVector[1], originalVector[0])  
        vector_2 = (-originalVector[1], -originalVector[0]) 
        vector_3 = (originalVector[0], originalVector[1])  
        vectorsToCheck = [vector_1, vector_2, vector_3]

        canMove = True

        for vector in vectorsToCheck:
            posToCheck = (coord[0] + vector[0], coord[1] + vector[1])
            try:
                if self.grid.get(posToCheck) != "white":
                    None
                else:
                    canMove = False
            except IndexError:
                continue

        return canMove

    def findAvailableLocations(self, pos, visualize):
        directionVectors = [(0, 1), (0, -1), (1, 0), (-1, 0)]
        availablePositions = []

        for direction in directionVectors:
            newPos = (pos[0] + direction[0], pos[1] + direction[1])

            try:
                color = self.grid.get(newPos)
                if color == "black": 
                    if visualize:
                        self.grid.set(newPos, "green")
                    availablePos = self.evaluatePossibleCoord(newPos, visualize, direction)
                    if availablePos: availablePositions.append(newPos)

            except IndexError:
                continue
    

        print(f"At: {pos}, Possible next moves (green): {availablePositions}")
        return availablePositions

    def generate(self) -> bool:  
        self.grid.resetColorMarkers()
        self.grid.set(self.coordinates[-1], "white")

        positions = self.findAvailableLocations(self.coordinates[-1], visualize=True)
        if positions == []:
            if len(self.coordinates) == 1:
                print(self.coordinates)
                self.findEndPoints()
            self.coordinates.pop()
            if self.coordinates == []: return False
            result = self.generate()
            return result
        num = random.randint(0, len(positions) - 1)  

        newPos = positions[num]
        self.coordinates.append(newPos)

        print(f"{newPos} Selected")
        return True

    def addStartAndEnd(self):
        self.grid.set((self.endPos[0], self.endPos[1]), "yellow")

    def findEndPoints(self):
        if self.startMode == "horizontal":
            possibleY = []
            for i in range(self.height):
                color = self.grid.get((self.endPos[0], i))
                if color == "white": possibleY.append(i)
            index = random.randint(0, len(possibleY)) - 1
            self.endPos[1] = possibleY[index]
        else:
            possibleX = []
            for i in range(self.width):
                color = self.grid.get((i, self.endPos[1]))
                if color == "white": possibleX.append(i)
            index = random.randint(0, len(possibleX)) - 1
            self.endPos[0] = possibleX[index]