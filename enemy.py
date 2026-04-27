import pygame


ENEMY_TYPES = {
    "chaser": {
        "color": (80, 255, 80),
        "health": 100,
        "max_health": 100,
        "attack_cooldown": 0,
        "speed": 1.0,
        "size": 1.0,
        "on_death_spawn": [],
        "spawn_style": "death",
    },
    "berserker": {
        "color": (255, 90, 90),
        "health": 60,
        "max_health": 60,
        "attack_cooldown": 0,
        "speed": 2.0,
        "size": 0.85,
        "on_death_spawn": [],
        "spawn_style": "death",
    },
    "tank": {
        "color": (80, 120, 255),
        "health": 200,
        "max_health": 200,
        "attack_cooldown": 0,
        "speed": 0.6,
        "size": 1.35,
        "on_death_spawn": ["tankling"],
        "spawn_style": "corners",
    },
    "revenant": {
        "color": (180, 80, 255),
        "health": 90,
        "max_health": 90,
        "attack_cooldown": 0,
        "speed": 1.0,
        "size": 1.0,
        "on_death_spawn": ["hunter"],
        "spawn_style": "origin",
    },
    "tankling": {
        "color": (120, 170, 255),
        "health": 110,
        "max_health": 110,
        "attack_cooldown": 0,
        "speed": 1.2,
        "size": 1.15,
        "on_death_spawn": ["berserker"],
        "spawn_style": "origin",
    },
    "hunter": {
        "color": (255, 220, 80),
        "health": 80,
        "max_health": 80,
        "attack_cooldown": 0,
        "speed": 1.4,
        "size": 1.0,
        "on_death_spawn": [],
        "spawn_style": "death",
    },
    "splitter": {
        "color": (80, 255, 255),
        "health": 70,
        "max_health": 70,
        "attack_cooldown": 0,
        "speed": 1.0,
        "size": 1.0,
        "on_death_spawn": ["berserker", "berserker"],
        "spawn_style": "corners",
    },
}


class Enemy:
    def __init__(
        self,
        i,
        j,
        color,
        health,
        max_health,
        attack_cooldown,
        speed=1.0,
        size=1.0,
        on_death_spawn=None,
    ):
        self.i = i
        self.j = j
        self.color = color
        self.health = health
        self.max_health = max_health
        self.attack_cooldown = attack_cooldown
        self.speed = speed
        self.size = size
        self.on_death_spawn = list(on_death_spawn or [])
        self.spawn_style = "death"
        self.move_progress = 0.0
        self.current_path = []
        self.start_i = i
        self.start_j = j

    @classmethod
    def from_type(cls, i, j, enemy_type):
        data = ENEMY_TYPES[enemy_type]
        enemy = cls(
            i,
            j,
            data["color"],
            data["health"],
            data["max_health"],
            data["attack_cooldown"],
            speed=data["speed"],
            size=data["size"],
            on_death_spawn=data["on_death_spawn"],
        )
        enemy.enemy_type = enemy_type
        enemy.spawn_style = data.get("spawn_style", "death")
        return enemy

    @property
    def is_alive(self):
        return self.health > 0

    def move(self):
        self.move_progress += self.speed
        while self.current_path != [] and self.move_progress >= 1:
            nv_position = self.current_path.pop(0)
            self.i = nv_position[0]
            self.j = nv_position[1]
            self.move_progress -= 1

    def find_path(self, maze, goal):
        """
        Find the shortest path from `start` to `goal` using A*.
        Returns a list of coordinates representing the path.
        """
        start = (self.i, self.j)

        if goal != start:

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

    def in_player(self, player):
        return self.is_alive and self.i == player.i and self.j == player.j

    def draw(self, surface, cell_size):
        if not self.is_alive:
            return

        x = self.i * cell_size
        y = self.j * cell_size

        inset = max(2, int(6 / max(self.size, 0.5)))
        rect_size = min(cell_size - 2, int((cell_size - 2 * inset) * self.size))
        rect_size = max(10, rect_size)

        player_rect = pygame.Rect(
            x + (cell_size - rect_size) // 2,
            y + (cell_size - rect_size) // 2,
            rect_size,
            rect_size
        )

        pygame.draw.rect(surface, self.color, player_rect)


def distance(a, b):
    """donne le nombre de deplacement entre 2 point dans une grille"""
    return abs(a[0] - b[0]) + abs(a[1] - b[1])
    
