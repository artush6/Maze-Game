import pygame

class Player:
    def __init__(self, i, j, color, health, max_health, attack_cooldown):
        self.i = i
        self.j = j
        self.color = color
        self.health = health
        self.max_health = max_health
        self.attack_cooldown = attack_cooldown

    def move(self, direction, maze):
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

        player_rect = pygame.Rect(
            x + 6,
            y + 6,
            cell_size - 12,
            cell_size - 12
        )

        pygame.draw.rect(surface, self.color, player_rect)
