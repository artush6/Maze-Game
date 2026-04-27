import pygame


class Player:
    DIRECTION_OFFSETS = {
        "N": (0, -1),
        "S": (0, 1),
        "W": (-1, 0),
        "E": (1, 0),
    }

    def __init__(self, i, j, health, max_health, nb_bullets=2, facing="E"):
        self.i = i
        self.j = j
        self.health = health
        self.max_health = max_health
        self.nb_bullets = nb_bullets
        self.facing = facing
        self.color = ("red", "red", "orange", "yellow", "green")

    def move(self, direction, maze):
        if direction in self.DIRECTION_OFFSETS:
            self.facing = direction

        current_cell = maze.grid[self.i][self.j]

        if direction == 'N' and current_cell.wall_north is False:
            self.j -= 1
        elif direction == 'S' and current_cell.wall_south is False:
            self.j += 1
        elif direction == 'W' and current_cell.wall_west is False:
            self.i -= 1
        elif direction == 'E' and current_cell.wall_east is False:
            self.i += 1

    def draw(self, surface, cell_size):
        x = self.i * cell_size
        y = self.j * cell_size

        body_rect = pygame.Rect(
            x + 6,
            y + 6,
            cell_size - 12,
            cell_size - 12
        )
        body_center = body_rect.center
        body_radius = body_rect.width // 2
        nose_dx, nose_dy = self.DIRECTION_OFFSETS.get(self.facing, (1, 0))
        nose_center = (
            body_center[0] + nose_dx * (body_radius - 3),
            body_center[1] + nose_dy * (body_radius - 3),
        )

        pygame.draw.circle(surface, self.color[self.health], body_center, body_radius)
        pygame.draw.circle(surface, (255, 245, 180), nose_center, 4)
