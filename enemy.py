import pygame


class Enemy:
    def __init__(self, i, j, color, health, max_health, attack_cooldown):
        self.i = i
        self.j = j
        self.color = color
        self.health = health
        self.max_health = max_health
        self.attack_cooldown = attack_cooldown
        self.current_path = []

    @property
    def is_alive(self):
        return self.health > 0

    def move(self):
        if self.current_path != []:
            nv_position = self.current_path.pop(0)
            self.i = nv_position[0]
            self.j = nv_position[1]
    

    def find_path(self, maze, goal):
        """
        Find the shortest path from `start` to `goal` using A*.
        Returns a list of coordinates representing the path.
        """
        start = (self.i, self.j)
        
        came_from = {}
        g_score = {start: 0}
        f_score = {start: distance(start, goal)}
    
        open_set = []
        open_set.append((0 + f_score[start], g_score[start], start))
        while len(open_set) > 0:
            f, current_cost, current = min(open_set)
            open_set.remove((f, current_cost, current))

            if current == goal:
                path = []
                while current in came_from:
                    path.append(current)
                    current = came_from[current]
                self.current_path = path[::-1]

            for direction in ['N', 'S', 'W', 'E']:
                ni, nj = current
                if direction == 'N':
                    ni -= 0
                    nj -= 1
                elif direction == 'S':
                    ni += 0
                    nj += 1
                elif direction == 'W':
                    ni -= 1
                    nj += 0
                elif direction == 'E':
                    ni += 1
                    nj += 0

                if (0 <= ni < maze.width and 0 <= nj < maze.height):
                    next_cell = (ni, nj)
                

                    if (direction == 'N' and not maze.grid[current[0]][current[1]].wall_north) or \
                        (direction == 'S' and not maze.grid[current[0]][current[1]].wall_south) or \
                        (direction == 'W' and not maze.grid[current[0]][current[1]].wall_west) or \
                        (direction == 'E' and not maze.grid[current[0]][current[1]].wall_east):
                        tentative_g = g_score[current] + 1
                        if next_cell not in g_score or tentative_g < g_score[next_cell]:
                            came_from[next_cell] = current
                            g_score[next_cell] = tentative_g
                            f_score[next_cell] = tentative_g + distance(next_cell, goal)
                            open_set.append((f_score[next_cell], tentative_g, next_cell))
        
    def draw(self, surface, cell_size):
        if not self.is_alive:
            return

        x = self.i * cell_size
        y = self.j * cell_size

        player_rect = pygame.Rect(
            x + 6,
            y + 6,
            cell_size - 12,
            cell_size - 12
        )

        pygame.draw.rect(surface, self.color, player_rect)



def distance(a, b):
    """donne le nombre de deplacement entre 2 point dans une grille"""
    return abs(a[0] - b[0]) + abs(a[1] - b[1])
