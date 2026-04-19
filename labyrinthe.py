import pygame
from random import choice, randint

from pile import Stack
from player import Player
from enemy import Enemy


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

        self.entry = (0, 0)
        self.exit = (width - 1, height - 1)
        self.grid = [[Cell() for _ in range(height)] for _ in range(width)]

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
            self.grid[i][j].wall_south = False
            self.grid[i][j + 1].wall_north = False
            self.grid[i][j + 1].visited = True
            stack.push((i, j + 1))
        elif direction == "N":
            self.grid[i][j].wall_north = False
            self.grid[i][j - 1].wall_south = False
            self.grid[i][j - 1].visited = True
            stack.push((i, j - 1))
        elif direction == "E":
            self.grid[i][j].wall_east = False
            self.grid[i + 1][j].wall_west = False
            self.grid[i + 1][j].visited = True
            stack.push((i + 1, j))
        elif direction == "W":
            self.grid[i][j].wall_west = False
            self.grid[i - 1][j].wall_east = False
            self.grid[i - 1][j].visited = True
            stack.push((i - 1, j))

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

        self.create_entry_and_exit()

    def create_entry_and_exit(self):
        """Open one entrance and one exit on opposite corners."""
        self.entry = (0, 0)
        self.exit = (self.width - 1, self.height - 1)
        self.grid[0][0].wall_west = False
        self.grid[self.width - 1][self.height - 1].wall_east = False

    def draw(self, surface):
        """Draw the full maze in a Pygame window."""
        cell = self.cell_size
        surface.fill(self.background_color)

        entry_rect = pygame.Rect(
            self.entry[0] * cell + 6,
            self.entry[1] * cell + 6,
            cell - 12,
            cell - 12,
        )
        exit_rect = pygame.Rect(
            self.exit[0] * cell + 6,
            self.exit[1] * cell + 6,
            cell - 12,
            cell - 12,
        )

        pygame.draw.rect(surface, self.entry_color, entry_rect)
        pygame.draw.rect(surface, self.exit_color, exit_rect)

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


def main():
    """Launch a small Pygame window that shows the generated maze."""
    pygame.init()

    cell_size = 32
    width = 20
    height = 20

    maze = Maze(width, height, cell_size)
    maze.generate()

    player = Player(maze.entry[0], maze.entry[1], (255, 80, 80), 100, 100, 0)
    enemy = Enemy(12,10,(80, 255, 80),100,100,0)


    screen = pygame.display.set_mode((width * cell_size, height * cell_size))
    pygame.display.set_caption("Maze Base")
    clock = pygame.time.Clock()
    font = pygame.font.SysFont(None, 48)
    won = False

    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    enemy.find_path(maze, (player.i,player.j))
                    enemy.move()
                if event.key == pygame.K_UP and not won:
                    player.move("N", maze)
                elif event.key == pygame.K_DOWN and not won:
                    player.move("S", maze)
                elif event.key == pygame.K_LEFT and not won:
                    player.move("W", maze)
                elif event.key == pygame.K_RIGHT and not won:
                    player.move("E", maze)
                elif event.key == pygame.K_r:
                    maze = Maze(width, height, cell_size)
                    maze.generate()
                    player = Player(maze.entry[0], maze.entry[1], (255, 80, 80), 100, 100, 0)
                    enemy = Enemy(12,10,(80, 255, 80),100,100,0)
                    won = False

            if (player.i, player.j) == maze.exit:
                won = True

        maze.draw(screen)
        enemy.draw(screen, maze.cell_size)
        player.draw(screen, maze.cell_size)

        if won:
            message = font.render("You Won! Press R to restart", True, (255, 255, 255))
            message_rect = message.get_rect(center=(screen.get_width() // 2, screen.get_height() // 2))
            background_rect = message_rect.inflate(24, 20)
            pygame.draw.rect(screen, (20, 24, 38), background_rect)
            pygame.draw.rect(screen, (255, 215, 0), background_rect, 2)
            screen.blit(message, message_rect)

        pygame.display.flip()
        clock.tick(60)

    pygame.quit()

if __name__ == "__main__":
    main()
