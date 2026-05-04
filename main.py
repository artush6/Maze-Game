import pygame
from random import randint
from maps import Maps
from player import Player
from enemy import Enemy
from bullet import Bullet
from labyrinthe import Maze


def main():
    pygame.init()
    state = "menu"

    cell_size = 40
    width = 20
    height = 20

    screen = pygame.display.set_mode((width * cell_size + 400, height * cell_size + 5))
    pygame.display.set_caption("Jeu du labyrinthe")
    clock = pygame.time.Clock()
    font = pygame.font.SysFont(None, 48)
    small_font = pygame.font.SysFont(None, 28)
    tiny_font = pygame.font.SysFont(None, 24)
    button_play = pygame.Rect(screen.get_width()//2 - 150, 200, 300, 60)
    button_rules = pygame.Rect(screen.get_width()//2 - 150, 300, 300, 60)
    button_back = pygame.Rect(20, 20, 120, 50)
    pause_continue_button = pygame.Rect(screen.get_width()//2 - 160, 240, 320, 60)
    pause_restart_button = pygame.Rect(screen.get_width()//2 - 160, 320, 320, 60)
    pause_menu_button = pygame.Rect(screen.get_width()//2 - 160, 400, 320, 60)
    sidebar_x = width * cell_size + 20

    def draw_text_block(surface, text_lines, start_x, start_y, line_height, text_font, color):
        y = start_y
        for line in text_lines:
            txt = text_font.render(line, True, color)
            surface.blit(txt, (start_x, y))
            y += line_height

    def draw_sidebar(surface):
        panel_rect = pygame.Rect(width * cell_size + 5, 0, 395, height * cell_size + 5)
        pygame.draw.rect(surface, (32, 38, 56), panel_rect)
        pygame.draw.line(surface, (255, 215, 0), (width * cell_size + 5, 0), (width * cell_size + 5, height * cell_size + 5), 2)

        title = font.render("Commandes", True, (255, 255, 255))
        surface.blit(title, (sidebar_x, 35))

        controls_title = small_font.render("Pendant la partie", True, (255, 215, 0))
        surface.blit(controls_title, (sidebar_x, 135))
        controls_lines = [
            "↑ ↓ ← →",
            "S : tirer",
            "R : recommencer",
            "ESC : pause",
        ]
        draw_text_block(surface, controls_lines, sidebar_x, 175, 30, tiny_font, (235, 235, 235))

    def draw_pause_overlay(surface):
        overlay = pygame.Surface((screen.get_width(), screen.get_height()), pygame.SRCALPHA)
        overlay.fill((10, 12, 20, 180))
        surface.blit(overlay, (0, 0))

        title = font.render("Pause", True, (255, 255, 255))
        surface.blit(title, title.get_rect(center=(screen.get_width() // 2, 160)))

        pygame.draw.rect(surface, (70, 130, 180), pause_continue_button)
        pygame.draw.rect(surface, (70, 130, 180), pause_restart_button)
        pygame.draw.rect(surface, (180, 70, 70), pause_menu_button)

        txt_continue = small_font.render("Continuer", True, (255, 255, 255))
        txt_restart = small_font.render("Recommencer", True, (255, 255, 255))
        txt_menu = small_font.render("Retour au menu", True, (255, 255, 255))

        surface.blit(txt_continue, txt_continue.get_rect(center=pause_continue_button.center))
        surface.blit(txt_restart, txt_restart.get_rect(center=pause_restart_button.center))
        surface.blit(txt_menu, txt_menu.get_rect(center=pause_menu_button.center))

    def respawn_positions(enemy, spawn_count):
        if getattr(enemy, "spawn_style", "death") == "origin":
            return [(enemy.start_i, enemy.start_j)] * spawn_count

        if getattr(enemy, "spawn_style", "death") == "corners":
            corners = [(width - 1, 0), (0, height - 1), (0, 0), (width - 1, height - 1)]
            return corners[:spawn_count]

        return [(enemy.i, enemy.j)] * spawn_count

    def build_game_state(level):
        maze = Maze(width, height, cell_size)
        maze.generate()
        player = Player(maze.entry[0], maze.entry[1], 4, 4, 2, facing="E")
        enemies = [
            Enemy.from_type(1, 19, "chaser", level),
            Enemy.from_type(19, 19, "revenant", level),
            Enemy.from_type(19, 1, "hunter", level),
            Enemy.from_type(10, 19, "splitter", level),
            Enemy.from_type(19, 10, "tank", level),
        ]
        pos_x,  pos_y = 100, 100
        while pos_x + pos_y > (maze.width + maze.height)//2:
            pos_x = randint(0, maze.width - 1)
            pos_y = randint(0,maze.height-1)
        maps = Maps(pos_x, pos_y)
        return maze, player, enemies, maps
    
    ones_time = pygame.time.get_ticks()
    bullets_delay = 1000
    
    last_move_time = 0
    move_delay = 120
    
    maze, player, list_enemy, maps = build_game_state(1)
    bullets = []
    won = False
    lost = False
    level_changed = False


    running = True
    while running:
        current_time = pygame.time.get_ticks()
        enemy_reached_player = False

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

            elif event.type == pygame.MOUSEBUTTONDOWN:
                mouse_pos = pygame.mouse.get_pos()

                if state == "menu":
                    if button_play.collidepoint(mouse_pos):
                        level = 1
                        maze, player, list_enemy, maps = build_game_state(level)
                        bullets = []
                        won = False
                        lost = False
                        level_changed = False
                        state = "game"
                    elif button_rules.collidepoint(mouse_pos):
                        state = "rules"

                elif state == "rules":
                    if button_back.collidepoint(mouse_pos):
                        state = "menu"

                elif state == "pause":
                    if pause_continue_button.collidepoint(mouse_pos):
                        state = "game"
                    elif pause_restart_button.collidepoint(mouse_pos):
                        maze, player, list_enemy, maps = build_game_state(level)
                        bullets = []
                        won = False
                        lost = False
                        level_changed = False
                        ones_time = pygame.time.get_ticks()
                        state = "game"
                    elif pause_menu_button.collidepoint(mouse_pos):
                        state = "menu"

            elif event.type == pygame.KEYDOWN and state == "game":
                if event.key == pygame.K_ESCAPE:
                    state = "pause"
                elif event.key == pygame.K_s:
                    if player.nb_bullets > 0:
                        bullet_x = player.i * maze.cell_size + maze.cell_size // 2
                        bullet_y = player.j * maze.cell_size + maze.cell_size // 2

                        if player.facing == "N":
                            dx, dy = 0, -1
                            bullet_y -= 10
                        elif player.facing == "S":
                            dx, dy = 0, 1
                            bullet_y += 10
                        elif player.facing == "W":
                            dx, dy = -1, 0
                            bullet_x -= 10
                        else:
                            dx, dy = 1, 0
                            bullet_x += 10

                        new_bullet = Bullet(bullet_x, bullet_y, dx, dy)
                        player.nb_bullets -= 1
                        bullets.append(new_bullet)

                elif event.key == pygame.K_r:
                    maze, player, list_enemy, maps = build_game_state(level)
                    bullets = []
                    won = False
                    lost = False
                    level_changed = False
                    ones_time = pygame.time.get_ticks()

            elif event.type == pygame.KEYDOWN and state == "pause":
                if event.key == pygame.K_ESCAPE:
                    state = "game"
                    
        keys = pygame.key.get_pressed()

        if state == "game" and not won and not lost:
            if current_time - last_move_time > move_delay:
                if keys[pygame.K_UP]:
                    player.move("N", maze)
                    last_move_time = current_time
                elif keys[pygame.K_DOWN]:
                    player.move("S", maze)
                    last_move_time = current_time
                elif keys[pygame.K_LEFT]:
                    player.move("W", maze)
                    last_move_time = current_time
                elif keys[pygame.K_RIGHT]:
                    player.move("E", maze)
                    last_move_time = current_time

        if state == "game":
            for enemy in list_enemy:
                if current_time - enemy.last_move > enemy.move_delay and not won and not lost:
                    enemy.find_path(maze, (player.i, player.j))
                    enemy.move()
                    if enemy.in_player(player):
                        enemy_reached_player = True
                    enemy.last_move = current_time
        
            if current_time - ones_time > bullets_delay and not won and not lost:
                if player.nb_bullets < 2:
                    player.nb_bullets += 1   
                    ones_time = current_time
            
            if maps.in_player(player):
                maps.is_alive = False
                maps.find_path(maze)

            if enemy_reached_player and player.health > 0:
                player.health -= 1

            if (player.i, player.j) == maze.exit:
                won = True

            for bullet in bullets:
                bullet.update(maze, screen.get_width(), screen.get_height())
                for enemy in list_enemy:
                    if enemy.is_alive:
                        bullet.collides_with_enemy(enemy, maze.cell_size)

            bullets = [bullet for bullet in bullets if bullet.alive]

            next_enemies = []
            spawned_enemies = []
            for enemy in list_enemy:
                if enemy.is_alive:
                    next_enemies.append(enemy)
                    continue

                positions = respawn_positions(enemy, len(getattr(enemy, "on_death_spawn", [])))
                for spawn_type, (spawn_i, spawn_j) in zip(getattr(enemy, "on_death_spawn", []), positions):
                    spawned_enemies.append(Enemy.from_type(spawn_i, spawn_j, spawn_type))

            list_enemy = next_enemies + spawned_enemies

            if player.health == 0:
                lost = True



        screen.fill((maze.background_color))

        if state == "menu":
            title = font.render("Jeu du labyrinthe", True, (255,255,255))
            screen.blit(title, (screen.get_width()//2 - title.get_width()//2, 100))

            pygame.draw.rect(screen, (70,130,180), button_play)
            pygame.draw.rect(screen, (70,130,180), button_rules)

            txt_play = font.render("Lancer le jeu", True, (255,255,255))
            txt_rules = font.render("Regles", True, (255,255,255))
                
            screen.blit(txt_play, txt_play.get_rect(center=button_play.center))
            screen.blit(txt_rules, txt_rules.get_rect(center=button_rules.center))


        elif state == "rules":
            rules_text = [
                "Objectif : atteindre la sortie du labyrinthe.",
                "Fleches : se deplacer dans les couloirs.",
                "S : tirer une balle dans la direction regardee.",
                "R : recommencer la partie au niveau actuel.",
                "Les ennemis vous retirent de la vie au contact.",
                "La carte magique montre le chemin vers la sortie.",
                "Le nombre de balles est limite mais se recharge.",
                "Si vous gagnez, vous passez au niveau suivant.",
                "Si vous perdez, vous revenez au niveau precedent.",
            ]

            for i, line in enumerate(rules_text):
                txt = small_font.render(line, True, (255,255,255))
                screen.blit(txt, (100, 110 + i*48))

            pygame.draw.rect(screen, (180,70,70), button_back)
            txt_back = font.render("Retour", True, (255,255,255))
            screen.blit(txt_back, txt_back.get_rect(center=button_back.center))


        elif state == "game" or state == "pause":
            maze.draw(screen)

            if maps.is_alive:
                maps.draw_objet(screen, maze.cell_size)
            else:
                maps.draw_path(screen, maze.cell_size)

            for enemy in list_enemy:
                enemy.draw(screen, maze.cell_size)

            player.draw(screen, maze.cell_size)

            for bullet in bullets:
                bullet.draw(screen)

            draw_sidebar(screen)

            if state == "pause":
                draw_pause_overlay(screen)

        if won:
            if not level_changed:
                level = level+1
                level_changed = True
            message = font.render(f"Gagne ! Appuie sur R pour aller au niveau {level} !", True, (255, 255, 255))
            message_rect = message.get_rect(center=(screen.get_width() // 2, screen.get_height() // 2))
            background_rect = message_rect.inflate(24, 20)
            pygame.draw.rect(screen, (20, 24, 38), background_rect)
            pygame.draw.rect(screen, (255, 215, 0), background_rect, 2)
            screen.blit(message, message_rect)

        if lost:
            if not level_changed:
                level = max(1,level-1)
                level_changed = True
            message = font.render(f"Perdu ! Appuie sur R pour aller au niveau {level} !", True, (255, 255, 255))
            message_rect = message.get_rect(center=(screen.get_width() // 2, screen.get_height() // 2))
            background_rect = message_rect.inflate(24, 20)
            pygame.draw.rect(screen, (20, 24, 38), background_rect)
            pygame.draw.rect(screen, (255, 215, 0), background_rect, 2)
            screen.blit(message, message_rect)

        pygame.display.flip()
        clock.tick(30)

    pygame.quit()

if __name__ == "__main__":
    main()
