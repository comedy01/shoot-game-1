import pygame
import math
import random
import os

pygame.init()

screen_width, screen_height = 800, 800

while True:
    player_size = 27
    player_speed = 150

    green_enemy_damage = 50
    yellow_enemy_damage = 100

    wants_to_quit = False

    bullet_speed = 600
    bullet_speed_cost = 1
    bullet_speed_upgrades = 6

    original_player_health = 100
    player_health = original_player_health
    health_upgrades = 6
    health_upgrade_cost = 1
    original_regen_delay = 800
    health_regen_delay = original_regen_delay
    health_regen_upgrades = 6
    health_regen_upgrade_cost = 1

    original_bullet_delay = 24
    bullet_delay = original_bullet_delay
    specialization_delay = 0
    original_auto_spawnrate_increase = 1300
    auto_spawnrate_increase = original_auto_spawnrate_increase

    green_enemy_speed = 100
    yellow_enemy_speed = 135
    green_enemy_spawn_delay = 55
    yellow_enemy_spawn_delay = 50
    enemy_spawn_distance = 250

    fire_upgrades = 6
    fire_upgrade_cost = 1

    quad_shoot_upgrades = 1
    quad_shoot_cost = 12
    has_chosen_quad_shoot = False

    turret_size = 20
    turret_fire_delay = 26
    turret_count = 1
    turret_fire_cost = 1
    turret_fire_upgrades = 6
    turret_placement_mode = False
    has_turret = False

    bullet_penetration_cost = 5

    grid_size = 6
    cell_size = screen_width // grid_size

    movement_speed_upgrades = 6
    movement_speed_cost = 1

    paused = False
    upgrade_menu_active = False
    running = True
    game_over = False
    selected_cell = None
    has_made_decision = False
    has_made_second_decision = False
    has_made_third_decision = False
    has_chosen_turrets = False
    has_chosen_dual_shoot = False
    has_chosen_twin_shoot = False
    has_chosen_double_twin_shoot = False
    has_chosen_triple_shoot = False
    has_bullet_penetration = False
    green_enemy_mode = True
    yellow_enemy_mode = False

    angle = 0
    spawn_delay = 0

    green_enemies_killed = 0
    green_enemies_killed_threshold = 7
    total_green_enemies_killed = 0
    total_yellow_enemies_killed = 0
    yellow_enemies_killed = 0
    yellow_enemies_killed_threshold = 14

    score = 0
    score_increment = 1
    coin_count = 0
    coin_delay = 800

    bullets = []
    turrets = []
    green_enemies = []
    yellow_enemies = []

    WHITE = (255, 255, 255)
    RED = (255, 0, 0)
    DARK_YELLOW = (105, 105, 30)
    GREEN = (0, 255, 0)
    BLACK = (0, 0, 0)

    screen = pygame.display.set_mode((screen_width, screen_height))
    pygame.display.set_caption("Shooting Game")

    player_img = pygame.image.load(os.path.join("Assets", "player.png"))

    bullet_img = pygame.Surface((10, 10))
    bullet_img.fill(RED)

    enemy_img = pygame.Surface((30, 30))
    enemy_img.fill(GREEN)

    player_x = screen_width // 2 - player_size // 2
    player_y = screen_height // 2 - player_size // 2

    clock = pygame.time.Clock()
    turret_img = pygame.image.load(os.path.join("Assets", "turret.png"))
    font = pygame.font.Font('Assets/Montserrat-Bold.ttf', 32)
    font_color = (255, 255, 255)
    font_position = (10, 10)

    pause_font = pygame.font.Font('Assets/Montserrat-Bold.ttf', 48)
    pause_text = pause_font.render("Paused", True, BLACK)
    pause_rect = pause_text.get_rect(center=(screen_width // 2, 25))

    specialization_font = pygame.font.Font('Assets/Montserrat-Bold.ttf', 25)
    specialization_text = specialization_font.render("You can now choose a specialization", True, BLACK)
    specialization_rect = specialization_text.get_rect(center=(screen_width // 2, 70))

    back_button_font = pygame.font.Font('Assets/Montserrat-Bold.ttf', 32)
    back_button_text = pause_font.render("Back", True, BLACK)
    back_button_rect = pause_text.get_rect(center=(screen_width // 2 + 20, 260))

    resume_button_font = pygame.font.Font('Assets/Montserrat-Bold.ttf', 36)
    resume_button_text = resume_button_font.render("Resume", True, BLACK)
    resume_button_rect = resume_button_text.get_rect(center=(screen_width // 2 - 10, 300))

    upgrades_button_font = pygame.font.Font('Assets/Montserrat-Bold.ttf', 36)
    upgrades_button_text = upgrades_button_font.render("Upgrades", True, BLACK)
    upgrades_button_rect = upgrades_button_text.get_rect(center=(screen_width // 2 - 10, 340))

    rate_of_fire_button_font = pygame.font.Font('Assets/Montserrat-Bold.ttf', 25)
    rate_of_fire_button_text = rate_of_fire_button_font.render(
        f"Fire rate ({fire_upgrade_cost} coins), {fire_upgrades} left", True, RED)
    rate_of_fire_button_rect = rate_of_fire_button_text.get_rect(topleft=(20, screen_height - 172))

    dual_shoot_button_font = pygame.font.Font('Assets/Montserrat-Bold.ttf', 30)
    dual_shoot_button_text = dual_shoot_button_font.render(f"Dual Shooter", True, RED)
    dual_shoot_button_rect = dual_shoot_button_text.get_rect(center=(screen_width // 2, 470))

    turret_button_font = pygame.font.Font('Assets/Montserrat-Bold.ttf', 30)
    turret_placement_mode_text = turret_button_font.render(f"Place a turret", True, RED)
    turret_placement_mode_rect = turret_placement_mode_text.get_rect(center=(screen_width // 2, 500))

    bullet_speed_font = pygame.font.Font('Assets/Montserrat-Bold.ttf', 25)
    bullet_speed_text = bullet_speed_font.render(
        f"Bullet Speed ({bullet_speed_cost} coins), {bullet_speed_upgrades} left", True, RED)
    bullet_speed_rect = bullet_speed_text.get_rect(topleft=(20, screen_height - 139))

    quad_shoot_button_font = pygame.font.Font('Assets/Montserrat-Bold.ttf', 30)
    quad_shoot_button_text = quad_shoot_button_font.render(f"Quad Shooter", True, RED)
    quad_shoot_button_rect = quad_shoot_button_text.get_rect(center=(screen_width // 2, 470))

    turret_gunner_font = pygame.font.Font('Assets/Montserrat-Bold.ttf', 30)
    turret_gunner_text = turret_gunner_font.render(f"Turret gunner", True, RED)
    turret_gunner_rect = turret_gunner_text.get_rect(center=(screen_width // 2, 500))

    twin_shooter_font = pygame.font.Font('Assets/Montserrat-Bold.ttf', 30)
    twin_shooter_text = twin_shooter_font.render(f"Twin Shooter", True, RED)
    twin_shooter_rect = twin_shooter_text.get_rect(center=(screen_width // 2, 530))

    double_twin_shooter_font = pygame.font.Font('Assets/Montserrat-Bold.ttf', 30)
    double_twin_shooter_text = double_twin_shooter_font.render(f"Double Twin Shooter", True, RED)
    double_twin_shooter_rect = double_twin_shooter_text.get_rect(center=(screen_width // 2, 500))

    triple_shooter_font = pygame.font.Font('Assets/Montserrat-Bold.ttf', 30)
    triple_shooter_text = triple_shooter_font.render(f"Triple Shooter", True, RED)
    triple_shooter_rect = triple_shooter_text.get_rect(center=(screen_width // 2, 530))

    turret_fire_button_font = pygame.font.Font('Assets/Montserrat-Bold.ttf', 25)
    turret_fire_button_text = turret_fire_button_font.render(
        f"Turret fire rate ({turret_fire_cost} coins), {turret_fire_upgrades} left", True, RED)
    turret_fire_button_rect = turret_fire_button_text.get_rect(topleft=(20, screen_height - 238))

    movement_speed_button_font = pygame.font.Font('Assets/Montserrat-Bold.ttf', 25)
    movement_speed_button_text = movement_speed_button_font.render(
        f"Movement speed ({movement_speed_cost} coins), {movement_speed_upgrades} left", True, RED)
    movement_speed_button_rect = movement_speed_button_text.get_rect(topleft=(20, screen_height - 106))

    health_button_font = pygame.font.Font('Assets/Montserrat-Bold.ttf', 25)
    health_button_text = health_button_font.render(f"Health ({health_upgrade_cost} coins), {health_upgrades} left",
                                                   True, RED)
    health_button_rect = health_button_text.get_rect(topleft=(20, screen_height - 73))

    health_regen_font = pygame.font.Font('Assets/Montserrat-Bold.ttf', 25)
    health_regen_text = health_regen_font.render(
        f"Health Regen ({health_regen_upgrade_cost} coins), {health_regen_upgrades} left", True, RED)
    health_regen_rect = health_regen_text.get_rect(topleft=(20, screen_height - 45))

    bottom_left_upgrades_font = pygame.font.Font('Assets/Montserrat-Bold.ttf', 32)
    bottom_left_upgrades_text = bottom_left_upgrades_font.render(f"Upgrades", True, RED)
    bottom_left_upgrades_rect = bottom_left_upgrades_text.get_rect(center=(97, screen_height - 238))

    bullet_penetration_font = pygame.font.Font('Assets/Montserrat-Bold.ttf', 25)
    bullet_penetration_text = bullet_penetration_font.render(
        f"Bullet penetration ({bullet_penetration_cost} coins), 1 left", True, RED)
    bullet_penetration_rect = bullet_penetration_text.get_rect(topleft=(20, screen_height - 205))


    def blit_screen():
        if paused and not upgrade_menu_active:
            screen.fill((255, 255, 255))
            screen.blit(pause_text, pause_rect)
            screen.blit(resume_button_text, resume_button_rect)
            screen.blit(upgrades_button_text, upgrades_button_rect)

        elif upgrade_menu_active and not has_made_decision and total_green_enemies_killed <= 150:
            screen.fill((255, 255, 255))
            screen.blit(back_button_text, back_button_rect)
            screen.blit(resume_button_text, resume_button_rect)
            screen.blit(pause_text, pause_rect)

        elif upgrade_menu_active and not has_made_decision and total_green_enemies_killed >= 150:
            screen.fill((255, 255, 255))
            screen.blit(back_button_text, back_button_rect)
            screen.blit(resume_button_text, resume_button_rect)
            screen.blit(pause_text, pause_rect)
            screen.blit(dual_shoot_button_text, dual_shoot_button_rect)
            screen.blit(turret_gunner_text, turret_gunner_rect)
            screen.blit(twin_shooter_text, twin_shooter_rect)
            screen.blit(turret_gunner_text, turret_gunner_rect)

        elif has_chosen_turrets and upgrade_menu_active:
            screen.fill((255, 255, 255))
            screen.blit(pause_text, pause_rect)
            screen.blit(back_button_text, back_button_rect)
            screen.blit(resume_button_text, resume_button_rect)
            screen.blit(turret_placement_mode_text, turret_placement_mode_rect)
            screen.blit(turret_fire_button_text, turret_fire_button_rect)

        elif has_chosen_dual_shoot and upgrade_menu_active and total_green_enemies_killed < 400:
            screen.fill((255, 255, 255))
            screen.blit(pause_text, pause_rect)
            screen.blit(back_button_text, back_button_rect)
            screen.blit(resume_button_text, resume_button_rect)

        elif has_chosen_twin_shoot and upgrade_menu_active and total_green_enemies_killed < 400:
            screen.fill((255, 255, 255))
            screen.blit(pause_text, pause_rect)
            screen.blit(back_button_text, back_button_rect)
            screen.blit(resume_button_text, resume_button_rect)

        elif has_chosen_twin_shoot and upgrade_menu_active and total_green_enemies_killed >= 400:
            screen.fill((255, 255, 255))
            screen.blit(pause_text, pause_rect)
            screen.blit(back_button_text, back_button_rect)
            screen.blit(resume_button_text, resume_button_rect)
            screen.blit(double_twin_shooter_text, double_twin_shooter_rect)
            screen.blit(triple_shooter_text, triple_shooter_rect)

        elif has_chosen_dual_shoot and upgrade_menu_active and total_green_enemies_killed >= 400:
            screen.fill((255, 255, 255))
            screen.blit(pause_text, pause_rect)
            screen.blit(back_button_text, back_button_rect)
            screen.blit(resume_button_text, resume_button_rect)
            screen.blit(quad_shoot_button_text, quad_shoot_button_rect)
            screen.blit(double_twin_shooter_text, double_twin_shooter_rect)

        elif has_chosen_quad_shoot and upgrade_menu_active:
            screen.fill((255, 255, 255))
            screen.blit(pause_text, pause_rect)
            screen.blit(back_button_text, back_button_rect)
            screen.blit(resume_button_text, resume_button_rect)

        elif has_chosen_double_twin_shoot and upgrade_menu_active:
            screen.fill((255, 255, 255))
            screen.blit(pause_text, pause_rect)
            screen.blit(back_button_text, back_button_rect)
            screen.blit(resume_button_text, resume_button_rect)

        elif has_chosen_triple_shoot and upgrade_menu_active:
            screen.fill((255, 255, 255))
            screen.blit(pause_text, pause_rect)
            screen.blit(back_button_text, back_button_rect)
            screen.blit(resume_button_text, resume_button_rect)

        if upgrade_menu_active:
            if not turret_placement_mode:
                screen.blit(bullet_speed_text, bullet_speed_rect)
                screen.blit(movement_speed_button_text, movement_speed_button_rect)
                screen.blit(health_button_text, health_button_rect)
                screen.blit(health_regen_text, health_regen_rect)
                screen.blit(bottom_left_upgrades_text, bottom_left_upgrades_rect)
                screen.blit(rate_of_fire_button_text, rate_of_fire_button_rect)
                screen.blit(bullet_penetration_text, bullet_penetration_rect)
            else:
                screen.fill(WHITE)
                placement_message = font.render("Click on a grid cell to place a turret.", True, BLACK)
                placement_rect = placement_message.get_rect(center=(screen_width // 2, 70))
                screen.blit(placement_message, placement_rect)
                draw_grid()
                for turret in turrets:
                    turret_x = turret.col * cell_size + cell_size // 2
                    turret_y = turret.row * cell_size + cell_size // 2
                    screen.blit(turret_img, (turret_x - turret_size // 2 - 11, turret_y - turret_size // 2 - 9))


    def start_screen():
        screen.fill((0, 255, 255))
        start_message = font.render("", True, (48, 93, 120))
        screen.blit(start_message, (screen.get_width() / 2 - start_message.get_width() / 2,
                                    screen.get_height() / 2 - start_message.get_height() / 2 - 40))
        starting_in = font.render(f"Starting in {start_time}", True, (48, 93, 120))
        screen.blit(starting_in, (
        screen.get_width() / 2 - starting_in.get_width() / 2, screen.get_height() / 2 - starting_in.get_height() / 2))
        skip_to_start = font.render("press space to skip timer", True, (48, 93, 120))
        screen.blit(skip_to_start, (screen.get_width() / 2 - skip_to_start.get_width() / 2,
                                    screen.get_height() / 2 - skip_to_start.get_height() / 2 + 40))
        pygame.display.update()
        pygame.time.delay(60)


    def draw_player_health_bar():
        pygame.draw.rect(screen, RED, (screen_width // 2 - player_health // 2, 30, player_health, 20))


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
                dx = self.target[0] - (self.col * cell_size + cell_size // 2)
                dy = self.target[1] - (self.row * cell_size + cell_size // 2)
                angle = math.degrees(math.atan2(dy, dx))
                bullets.append([self.col * cell_size + cell_size // 2, angle, self.row * cell_size + cell_size // 2])
                self.shoot_delay = turret_fire_delay


    def calculate_distance(point1, point2):
        x1, y1 = point1
        x2, y2 = point2
        return math.sqrt((x1 - x2) ** 2 + (y1 - y2) ** 2)


    def find_closest_enemy(turret, green_enemies):
        min_distance = float('inf')
        closest_enemy = None
        for enemy in green_enemies:
            enemy_center = (enemy[0] + 15, enemy[1] + 15)
            turret_center = (turret.col * cell_size + cell_size // 2, turret.row * cell_size + cell_size // 2)
            d = calculate_distance(enemy_center, turret_center)

            if d < min_distance:
                min_distance = d
                closest_enemy = enemy

        return closest_enemy


    def draw_grid():
        for row in range(grid_size):
            for col in range(grid_size):
                pygame.draw.rect(screen, (100, 100, 100), (col * cell_size, row * cell_size, cell_size, cell_size), 1)


    def place_turret(row, col):
        turrets.append(Turret(row, col))


    def spawn_green_enemy():
        while True:
            enemy_x = random.randint(0, screen_width - 30)
            enemy_y = random.randint(0, screen_height - 30)

            distance = math.sqrt((enemy_x - player_x) ** 2 + (enemy_y - player_y) ** 2)
            if distance >= enemy_spawn_distance:
                green_enemies.append([enemy_x, enemy_y])
                break


    def spawn_yellow_enemy():
        while True:
            enemy_x = random.randint(0, screen_width - 30)
            enemy_y = random.randint(0, screen_height - 30)

            distance = math.sqrt((enemy_x - player_x) ** 2 + (enemy_y - player_y) ** 2)
            if distance >= enemy_spawn_distance:
                yellow_enemies.append([enemy_x, enemy_y])
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

        start_screen()

    while running:
        dt = clock.tick(60) / 1000

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    if not paused:
                        paused = True

                    elif upgrade_menu_active:
                        upgrade_menu_active = False
                        turret_placement_mode = False

                    elif turret_placement_mode:
                        turret_placement_mode = False
                        upgrade_menu_active = True
                        has_chosen_turrets = True

                    elif paused:
                        paused = False

            if event.type == pygame.MOUSEBUTTONDOWN and has_chosen_turrets:
                if back_button_rect.collidepoint(event.pos):
                    upgrade_menu_active = True
                    paused = True

                elif turret_placement_mode_rect.collidepoint(event.pos) and has_chosen_turrets:
                    turret_placement_mode = True

                elif turret_fire_button_rect.collidepoint(event.pos) and has_turret and turret_fire_upgrades > 0:
                    coin_count -= turret_fire_cost
                    turret_fire_delay -= 2
                    turret_fire_upgrades -= 1
                    turret_fire_button_rect = turret_fire_button_text.get_rect(topleft=(20, screen_height - 238))
                    turret_fire_button_text = turret_fire_button_font.render(
                        f"Turret fire rate ({turret_fire_cost} coins), {turret_fire_upgrades} left", True, RED)

                elif resume_button_rect.collidepoint(event.pos):
                    paused = False
                    upgrade_menu_active = False

            if event.type == pygame.MOUSEBUTTONDOWN and paused:
                if resume_button_rect.collidepoint(event.pos):
                    paused = not paused

                elif upgrades_button_rect.collidepoint(event.pos) and not has_made_decision:
                    upgrade_menu_active = True
                    paused = True

                elif upgrades_button_rect.collidepoint(event.pos) and has_made_decision:
                    upgrade_menu_active = True

            if event.type == pygame.MOUSEBUTTONDOWN and upgrade_menu_active:
                if resume_button_rect.collidepoint(event.pos):
                    upgrade_menu_active = False
                    paused = False

                elif back_button_rect.collidepoint(event.pos):
                    upgrade_menu_active = False

                elif turret_gunner_rect.collidepoint(
                        event.pos) and not has_made_decision and total_green_enemies_killed > 150:
                    upgrade_menu_active = True
                    has_chosen_turrets = True
                    has_made_decision = True
                    bottom_left_upgrades_rect = bottom_left_upgrades_text.get_rect(center=(97, screen_height - 256))

                elif rate_of_fire_button_rect.collidepoint(event.pos):
                    if fire_upgrades > 0 and coin_count >= fire_upgrade_cost:
                        coin_count -= fire_upgrade_cost
                        original_bullet_delay -= 2
                        fire_upgrades -= 1
                        rate_of_fire_button_text = rate_of_fire_button_font.render(
                            f"Fire rate ({fire_upgrade_cost} coins), {fire_upgrades} left", True, RED)

                elif dual_shoot_button_rect.collidepoint(
                        event.pos) and not has_made_decision and total_green_enemies_killed >= 150:
                    upgrade_menu_active = True
                    has_made_decision = True
                    has_chosen_dual_shoot = True

                elif twin_shooter_rect.collidepoint(
                        event.pos) and not has_made_decision and total_green_enemies_killed >= 150:
                    upgrade_menu_active = True
                    has_made_decision = True
                    has_chosen_twin_shoot = True
                    original_bullet_delay += 5

                elif quad_shoot_button_rect.collidepoint(
                        event.pos) and has_chosen_dual_shoot and total_green_enemies_killed >= 400:
                    upgrade_menu_active = True
                    has_chosen_quad_shoot = True
                    has_chosen_dual_shoot = False
                    has_made_second_decision = True

                elif double_twin_shooter_rect.collidepoint(
                        event.pos) and has_chosen_dual_shoot and total_green_enemies_killed >= 400:
                    upgrade_menu_active = True
                    has_chosen_double_twin_shoot = True
                    has_chosen_dual_shoot = False
                    has_made_second_decision = True

                elif triple_shooter_rect.collidepoint(
                        event.pos) and has_chosen_twin_shoot and total_green_enemies_killed >= 400:
                    upgrade_menu_active = True
                    has_chosen_twin_shoot = False
                    has_chosen_triple_shoot = True
                    has_made_second_decision = True
                    original_bullet_delay += 2

                elif double_twin_shooter_rect.collidepoint(
                        event.pos) and has_chosen_twin_shoot and total_green_enemies_killed >= 400:
                    upgrade_menu_active = True
                    has_chosen_double_twin_shoot = True
                    has_chosen_twin_shoot = False
                    original_bullet_delay += 3
                    has_made_second_decision = True

                elif bullet_speed_rect.collidepoint(
                        event.pos) and coin_count >= bullet_speed_cost and bullet_speed_upgrades > 0:
                    coin_count -= bullet_speed_cost
                    bullet_speed_upgrades -= 1
                    bullet_speed += 100
                    bullet_speed_text = bullet_speed_font.render(
                        f"Bullet Speed ({bullet_speed_cost} coins), {bullet_speed_upgrades} left", True, RED)

                elif movement_speed_button_rect.collidepoint(
                        event.pos) and coin_count >= movement_speed_cost and movement_speed_upgrades > 0:
                    player_speed = player_speed * 1.05
                    coin_count -= movement_speed_cost
                    movement_speed_upgrades -= 1
                    movement_speed_button_text = movement_speed_button_font.render(
                        f"Movement speed ({movement_speed_cost} coins), {movement_speed_upgrades} left", True, RED)

                elif health_button_rect.collidepoint(
                        event.pos) and coin_count >= health_upgrade_cost and health_upgrades > 0:
                    original_player_health += 30
                    coin_count -= health_upgrade_cost
                    health_upgrades -= 1
                    health_button_text = health_button_font.render(
                        f"Health ({health_upgrade_cost} coins), {health_upgrades} left", True, RED)

                elif health_regen_rect.collidepoint(
                        event.pos) and coin_count >= health_regen_upgrade_cost and health_regen_upgrades > 0:
                    original_regen_delay -= 100
                    coin_count -= health_regen_upgrade_cost
                    health_regen_upgrades -= 1
                    health_regen_text = health_regen_font.render(
                        f"Health Regen ({health_regen_upgrade_cost} coins), {health_regen_upgrades} left", True, RED)

                elif bullet_penetration_rect.collidepoint(
                        event.pos) and coin_count >= bullet_penetration_cost and has_bullet_penetration == False:
                    coin_count -= bullet_penetration_cost
                    has_bullet_penetration = True
                    bullet_penetration_text = bullet_penetration_font.render(
                        f"Bullet penetration ({bullet_penetration_cost} coins), 0 left", True, RED)

            if event.type == pygame.MOUSEBUTTONDOWN and turret_placement_mode and has_chosen_turrets and upgrade_menu_active:
                if not turret_placement_mode_rect.collidepoint(event.pos):
                    row = event.pos[1] // cell_size
                    col = event.pos[0] // cell_size

                    if (row, col) not in [(turret.row, turret.col) for turret in turrets] and turret_count >= 1:
                        place_turret(row, col)
                        new_turret = Turret(row, col)
                        turrets.append(new_turret)
                        turret_count -= 1
                        has_turret = True

        bullet_key = pygame.key.get_pressed()
        if bullet_key[pygame.K_SPACE] and bullet_delay <= 0:
            if has_chosen_dual_shoot:
                bullets.append([player_x + player_size // 2, angle, player_y + player_size // 2])
                bullets.append([player_x + player_size // 2, angle + 180, player_y + player_size // 2])

            elif has_chosen_quad_shoot:
                bullets.append([player_x + player_size // 2, angle, player_y + player_size // 2])
                bullets.append([player_x + player_size // 2, angle + 90, player_y + player_size // 2])
                bullets.append([player_x + player_size // 2, angle + 180, player_y + player_size // 2])
                bullets.append([player_x + player_size // 2, angle + 270, player_y + player_size // 2])

            elif has_chosen_twin_shoot:
                angle -= 8
                bullets.append([player_x + player_size // 2, angle, player_y + player_size // 2])
                angle += 16
                bullets.append([player_x + player_size // 2, angle, player_y + player_size // 2])

            elif has_chosen_double_twin_shoot:
                angle -= 8
                bullets.append([player_x + player_size // 2, angle, player_y + player_size // 2])
                angle += 16
                bullets.append([player_x + player_size // 2, angle, player_y + player_size // 2])
                angle += 172
                bullets.append([player_x + player_size // 2, angle, player_y + player_size // 2])
                angle -= 16
                bullets.append([player_x + player_size // 2, angle, player_y + player_size // 2])

            elif has_chosen_triple_shoot:
                bullets.append([player_x + player_size // 2, angle, player_y + player_size // 2])
                angle -= 10
                bullets.append([player_x + player_size // 2, angle, player_y + player_size // 2])
                angle += 20
                bullets.append([player_x + player_size // 2, angle, player_y + player_size // 2])

            else:
                bullets.append([player_x + player_size // 2, angle, player_y + player_size // 2])
            bullet_delay = original_bullet_delay

        if not game_over and not paused and not upgrade_menu_active:
            mouse_x, mouse_y = pygame.mouse.get_pos()

            angle = math.atan2(mouse_y - player_y - player_size // 2, mouse_x - player_x - player_size // 2)
            angle = math.degrees(angle)

            player_rotated = pygame.transform.rotate(player_img, -angle)
            player_rect = player_rotated.get_rect(center=(player_x + player_size // 2, player_y + player_size // 2))
            screen.fill(WHITE)
            screen.blit(player_rotated, player_rect.topleft)

            for bullet in bullets:
                bullet[0] += math.cos(math.radians(bullet[1])) * bullet_speed * dt
                bullet[2] += math.sin(math.radians(bullet[1])) * bullet_speed * dt
                pygame.draw.circle(screen, RED, (int(bullet[0]), int(bullet[2])), 5)

            bullets = [bullet for bullet in bullets if
                       0 <= bullet[0] <= screen_width and 0 <= bullet[2] <= screen_height]

            if green_enemy_mode:
                for enemy in green_enemies:
                    enemy_center = (enemy[0] + 15, enemy[1] + 15)
                    player_center = (player_x + player_size // 2, player_y + player_size // 2)

                    direction_vector = (player_center[0] - enemy_center[0], player_center[1] - enemy_center[1])

                    vector_length = math.sqrt(direction_vector[0] ** 2 + direction_vector[1] ** 2)
                    if vector_length != 0:
                        direction_vector = (direction_vector[0] / vector_length, direction_vector[1] / vector_length)

                    enemy[0] += direction_vector[0] * green_enemy_speed * dt
                    enemy[1] += direction_vector[1] * green_enemy_speed * dt

                    pygame.draw.ellipse(screen, GREEN, (enemy[0], enemy[1], 35, 35))
            elif yellow_enemy_mode:
                for enemy in yellow_enemies:
                    enemy_center = (enemy[0] + 15, enemy[1] + 15)
                    player_center = (player_x + player_size // 2, player_y + player_size // 2)

                    direction_vector = (player_center[0] - enemy_center[0], player_center[1] - enemy_center[1])

                    vector_length = math.sqrt(direction_vector[0] ** 2 + direction_vector[1] ** 2)
                    if vector_length != 0:
                        direction_vector = (direction_vector[0] / vector_length, direction_vector[1] / vector_length)

                    enemy[0] += direction_vector[0] * yellow_enemy_speed * dt
                    enemy[1] += direction_vector[1] * yellow_enemy_speed * dt

                    pygame.draw.ellipse(screen, DARK_YELLOW, (enemy[0], enemy[1], 30, 30))

            if green_enemy_mode:
                for turret in turrets:
                    closest_enemy = find_closest_enemy(turret, green_enemies)
                    turret.update_target(closest_enemy)
                    turret.shoot()
            elif yellow_enemy_mode:
                for turret in turrets:
                    closest_enemy = find_closest_enemy(turret, yellow_enemies)
                    turret.update_target(closest_enemy)
                    turret.shoot()

            for turret in turrets:
                turret_x = turret.col * cell_size + cell_size // 2
                turret_y = turret.row * cell_size + cell_size // 2
                screen.blit(turret_img, (turret_x - turret_size // 2 - 11, turret_y - turret_size // 2 - 9))
                if turret.shoot_delay > 0:
                    turret.shoot_delay -= 1

            for bullet in bullets:
                if green_enemy_mode:
                    for enemy in green_enemies:
                        enemy_center = (enemy[0] + 15, enemy[1] + 15)
                        bullet_center = (bullet[0], bullet[2])
                        distance = math.sqrt(
                            (bullet_center[0] - enemy_center[0]) ** 2 + (bullet_center[1] - enemy_center[1]) ** 2)
                        if distance < 21:
                            green_enemies.remove(enemy)
                            score += score_increment
                            green_enemies_killed += 1
                            total_green_enemies_killed += 1
                            if not has_bullet_penetration:
                                if bullet in bullets:
                                    bullets.remove(bullet)

                elif yellow_enemy_mode:
                    for enemy in yellow_enemies:
                        enemy_center = (enemy[0] + 15, enemy[1] + 15)
                        bullet_center = (bullet[0], bullet[2])
                        distance = math.sqrt(
                            (bullet_center[0] - enemy_center[0]) ** 2 + (bullet_center[1] - enemy_center[1]) ** 2)
                        if distance < 18:
                            yellow_enemies.remove(enemy)
                            score += score_increment
                            yellow_enemies_killed += 1
                            total_yellow_enemies_killed += 1
                            if not has_bullet_penetration:
                                if bullet in bullets:
                                    bullets.remove(bullet)

            if not game_over and not paused:
                keys = pygame.key.get_pressed()
                if keys[pygame.K_w]:
                    player_y -= player_speed * dt
                    if player_y < 0:
                        player_y = 0
                if keys[pygame.K_s]:
                    player_y += player_speed * dt
                    if player_y > screen_height - player_size:
                        player_y = screen_height - player_size
                if keys[pygame.K_a]:
                    player_x -= player_speed * dt
                    if player_x < 0:
                        player_x = 0
                if keys[pygame.K_d]:
                    player_x += player_speed * dt
                    if player_x > screen_width - player_size:
                        player_x = screen_width - player_size
                if keys[pygame.K_q]:
                    running = False
                    pygame.quit()
                if keys[pygame.K_r]:
                    running = False

            if player_health <= 0:
                game_over = True

            spawn_delay -= 1
            if green_enemy_mode:
                if spawn_delay <= 0 and green_enemy_mode:
                    spawn_green_enemy()
                    spawn_delay = green_enemy_spawn_delay
            elif yellow_enemy_mode:
                if spawn_delay <= 0 and yellow_enemy_mode:
                    spawn_yellow_enemy()
                    spawn_delay = yellow_enemy_spawn_delay

            if len(green_enemies) == 0 and green_enemy_spawn_delay >= 20 and green_enemy_mode:
                green_enemy_spawn_delay -= 5
                spawn_green_enemy()
                score_increment += 0.1
            elif len(yellow_enemies) == 0 and yellow_enemy_spawn_delay >= 20 and yellow_enemy_mode:
                yellow_enemy_spawn_delay -= 5
                spawn_yellow_enemy()
                score_increment += 0.1

            if green_enemy_mode:
                if green_enemies_killed >= green_enemies_killed_threshold:
                    green_enemies_killed_threshold += 1
                    green_enemies_killed = 0
                    coin_count += 1
            elif yellow_enemy_mode:
                if yellow_enemies_killed >= yellow_enemies_killed_threshold:
                    yellow_enemies_killed_threshold += 1
                    yellow_enemies_killed = 0
                    coin_count += 1

            if green_enemy_mode:
                for enemy in green_enemies:
                    if player_x < enemy[0] + 30 and player_x + player_size > enemy[0] and player_y < enemy[
                        1] + 30 and player_y + player_size > enemy[1]:
                        player_health -= green_enemy_damage
                        green_enemies.remove(enemy)
            elif yellow_enemy_mode:
                for enemy in yellow_enemies:
                    if player_x < enemy[0] + 30 and player_x + player_size > enemy[0] and player_y < enemy[
                        1] + 30 and player_y + player_size > enemy[1]:
                        player_health -= yellow_enemy_damage
                        yellow_enemies.remove(enemy)

            if player_health < original_player_health and health_regen_delay <= 0:
                player_health += 10
                health_regen_delay = original_regen_delay

            if auto_spawnrate_increase <= 0:
                if green_enemy_mode:
                    if green_enemy_spawn_delay <= 25:
                        green_enemy_spawn_delay -= 2
                        auto_spawnrate_increase = original_auto_spawnrate_increase
                    else:
                        green_enemy_spawn_delay -= 5
                        auto_spawnrate_increase = original_auto_spawnrate_increase
                    print("spawn rate increased")
                if yellow_enemy_mode:
                    if yellow_enemy_spawn_delay <= 25:
                        yellow_enemy_spawn_delay -= 2
                        auto_spawnrate_increase = original_auto_spawnrate_increase
                    else:
                        yellow_enemy_spawn_delay -= 5
                        auto_spawnrate_increase = original_auto_spawnrate_increase

        else:
            blit_screen()

        if game_over:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    wants_to_quit = True
                    running = False
            screen.fill(WHITE)
            text = font.render(f"Game Over", True, BLACK)
            text_rect = text.get_rect(center=(screen_width // 2, screen_height // 2))
            screen.blit(text, text_rect)
            keys = pygame.key.get_pressed()
            if keys[pygame.K_q]:
                wants_to_quit = True
                running = False
            if keys[pygame.K_r]:
                running = False

        if not paused and not game_over:
            draw_player_health_bar()

        if total_green_enemies_killed >= 150 and not has_made_decision:
            screen.blit(specialization_text, specialization_rect)
        elif total_green_enemies_killed >= 400 and not has_made_second_decision:
            screen.blit(specialization_text, specialization_rect)

        if paused:
            keys = pygame.key.get_pressed()
            if keys[pygame.K_q]:
                wants_to_quit = True
                running = False

        coin_font = pygame.font.Font('Assets/Montserrat-Bold.ttf', 36)
        coin_text = coin_font.render(f"Coins: {coin_count}", True, RED)
        coin_rect = coin_text.get_rect(topright=(screen_width - 10, 10))

        screen.blit(coin_text, coin_rect)
        display_score(int(score))

        if total_green_enemies_killed > 400:
            yellow_enemy_mode = True
            green_enemy_mode = False

        print(green_enemy_spawn_delay)

        auto_spawnrate_increase -= 1
        bullet_delay -= 1
        health_regen_delay -= 1
        pygame.display.update()

    if wants_to_quit:
        pygame.quit()
        quit()
