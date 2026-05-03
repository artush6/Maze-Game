import pygame
from random import choice, randint, shuffle

class Stack:
    """Simple stack used by the maze generation algorithm."""

    def __init__(self):
        """Create an empty stack backed by a Python list."""
        self.items = []

    def is_empty(self):
        """Return True when the stack has no elements."""
        return self.items == []

    def push(self, value):
        """Push a value onto the top of the stack."""
        self.items.append(value)

    def pop(self):
        """Remove and return the top value of the stack."""
        if not self.is_empty():
            return self.items.pop()
        print("Stack is empty!")

    def size(self):
        """Return the number of elements in the stack."""
        return len(self.items)

    def top(self):
        """Return the top value without removing it."""
        if not self.is_empty():
            return self.items[-1]
        print("Stack is empty!")


class Cell:
    """One maze cell with four walls and a visited flag."""

    def __init__(self):
        self.wall_north = True
        self.wall_west = True
        self.wall_south = True
        self.wall_east = True
        self.visited = False

    def __repr__(self):
        return (
            f"C(N={int(self.wall_north)},S={int(self.wall_south)},"
            f"E={int(self.wall_east)},W={int(self.wall_west)},V={int(self.visited)})"
        )


class Maze:
    """Maze grid that keeps the original depth-first generation approach."""

    def __init__(self, width, height, cell_size=32):
        self.width = width
        self.height = height
        self.cell_size = cell_size
        self.wall_color = (240, 240, 240)
        self.background_color = (20, 24, 38)
        self.entry_color = (96, 165, 250)
        self.exit_color = (74, 222, 128)
        
        self.entry = (0,0)
        
        self.exit = (width - 1, height - 1)
        self.exit_image = pygame.image.load("images/exit flag.png").convert_alpha()
        self.exit_image = pygame.transform.scale(self.exit_image, (35, 35)) 
        
        self.grid = [[Cell() for _ in range(height)] for _ in range(width)]

    def __open_wall(self, i, j, direction):
        """Open the wall in `direction` and the matching wall in the neighboring cell."""
        if direction == "N" and j > 0:
            self.grid[i][j].wall_north = False
            self.grid[i][j - 1].wall_south = False
        elif direction == "S" and j < self.height - 1:
            self.grid[i][j].wall_south = False
            self.grid[i][j + 1].wall_north = False
        elif direction == "W" and i > 0:
            self.grid[i][j].wall_west = False
            self.grid[i - 1][j].wall_east = False
        elif direction == "E" and i < self.width - 1:
            self.grid[i][j].wall_east = False
            self.grid[i + 1][j].wall_west = False

    def __possible_directions(self, i, j):
        """Return the directions that lead to unvisited neighboring cells."""
        directions = []

        if j < self.height - 1 and not self.grid[i][j + 1].visited:
            directions.append("S")

        if j > 0 and not self.grid[i][j - 1].visited:
            directions.append("N")

        if i < self.width - 1 and not self.grid[i + 1][j].visited:
            directions.append("E")

        if i > 0 and not self.grid[i - 1][j].visited:
            directions.append("W")

        return directions

    def __remove_wall(self, i, j, direction, stack):
        """Open the wall between the current cell and the chosen neighbor."""
        if direction == "S":
            self.__open_wall(i, j, direction)
            self.grid[i][j + 1].visited = True
            stack.push((i, j + 1))
        elif direction == "N":
            self.__open_wall(i, j, direction)
            self.grid[i][j - 1].visited = True
            stack.push((i, j - 1))
        elif direction == "E":
            self.__open_wall(i, j, direction)
            self.grid[i + 1][j].visited = True
            stack.push((i + 1, j))
        elif direction == "W":
            self.__open_wall(i, j, direction)
            self.grid[i - 1][j].visited = True
            stack.push((i - 1, j))

    def __add_extra_openings(self, count):
        """Open a few additional walls to create loops in the maze."""
        candidates = []

        for i in range(self.width):
            for j in range(self.height):
                if i < self.width - 1 and self.grid[i][j].wall_east:
                    candidates.append((i, j, "E"))
                if j < self.height - 1 and self.grid[i][j].wall_south:
                    candidates.append((i, j, "S"))

        shuffle(candidates)

        for i, j, direction in candidates[:count]:
            self.__open_wall(i, j, direction)

    def generate(self):
        """Generate a random maze using depth-first search with backtracking."""
        stack = Stack()

        i = randint(0, self.width - 1)
        j = randint(0, self.height - 1)

        self.grid[i][j].visited = True
        stack.push((i, j))

        while not stack.is_empty():
            i, j = stack.pop()
            directions = self.__possible_directions(i, j)

            if len(directions) > 0:
                stack.push((i, j))
                direction = choice(directions)
                self.__remove_wall(i, j, direction, stack)

        extra_openings = max(1, (self.width * self.height) // 12)
        self.__add_extra_openings(extra_openings)

    def draw(self, surface):
        """Draw the full maze in a Pygame window."""
        cell = self.cell_size

        exit_rect = pygame.Rect(
            self.exit[0] * cell + 3,
            self.exit[1] * cell + 3,
            cell - 12,
            cell - 12,
        )
        
        surface.blit(self.exit_image, exit_rect)

        for i in range(self.width):
            for j in range(self.height):
                x = i * cell
                y = j * cell
                case = self.grid[i][j]

                if case.wall_north:
                    pygame.draw.line(surface, self.wall_color, (x, y), (x + cell, y), 2)
                if case.wall_south:
                    pygame.draw.line(surface, self.wall_color, (x, y + cell), (x + cell, y + cell), 2)
                if case.wall_west:
                    pygame.draw.line(surface, self.wall_color, (x, y), (x, y + cell), 2)
                if case.wall_east:
                    pygame.draw.line(surface, self.wall_color, (x + cell, y), (x + cell, y + cell), 2)



