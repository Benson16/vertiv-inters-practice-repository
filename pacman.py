import pygame
import random

# Initialize pygame
pygame.init()

# Screen dimensions
width, height = 600, 600
screen = pygame.display.set_mode((width, height))

# Colors
black = (0, 0, 0)
white = (255, 255, 255)
yellow = (255, 255, 0)
blue = (0, 0, 255)
red = (255, 0, 0)  # Color for the monsters

# Define the clock
clock = pygame.time.Clock()

# Player (Pac-Man) settings
player_size = 20
block_size = width // 20  

player_x = block_size + block_size // 2 - player_size // 2
player_y = block_size + block_size // 2 - player_size // 2
player_speed = 5

# Dot settings
dot_size = 10

# Monster settings
monster_size = 20
monster_speed = 3

# Maze layout (1 represents walls, 0 represents paths)
maze = [
    [1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1],
    [1, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 1],
    [1, 0, 1, 1, 0, 1, 0, 1, 1, 1, 1, 1, 0, 1, 0, 1, 1, 1, 0, 1],
    [1, 0, 1, 0, 0, 0, 0, 1, 0, 0, 0, 1, 0, 0, 0, 0, 0, 1, 0, 1],
    [1, 0, 1, 0, 1, 1, 1, 1, 0, 1, 0, 1, 1, 1, 1, 1, 0, 1, 0, 1],
    [1, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1],
    [1, 0, 1, 1, 1, 1, 1, 1, 0, 1, 0, 1, 1, 1, 1, 1, 1, 1, 0, 1],
    [1, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1],
    [1, 1, 1, 1, 1, 1, 0, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1],
    [1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1],
    [1, 1, 0, 1, 1, 1, 1, 1, 1, 1, 0, 1, 1, 1, 1, 0, 1, 1, 1, 1],
    [1, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 1],
    [1, 0, 1, 1, 0, 1, 0, 1, 1, 1, 1, 1, 0, 1, 0, 1, 1, 1, 0, 1],
    [1, 0, 1, 0, 0, 0, 0, 1, 0, 0, 0, 1, 0, 0, 0, 0, 0, 1, 0, 1],
    [1, 0, 1, 0, 1, 1, 1, 1, 0, 1, 0, 1, 1, 1, 1, 1, 0, 1, 0, 1],
    [1, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1],
    [1, 0, 1, 1, 1, 1, 0, 1, 0, 1, 0, 1, 1, 1, 1, 1, 1, 0, 0, 1],
    [1, 0, 0, 0, 1, 0, 0, 1, 0, 1, 0, 0, 0, 0, 0, 0, 1, 0, 0, 1],
    [1, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 1, 0, 1, 0, 0, 0, 1, 1],
    [1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1],
]

# Generate dots within the maze paths
def generate_dots():
    return [(x * block_size, y * block_size) 
            for y, row in enumerate(maze) 
            for x, block in enumerate(row) 
            if block == 0 and random.random() < 0.2]  # Adjust the density with the probability

dots = generate_dots()

# Function to draw the maze
def draw_maze():
    for y, row in enumerate(maze):
        for x, block in enumerate(row):
            if block == 1:
                pygame.draw.rect(screen, blue, (x * block_size, y * block_size, block_size, block_size))

def detect_wall_collision(x, y, size):
    # Check all four corners of Pac-Man
    for dx in [0, size]:
        for dy in [0, size]:
            grid_x, grid_y = (x + dx) // block_size, (y + dy) // block_size
            # Ensure grid_x and grid_y are within valid range
            if grid_x < 0 or grid_x >= len(maze[0]) or grid_y < 0 or grid_y >= len(maze):
                return True  # Treat out-of-bounds as a collision
            if maze[grid_y][grid_x] == 1:
                return True
    return False

def collect_dots(player_rect):
    global dots
    collected = 0
    new_dots = []
    for dot in dots:
        dot_rect = pygame.Rect(dot[0], dot[1], dot_size, dot_size)
        if player_rect.colliderect(dot_rect):
            collected += 1
        else:
            new_dots.append(dot)
    dots = new_dots
    return collected

def move_monster(monster_x, monster_y, player_x, player_y):
    if monster_x < player_x:
        if not detect_wall_collision(monster_x + monster_speed, monster_y, monster_size):
            monster_x += monster_speed
    elif monster_x > player_x:
        if not detect_wall_collision(monster_x - monster_speed, monster_y, monster_size):
            monster_x -= monster_speed

    if monster_y < player_y:
        if not detect_wall_collision(monster_x, monster_y + monster_speed, monster_size):
            monster_y += monster_speed
    elif monster_y > player_y:
        if not detect_wall_collision(monster_x, monster_y - monster_speed, monster_size):
            monster_y -= monster_speed

    return monster_x, monster_y

def detect_monster_collision(monster_x, monster_y, player_x, player_y, size):
    monster_rect = pygame.Rect(monster_x, monster_y, size, size)
    player_rect = pygame.Rect(player_x, player_y, size, size)
    return monster_rect.colliderect(player_rect)

# Initialize monster positions
monster1_x, monster1_y = width // 2, height // 2
monster2_x, monster2_y = width // 4, height // 4 

# Main game loop
running = True
score = 0
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    keys = pygame.key.get_pressed()
    if keys[pygame.K_LEFT]:
        if not detect_wall_collision(player_x - player_speed, player_y, player_size):
            player_x -= player_speed
    if keys[pygame.K_RIGHT]:
        if not detect_wall_collision(player_x + player_speed, player_y, player_size):
            player_x += player_speed
    if keys[pygame.K_UP]:
        if not detect_wall_collision(player_x, player_y - player_speed, player_size):
            player_y -= player_speed
    if keys[pygame.K_DOWN]:
        if not detect_wall_collision(player_x, player_y + player_speed, player_size):
            player_y += player_speed

    player_rect = pygame.Rect(player_x, player_y, player_size, player_size)
    score += collect_dots(player_rect)

    # Move the monsters
    monster1_x, monster1_y = move_monster(monster1_x, monster1_y, player_x, player_y)
    monster2_x, monster2_y = move_monster(monster2_x, monster2_y, player_x, player_y)

    # Check if either monster collides with Pac-Man
    if player_rect.colliderect(pygame.Rect(monster1_x, monster1_y, monster_size, monster_size)) or \
       player_rect.colliderect(pygame.Rect(monster2_x, monster2_y, monster_size, monster_size)):
        print("Game Over!")
        running = False

    screen.fill(black)
    draw_maze()
    pygame.draw.rect(screen, yellow, player_rect)
    pygame.draw.rect(screen, red, (monster1_x, monster1_y, monster_size, monster_size))
    pygame.draw.rect(screen, red, (monster2_x, monster2_y, monster_size, monster_size))

    for dot in dots:
        pygame.draw.rect(screen, white, (dot[0], dot[1], dot_size, dot_size))

    # Display the score
    font = pygame.font.Font(None, 24)
    text = font.render(f"Score: {score}", True, white)
    screen.blit(text, (10, 10))

    pygame.display.flip()
    clock.tick(30)

pygame.quit()
