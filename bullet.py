import pygame


class Bullet:
    def __init__(self, x, y, dx, dy, speed=8, radius=5, color=(255, 220, 120)):
        self.x = x
        self.y = y
        self.dx = dx
        self.dy = dy
        self.speed = speed
        self.radius = radius
        self.color = color
        self.alive = True

    def update(self, maze, screen_width, screen_height):
        if not self.alive:
            return

        next_x = self.x + self.dx * self.speed
        next_y = self.y + self.dy * self.speed

        cell_i = int(self.x) // maze.cell_size
        cell_j = int(self.y) // maze.cell_size

        if not (0 <= cell_i < maze.width and 0 <= cell_j < maze.height):
            self.alive = False
            return

        cell = maze.grid[cell_i][cell_j]
        current_cell_left = cell_i * maze.cell_size
        current_cell_right = current_cell_left + maze.cell_size
        current_cell_top = cell_j * maze.cell_size
        current_cell_bottom = current_cell_top + maze.cell_size

        if self.dx > 0 and next_x + self.radius >= current_cell_right and cell.wall_east:
            self.alive = False
            return
        if self.dx < 0 and next_x - self.radius <= current_cell_left and cell.wall_west:
            self.alive = False
            return
        if self.dy > 0 and next_y + self.radius >= current_cell_bottom and cell.wall_south:
            self.alive = False
            return
        if self.dy < 0 and next_y - self.radius <= current_cell_top and cell.wall_north:
            self.alive = False
            return

        self.x = next_x
        self.y = next_y

        if (
            self.x + self.radius < 0
            or self.x - self.radius > screen_width
            or self.y + self.radius < 0
            or self.y - self.radius > screen_height
        ):
            self.alive = False

    def draw(self, screen):
        pygame.draw.circle(screen, self.color, (int(self.x), int(self.y)), self.radius)

    def collides_with_enemy(self, enemy, cell_size):
        if not enemy.is_alive:
            return False

        enemy_x = enemy.i * cell_size
        enemy_y = enemy.j * cell_size

        enemy_rect = pygame.Rect(
            enemy_x + 6,
            enemy_y + 6,
            cell_size - 12,
            cell_size - 12
        )

        if enemy_rect.collidepoint(int(self.x), int(self.y)):
            self.alive = False
            enemy.health = max(0, enemy.health - 50)
            return True
        return False
