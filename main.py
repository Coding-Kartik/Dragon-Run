import pygame
from sys import exit
from random import randint


def obstacle_movement(obstacle_list, obstacle_speed):
    if obstacle_list:
        for obstacle_rect in obstacle_list:
            obstacle_rect.x -= obstacle_speed

            if obstacle_rect.bottom == 550:
                screen.blit(monster_surface, obstacle_rect)
            else:
                screen.blit(fly_surface, obstacle_rect)

        # Remove obstacles that are out of the screen
        obstacle_list = [obstacle for obstacle in obstacle_list if obstacle.x > -70]

    return obstacle_list


def display_score():
    current_time = int(pygame.time.get_ticks() / 1000) - start_time
    score_surface = text_font.render(f'Score: {current_time}', False, 'Black')
    score_rect = score_surface.get_rect(center=(580, 70))
    screen.blit(score_surface, score_rect)
    return current_time


def collision(player, obstacles):
    if obstacles:
        for obstacle_rect in obstacles:
            if player.colliderect(obstacle_rect):
                return False
    return True


pygame.init()
screen = pygame.display.set_mode((1200, 750))
pygame.display.set_caption('Runner')
clock = pygame.time.Clock()
game_active = False
text_font = pygame.font.Font('font/waltograph42.otf', 50)

# Load and resize surfaces
sky_surface = pygame.image.load('graphics/background.png').convert()
ground_surface = pygame.image.load('graphics/download.png').convert()
ground_rect = ground_surface.get_rect(midbottom=(0, 520))

# Resize player and obstacle images
player_surface = pygame.image.load('graphics/player.png').convert_alpha()
player_surface = pygame.transform.scale(player_surface, (80, 90))  # Resize player image
player_rect = player_surface.get_rect(midbottom=(80, 520))

monster_surface = pygame.image.load('graphics/plant.png').convert_alpha()
monster_surface = pygame.transform.scale(monster_surface, (70, 60))  # Resize monster image
fly_surface = pygame.image.load('graphics/fly.png').convert_alpha()
fly_surface = pygame.transform.scale(fly_surface, (70, 60))  # Resize fly image

# Initialize obstacle list
obstacle_rect_list = []

# Intro Screen
player_stand = pygame.image.load('graphics/player.png').convert_alpha()
player_stand = pygame.transform.scale(player_stand, (110, 100))  # Resize player stand image
player_stand = pygame.transform.rotozoom(player_stand, 0, 2)
player_stand_rect = player_stand.get_rect(center=(620, 420))

game_name = text_font.render('DRAGON RUN', True, (111, 196, 169))
game_name = pygame.transform.rotozoom(game_name, 0, 2)
game_name_rect = game_name.get_rect(center=(620, 140))

game_message = text_font.render("Click Space To Run", False, (111, 196, 169))
game_message_rect = game_message.get_rect(center=(620, 620))

# Timer
obstacle_timer = pygame.USEREVENT + 1
pygame.time.set_timer(obstacle_timer, 800)
start_time = 0
score = 0
player_gravity = 0

# Initial speed of obstacles
initial_obstacle_speed = 11
obstacle_speed = initial_obstacle_speed

while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            exit()

        if game_active:
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE and player_rect.bottom >= 520:
                    player_gravity = -20

            if event.type == obstacle_timer:
                if randint(0, 2):
                    obstacle_rect_list.append(monster_surface.get_rect(bottomright=(randint(1400, 1600), 550)))
                else:
                    obstacle_rect_list.append(fly_surface.get_rect(bottomright=(randint(1400, 1600), 250)))

        else:
            if event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE:
                game_active = True
                start_time = int(pygame.time.get_ticks() / 1000)
                obstacle_speed = initial_obstacle_speed  # Reset speed when starting a new game

    if game_active:
        screen.blit(sky_surface, (0, 0))
        screen.blit(ground_surface, (0, 520))

        score = display_score()

        # Increase speed every 10 score
        if score % 10 == 0 and score > 0:
            obstacle_speed += 0.05

        # Player movement
        player_gravity += 1
        player_rect.y += player_gravity
        if player_rect.bottom >= 520:
            player_rect.bottom = 520
        screen.blit(player_surface, player_rect)

        # Obstacle movement
        obstacle_rect_list = obstacle_movement(obstacle_rect_list, obstacle_speed)

        # Collision check
        game_active = collision(player_rect, obstacle_rect_list)

    else:
        screen.fill((9, 129, 162))
        screen.blit(player_stand, player_stand_rect)
        obstacle_rect_list.clear()

        score_message = text_font.render(f'Your Score: {score}', False, (111, 196, 169))
        score_message_rect = score_message.get_rect(center=(620, 620))

        screen.blit(game_name, game_name_rect)
        if score == 0:
            screen.blit(game_message, game_message_rect)
        else:
            screen.blit(score_message, score_message_rect)

    pygame.display.update()
    clock.tick(60)
