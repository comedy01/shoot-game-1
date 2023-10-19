import pygame
import math
import random
import os

# Initialize Pygame
pygame.init()

# Constants
SCREEN_WIDTH, SCREEN_HEIGHT = 800, 800
PLAYER_SIZE = 27
PLAYER_SPEED = 200
BULLET_SPEED = 900
ENEMY_SPEED = 100
ENEMY_SPAWN_DELAY = 80
ENEMY_SPAWN_DISTANCE = 250
fire_upgrades = 4
dual_shoot_upgrades = 1
quad_shoot_upgrades = 1
quad_shoot_cost = 12
fire_upgrade_cost = 4
dual_shoot_cost = 10
turret_cost = 10
GRID_SIZE = 6
CELL_SIZE = SCREEN_WIDTH // GRID_SIZE
TURRET_SIZE = 20
turret_fire_delay = 26
angle = 0
cls_amount = 0
turret_count = 36
movement_speed_upgrades = 3
movement_speed_cost = 3

WHITE = (255, 255, 255)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLACK = (0, 0, 0)

screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Shooting Game")

player_img = pygame.image.load(os.path.join("Assets", "player.png"))

bullet_img = pygame.Surface((10, 10))
bullet_img.fill(RED)

enemy_img = pygame.Surface((30, 30))
enemy_img.fill(GREEN)

player_x = SCREEN_WIDTH // 2 - PLAYER_SIZE // 2
player_y = SCREEN_HEIGHT // 2 - PLAYER_SIZE // 2

bullets = []
enemies = []
turrets = []

running = True
game_over = False
score = 0
score_increment = 1
spawn_delay = 0
original_bullet_delay = 12
bullet_delay = original_bullet_delay
coin_count = 0
upgrade_menu_active = False
paused = False
dual_shoot_enabled = False
quad_shoot_enabled = False
coin_delay = 1000
turret_placement_mode = False
selected_cell = None
turret_shoot_delay = turret_fire_delay
bullet_speed_cost = 4
bullet_speed_upgrades = 3
enemies_killed = 0
enemies_killed_threshold = 10
turret_menu = False
turret_fire_cost = 4
turret_fire_upgrades = 4
has_turret = False

clock = pygame.time.Clock()
turret_img = pygame.image.load(os.path.join("Assets", "turret.png"))

font = pygame.font.Font(None, 32)
font_color = (255, 255, 255)
font_position = (10, 10)

pause_font = pygame.font.Font(None, 48)
pause_text = pause_font.render("Paused", True, BLACK)
pause_rect = pause_text.get_rect(center=(SCREEN_WIDTH // 2, 25))

back_button_font = pygame.font.Font(None, 32)
back_button_text = pause_font.render("Back", True, BLACK)
back_button_rect = pause_text.get_rect(center=(SCREEN_WIDTH // 2 + 20, 260))

resume_button_font = pygame.font.Font(None, 36)
resume_button_text = resume_button_font.render("Resume", True, BLACK)
resume_button_rect = resume_button_text.get_rect(center=(SCREEN_WIDTH // 2, 300))

upgrades_button_font = pygame.font.Font(None, 36)
upgrades_button_text = upgrades_button_font.render("Upgrades", True, BLACK)
upgrades_button_rect = upgrades_button_text.get_rect(center=(SCREEN_WIDTH // 2, 340))

rate_of_fire_button_font = pygame.font.Font(None, 30)
rate_of_fire_button_text = rate_of_fire_button_font.render(f"Increase Rate of Fire ({fire_upgrade_cost} coins), {fire_upgrades} left", True, RED)
rate_of_fire_button_rect = rate_of_fire_button_text.get_rect(center=(SCREEN_WIDTH // 2, 410))

dual_shoot_button_font = pygame.font.Font(None, 30)
dual_shoot_button_text = dual_shoot_button_font.render(f"Dual Shoot ({dual_shoot_cost} coins), {dual_shoot_upgrades} left", True, RED)
dual_shoot_button_rect = dual_shoot_button_text.get_rect(center=(SCREEN_WIDTH // 2, 470))

turret_button_font = pygame.font.Font(None, 30)
turret_button_text = turret_button_font.render(f"Place a turret ({turret_cost} coins), {turret_count} left", True, RED)
turret_button_rect = turret_button_text.get_rect(center=(SCREEN_WIDTH // 2, 380))

bullet_speed_font = pygame.font.Font(None, 30)
bullet_speed_text = turret_button_font.render(f"Bullet Speed ({bullet_speed_cost} coins), {bullet_speed_upgrades} left", True, RED)
bullet_speed_rect = turret_button_text.get_rect(center=(SCREEN_WIDTH // 2+15, 440))

quad_shoot_button_font = pygame.font.Font(None, 30)
quad_shoot_button_text = dual_shoot_button_font.render(f"Quad Shoot ({quad_shoot_cost} coins), {quad_shoot_upgrades} left", True, RED)
quad_shoot_button_rect = dual_shoot_button_text.get_rect(center=(SCREEN_WIDTH // 2, 470))

turret_menu_font = pygame.font.Font(None, 30)
turret_menu_text = turret_button_font.render(f"Turrets", True, RED)
turret_menu_rect = turret_button_text.get_rect(center=(SCREEN_WIDTH // 2 + 120, 500))

turret_fire_button_font = pygame.font.Font(None, 30)
turret_fire_button_text = turret_fire_button_font.render(f"Increase turret fire rate ({turret_fire_cost} coins), {turret_fire_upgrades}left", True, RED)
turret_fire_button_rect = turret_fire_button_text.get_rect(center=(SCREEN_WIDTH // 2, 410))

movement_speed_button_font = pygame.font.Font(None, 30)
movement_speed_button_text = movement_speed_button_font.render(f"Increase movement speed ({movement_speed_cost} coins), {movement_speed_upgrades} left", True, RED)
movement_speed_button_rect = movement_speed_button_text.get_rect(center=(SCREEN_WIDTH // 2, 380))

class Turret:
    def __init__(self, row, col):
        self.row = row
        self.col = col
        self.target = None
        self.shoot_delay = 0

    def update_target(self, target):
        self.target = target

    def shoot(self):
        if self.target and self.shoot_delay <= 0:
            dx = self.target[0] - (self.col * CELL_SIZE + CELL_SIZE // 2)
            dy = self.target[1] - (self.row * CELL_SIZE + CELL_SIZE // 2)
            angle = math.degrees(math.atan2(dy, dx))
            bullets.append([self.col * CELL_SIZE + CELL_SIZE // 2, angle, self.row * CELL_SIZE + CELL_SIZE // 2])
            self.shoot_delay = turret_fire_delay


def calculate_distance(point1, point2):
    x1, y1 = point1
    x2, y2 = point2
    return math.sqrt((x1 - x2) ** 2 + (y1 - y2) ** 2)


def find_closest_enemy(turret, enemies):
    min_distance = float('inf')
    closest_enemy = None
    for enemy in enemies:
        enemy_center = (enemy[0] + 15, enemy[1] + 15)
        turret_center = (turret.col * CELL_SIZE + CELL_SIZE // 2, turret.row * CELL_SIZE + CELL_SIZE // 2)
        d = calculate_distance(enemy_center, turret_center)

        if d < min_distance:
            min_distance = d
            closest_enemy = enemy

    return closest_enemy


def draw_grid():
    for row in range(GRID_SIZE):
        for col in range(GRID_SIZE):
            pygame.draw.rect(screen, (100, 100, 100), (col * CELL_SIZE, row * CELL_SIZE, CELL_SIZE, CELL_SIZE), 1)


def place_turret(row, col):
    turrets.append(Turret(row, col))


def spawn_enemy():
    while True:
        enemy_x = random.randint(0, SCREEN_WIDTH - 30)
        enemy_y = random.randint(0, SCREEN_HEIGHT - 30)

        distance = math.sqrt((enemy_x - player_x) ** 2 + (enemy_y - player_y) ** 2)
        if distance >= ENEMY_SPAWN_DISTANCE:
            enemies.append([enemy_x, enemy_y])
            break


def display_score(score):
    text = font.render(f"Score: {score}", True, RED)
    screen.blit(text, font_position)


splashScreenTimer = 0
while splashScreenTimer < 4:
    dt = clock.tick(60) / 1000
    splashScreenTimer += dt
    start_time = round(5 - splashScreenTimer)
    keys = pygame.key.get_pressed()
    if keys[pygame.K_SPACE]:
        splashScreenTimer = 4
    if keys[pygame.K_q]:
        pygame.quit()

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()

    screen.fill((0, 255, 255))
    startMessage = font.render("CREATED BY COMEDY", True, (48, 93, 120))
    screen.blit(startMessage, (screen.get_width() / 2 - startMessage.get_width() / 2, screen.get_height() / 2 - startMessage.get_height() / 2-40))
    startingIn = font.render(f"Starting in {start_time}", True, (48, 93, 120))
    screen.blit(startingIn, (screen.get_width() / 2 - startingIn.get_width() / 2, screen.get_height() / 2 - startingIn.get_height() / 2))
    skip_to_start = font.render("press space to skip timer", True, (48, 93, 120))
    screen.blit(skip_to_start, (screen.get_width() / 2 - skip_to_start.get_width() / 2, screen.get_height() / 2 - skip_to_start.get_height() / 2+40))
    pygame.display.update()
    pygame.time.delay(60)

while running:
    dt = clock.tick(60) / 1000

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                if not paused:
                    paused = True

                elif upgrade_menu_active and paused:
                    upgrade_menu_active = False
                    turret_placement_mode = False

                elif turret_placement_mode and paused:
                    turret_placement_mode = False
                    upgrade_menu_active = False
                    turret_menu = True

                elif turret_menu and paused:
                    turret_menu = False
                    upgrade_menu_active = True
                    paused = True

                elif paused:
                    paused = False

        if event.type == pygame.MOUSEBUTTONDOWN and turret_menu and paused and not upgrade_menu_active and not turret_placement_mode:
            if back_button_rect.collidepoint(event.pos):
                turret_menu = False
                upgrade_menu_active = True
                paused = True

            elif turret_button_rect.collidepoint(event.pos):
                turret_menu = False
                turret_placement_mode = True
                paused = True

            elif turret_fire_button_rect.collidepoint(event.pos) and coin_count >= turret_fire_cost and turret_fire_upgrades > 0 and has_turret:
                turret_menu = True
                turret_placement_mode = False
                paused = True
                coin_count -= turret_fire_cost
                turret_fire_delay -= 7
                turret_fire_upgrades -= 1
                turret_fire_button_text = turret_fire_button_font.render(f"Increase turret fire rate ({turret_fire_cost} coins), {turret_fire_upgrades}left", True, RED)
            elif resume_button_rect.collidepoint(event.pos):
                turret_menu = False
                paused = False
                upgrade_menu_active = False

        if event.type == pygame.MOUSEBUTTONDOWN and paused and not upgrade_menu_active and not turret_placement_mode and not turret_menu:
            if resume_button_rect.collidepoint(event.pos):
                paused = not paused

            elif upgrades_button_rect.collidepoint(event.pos):
                upgrade_menu_active = True
                paused = True

        if event.type == pygame.MOUSEBUTTONDOWN and upgrade_menu_active and paused and not turret_placement_mode and not turret_menu:
            if resume_button_rect.collidepoint(event.pos):
                upgrade_menu_active = False
                paused = False

            elif back_button_rect.collidepoint(event.pos):
                upgrade_menu_active = False
                paused = True

            elif turret_menu_rect.collidepoint(event.pos):
                turret_menu = True
                upgrade_menu_active = False
                paused = True

            elif rate_of_fire_button_rect.collidepoint(event.pos):
                if fire_upgrades > 0 and coin_count >= fire_upgrade_cost:
                    coin_count -= fire_upgrade_cost
                    original_bullet_delay -= 2.5
                    fire_upgrades -= 1
                    rate_of_fire_button_text = rate_of_fire_button_font.render(f"Increase Rate of Fire ({fire_upgrade_cost} coins), {fire_upgrades} left", True, RED)

            elif dual_shoot_button_rect.collidepoint(event.pos) and dual_shoot_upgrades > 0 and coin_count >= dual_shoot_cost:
                coin_count -= dual_shoot_cost
                dual_shoot_upgrades -= 1
                dual_shoot_enabled = True
                dual_shoot_button_text = dual_shoot_button_font.render(f"Dual Shoot ({dual_shoot_cost} coins), {dual_shoot_upgrades} left", True, RED)

            elif quad_shoot_button_rect.collidepoint(event.pos) and quad_shoot_upgrades > 0 and coin_count >= quad_shoot_cost:
                coin_count -= quad_shoot_cost
                quad_shoot_upgrades -= 1
                dual_shoot_enabled = False
                quad_shoot_enabled = True
                quad_shoot_button_text = dual_shoot_button_font.render(f"Quad Shoot ({quad_shoot_cost} coins), {quad_shoot_upgrades} left", True, RED)

            elif bullet_speed_rect.collidepoint(event.pos) and coin_count >= bullet_speed_cost and bullet_speed_upgrades > 0:
                coin_count -= 4
                bullet_speed_upgrades -= 1
                BULLET_SPEED += 300
                bullet_speed_text = turret_button_font.render(f"Bullet Speed ({bullet_speed_cost} coins), {bullet_speed_upgrades} left", True, RED)

            elif movement_speed_button_rect.collidepoint(event.pos) and coin_count >= movement_speed_cost and movement_speed_upgrades > 0:
                PLAYER_SPEED = PLAYER_SPEED * 1.2
                coin_count -= movement_speed_cost
                movement_speed_upgrades -= 1
                movement_speed_button_text = movement_speed_button_font.render(f"Increase movement speed ({movement_speed_cost} coins), {movement_speed_upgrades} left", True, RED)

        if event.type == pygame.MOUSEBUTTONDOWN and turret_placement_mode and paused and not upgrade_menu_active:
            if not turret_button_rect.collidepoint(event.pos):
                row = event.pos[1] // CELL_SIZE
                col = event.pos[0] // CELL_SIZE

                if (row, col) not in [(turret.row, turret.col) for turret in turrets] and coin_count >= turret_cost and turret_count > 0:
                    place_turret(row, col)
                    new_turret = Turret(row, col)
                    turrets.append(new_turret)
                    coin_count -= turret_cost
                    turret_count -= 1
                    has_turret = True
                    turret_button_text = turret_button_font.render(f"Turrets ({turret_cost} coins), {turret_count} left", True, RED)

    bullet_key = pygame.key.get_pressed()
    if bullet_key[pygame.K_SPACE] and bullet_delay <= 0:
        if dual_shoot_enabled:
            bullets.append([player_x + PLAYER_SIZE // 2, angle, player_y + PLAYER_SIZE // 2])
            bullets.append([player_x + PLAYER_SIZE // 2, angle + 180, player_y + PLAYER_SIZE // 2])
        elif quad_shoot_enabled:
            bullets.append([player_x + PLAYER_SIZE // 2, angle, player_y + PLAYER_SIZE // 2])
            bullets.append([player_x + PLAYER_SIZE // 2, angle + 90, player_y + PLAYER_SIZE // 2])
            bullets.append([player_x + PLAYER_SIZE // 2, angle + 180, player_y + PLAYER_SIZE // 2])
            bullets.append([player_x + PLAYER_SIZE // 2, angle + 270, player_y + PLAYER_SIZE // 2])
        else:
            bullets.append([player_x + PLAYER_SIZE // 2, angle, player_y + PLAYER_SIZE // 2])
        bullet_delay = original_bullet_delay

    if not game_over and not paused and not upgrade_menu_active:
        mouse_x, mouse_y = pygame.mouse.get_pos()

        angle = math.atan2(mouse_y - player_y - PLAYER_SIZE // 2, mouse_x - player_x - PLAYER_SIZE // 2)
        angle = math.degrees(angle)

        player_rotated = pygame.transform.rotate(player_img, -angle)
        player_rect = player_rotated.get_rect(center=(player_x + PLAYER_SIZE // 2, player_y + PLAYER_SIZE // 2))
        screen.fill(WHITE)
        screen.blit(player_rotated, player_rect.topleft)

        for bullet in bullets:
            bullet[0] += math.cos(math.radians(bullet[1])) * BULLET_SPEED * dt
            bullet[2] += math.sin(math.radians(bullet[1])) * BULLET_SPEED * dt
            pygame.draw.circle(screen, RED, (int(bullet[0]), int(bullet[2])), 5)

        bullets = [bullet for bullet in bullets if 0 <= bullet[0] <= SCREEN_WIDTH and 0 <= bullet[2] <= SCREEN_HEIGHT]

        for enemy in enemies:
            enemy_center = (enemy[0] + 15, enemy[1] + 15)
            player_center = (player_x + PLAYER_SIZE // 2, player_y + PLAYER_SIZE // 2)

            direction_vector = (player_center[0] - enemy_center[0], player_center[1] - enemy_center[1])

            vector_length = math.sqrt(direction_vector[0] ** 2 + direction_vector[1] ** 2)
            if vector_length != 0:
                direction_vector = (direction_vector[0] / vector_length, direction_vector[1] / vector_length)

            enemy[0] += direction_vector[0] * ENEMY_SPEED * dt
            enemy[1] += direction_vector[1] * ENEMY_SPEED * dt

            pygame.draw.ellipse(screen, GREEN, (enemy[0], enemy[1], 30, 30))

        for turret in turrets:
            closest_enemy = find_closest_enemy(turret, enemies)
            turret.update_target(closest_enemy)
            turret.shoot()

        for turret in turrets:
            turret_x = turret.col * CELL_SIZE + CELL_SIZE // 2
            turret_y = turret.row * CELL_SIZE + CELL_SIZE // 2
            screen.blit(turret_img, (turret_x - TURRET_SIZE // 2 - 11, turret_y - TURRET_SIZE // 2 - 9))
            if turret.shoot_delay > 0:
                turret.shoot_delay -= 1

        for bullet in bullets:
            for enemy in enemies:
                enemy_center = (enemy[0] + 15, enemy[1] + 15)
                bullet_center = (bullet[0], bullet[2])
                distance = math.sqrt((bullet_center[0] - enemy_center[0]) ** 2 + (bullet_center[1] - enemy_center[1]) ** 2)
                if distance < 18:
                    enemies.remove(enemy)
                    score += score_increment
                    enemies_killed += 1

        if not game_over and not paused and not upgrade_menu_active:
            keys = pygame.key.get_pressed()
            if keys[pygame.K_w]:
                player_y -= PLAYER_SPEED * dt
                if player_y < 0:
                    player_y = 0
            if keys[pygame.K_s]:
                player_y += PLAYER_SPEED * dt
                if player_y > SCREEN_HEIGHT - PLAYER_SIZE:
                    player_y = SCREEN_HEIGHT - PLAYER_SIZE
            if keys[pygame.K_a]:
                player_x -= PLAYER_SPEED * dt
                if player_x < 0:
                    player_x = 0
            if keys[pygame.K_d]:
                player_x += PLAYER_SPEED * dt
                if player_x > SCREEN_WIDTH - PLAYER_SIZE:
                    player_x = SCREEN_WIDTH - PLAYER_SIZE
            if keys[pygame.K_q]:
                running = False
                pygame.quit()

        spawn_delay -= 1
        if spawn_delay <= 0:
            spawn_enemy()
            spawn_delay = ENEMY_SPAWN_DELAY

        if len(enemies) == 0 and ENEMY_SPAWN_DELAY >= 8:
            ENEMY_SPAWN_DELAY -= 3
            coin_count += 1
            spawn_enemy()
            cls_amount += 4
            score_increment += 0.1

        if enemies_killed >= enemies_killed_threshold <= 80:
            enemies_killed_threshold += 3
            coin_count += 1
            enemies_killed = 0

        elif enemies_killed >= enemies_killed_threshold >= 80:
            enemies_killed = 0
            coin_count += 1

        for enemy in enemies:
            if player_x < enemy[0] + 30 and player_x + PLAYER_SIZE > enemy[0] and player_y < enemy[1] + 30 and player_y + PLAYER_SIZE > enemy[1]:
                game_over = True

    else:
        if paused and not upgrade_menu_active and not turret_placement_mode and not turret_menu:
            screen.fill((255, 255, 255))
            screen.blit(pause_text, pause_rect)
            screen.blit(resume_button_text, resume_button_rect)
            screen.blit(upgrades_button_text, upgrades_button_rect)

        elif upgrade_menu_active and paused and not turret_menu:
            screen.fill((255, 255, 255))
            screen.blit(back_button_text, back_button_rect)
            screen.blit(rate_of_fire_button_text, rate_of_fire_button_rect)
            screen.blit(resume_button_text, resume_button_rect)
            screen.blit(pause_text, pause_rect)
            if not dual_shoot_enabled and not quad_shoot_enabled:
                screen.blit(dual_shoot_button_text, dual_shoot_button_rect)
            elif dual_shoot_enabled:
                screen.blit(quad_shoot_button_text, quad_shoot_button_rect)
            elif quad_shoot_enabled:
                screen.blit(quad_shoot_button_text, quad_shoot_button_rect)

            screen.blit(turret_menu_text, turret_menu_rect)
            screen.blit(bullet_speed_text, bullet_speed_rect)
            screen.blit(movement_speed_button_text, movement_speed_button_rect)

        elif turret_menu and paused and not upgrade_menu_active and not turret_placement_mode:
            screen.fill((255, 255, 255))
            screen.blit(pause_text, pause_rect)
            screen.blit(back_button_text, back_button_rect)
            screen.blit(resume_button_text, resume_button_rect)
            screen.blit(turret_button_text, turret_button_rect)
            screen.blit(turret_fire_button_text, turret_fire_button_rect)

        elif turret_placement_mode and paused and not upgrade_menu_active and not turret_menu:
            screen.fill((255, 255, 255))
            draw_grid()

            for turret in turrets:
                turret_x = turret.col * CELL_SIZE + CELL_SIZE // 2
                turret_y = turret.row * CELL_SIZE + CELL_SIZE // 2
                screen.blit(turret_img, (turret_x - TURRET_SIZE // 2-11, turret_y - TURRET_SIZE // 2-9))

            placement_message = font.render("Click on a grid cell to place a turret.", True, BLACK)
            placement_rect = placement_message.get_rect(center=(SCREEN_WIDTH // 2, 70))
            screen.blit(placement_message, placement_rect)

    if game_over:
        screen.fill(WHITE)
        text = font.render(f"Game Over", True, BLACK)
        text_rect = text.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2))
        screen.blit(text, text_rect)
        keys = pygame.key.get_pressed()
        if keys[pygame.K_q]:
            running = False
            pygame.quit()

    if paused:
        keys = pygame.key.get_pressed()
        if keys[pygame.K_q]:
            running = False
            pygame.quit()

    coin_font = pygame.font.Font(None, 36)
    coin_text = coin_font.render(f"Coins: {coin_count}", True, RED)
    coin_rect = coin_text.get_rect(topright=(SCREEN_WIDTH - 10, 10))

    screen.blit(coin_text, coin_rect)
    display_score(int(score))

    turret_shoot_delay -= 1
    bullet_delay -= 1
    pygame.display.update()

pygame.quit()
