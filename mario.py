import pygame
import math

# Initialize Pygame
pygame.init()

# Screen dimensions
SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Doom-like Raycasting with Floor, Ceiling, and Wall Barriers")

# Colors
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
GRAY = (169, 169, 169)
FLOOR_COLOR = (50, 50, 50)
CEILING_COLOR = (100, 100, 100)

# Map settings
MAP_WIDTH = 10
MAP_HEIGHT = 10
MAP = [
    '##########',
    '#........#',
    '#..##....#',
    '#........#',
    '#...##...#',
    '#........#',
    '#...##...#',
    '#........#',
    '#........#',
    '##########'
]

TILE_SIZE = 64
FOV = math.pi / 3  # Field of View (60 degrees)
HALF_FOV = FOV / 2
NUM_RAYS = 120
MAX_DEPTH = 800
DELTA_ANGLE = FOV / NUM_RAYS
DISTANCE_PROJ_PLANE = (SCREEN_WIDTH // 2) / math.tan(HALF_FOV)
SCALE = SCREEN_WIDTH // NUM_RAYS

# Player settings
player_pos = [SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2]
player_angle = math.pi / 4
player_speed = 3
player_radius = 20  # Collision radius for the player

# Jump settings
is_jumping = False
jump_speed = -10  # Negative for upward movement
gravity = 0.5
fall_speed = 0
jump_height = SCREEN_HEIGHT // 2

# Disable mouse movement
pygame.mouse.set_visible(False)  # Hide the mouse cursor

def draw_map():
    for y, row in enumerate(MAP):
        for x, char in enumerate(row):
            if char == '#':
                pygame.draw.rect(screen, GRAY, (x * TILE_SIZE, y * TILE_SIZE, TILE_SIZE, TILE_SIZE))

def cast_rays():
    start_angle = player_angle - HALF_FOV
    for ray in range(NUM_RAYS):
        current_angle = start_angle + ray * DELTA_ANGLE
        depth = 0
        while depth < MAX_DEPTH:
            target_x = player_pos[0] + depth * math.cos(current_angle)
            target_y = player_pos[1] + depth * math.sin(current_angle)

            col, row = int(target_x / TILE_SIZE), int(target_y / TILE_SIZE)

            if MAP[row][col] == '#':
                depth *= math.cos(player_angle - current_angle)  # Remove fish-eye effect

                proj_height = TILE_SIZE / (depth + 0.0001) * DISTANCE_PROJ_PLANE
                color = 255 / (1 + depth * depth * 0.0001)
                wall_top = SCREEN_HEIGHT // 2 - proj_height // 2
                wall_bottom = SCREEN_HEIGHT // 2 + proj_height // 2
                pygame.draw.rect(screen, (color, color, color),
                                 (ray * SCALE, wall_top, SCALE, proj_height))

                # Draw the floor and ceiling
                pygame.draw.rect(screen, FLOOR_COLOR,
                                 (ray * SCALE, wall_bottom, SCALE, SCREEN_HEIGHT - wall_bottom))
                pygame.draw.rect(screen, CEILING_COLOR,
                                 (ray * SCALE, 0, SCALE, wall_top))
                break

            depth += 1

def move_player():
    global player_angle, player_pos, is_jumping, fall_speed

    keys = pygame.key.get_pressed()
    move_x, move_y = 0, 0

    if keys[pygame.K_w]:
        move_x = player_speed * math.cos(player_angle)
        move_y = player_speed * math.sin(player_angle)
    if keys[pygame.K_s]:
        move_x = -player_speed * math.cos(player_angle)
        move_y = -player_speed * math.sin(player_angle)
    if keys[pygame.K_d]:
        strafe_x = player_speed * math.cos(player_angle + math.pi / 2)
        strafe_y = player_speed * math.sin(player_angle + math.pi / 2)
        move_x += strafe_x
        move_y += strafe_y
    if keys[pygame.K_a]:
        strafe_x = player_speed * math.cos(player_angle - math.pi / 2)
        strafe_y = player_speed * math.sin(player_angle - math.pi / 2)
        move_x += strafe_x
        move_y += strafe_y

    # Check for collisions
    new_x = player_pos[0] + move_x
    new_y = player_pos[1] + move_y

    grid_x = int(new_x / TILE_SIZE)
    grid_y = int(new_y / TILE_SIZE)
    if 0 <= grid_x < MAP_WIDTH and 0 <= grid_y < MAP_HEIGHT:
        if MAP[grid_y][grid_x] != '#':
            player_pos[0] = new_x
            player_pos[1] = new_y

    # Handle jumping
    if is_jumping:
        fall_speed += gravity
        player_pos[1] += fall_speed
        if player_pos[1] >= jump_height:
            player_pos[1] = jump_height
            is_jumping = False
            fall_speed = 0

def draw_floor_and_ceiling():
    pygame.draw.rect(screen, CEILING_COLOR, (0, 0, SCREEN_WIDTH, SCREEN_HEIGHT // 2))
    pygame.draw.rect(screen, FLOOR_COLOR, (0, SCREEN_HEIGHT // 2, SCREEN_WIDTH, SCREEN_HEIGHT // 2))

def handle_keyboard():
    global player_angle, is_jumping

    keys = pygame.key.get_pressed()
    if keys[pygame.K_LEFT]:
        player_angle -= 0.05  # Turn left
    if keys[pygame.K_RIGHT]:
        player_angle += 0.05  # Turn right
    if keys[pygame.K_SPACE]:
        if not is_jumping:
            is_jumping = True
            fall_speed = jump_speed

# Main game loop
running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    handle_keyboard()
    move_player()

    screen.fill(BLACK)
    draw_map()
    draw_floor_and_ceiling()
    cast_rays()

    pygame.display.flip()
    pygame.time.Clock().tick(60)

pygame.quit()
