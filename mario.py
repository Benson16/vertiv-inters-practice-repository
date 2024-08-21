import pygame
import sys
import random

# Initialize pygame
pygame.init()

# Constants
WIDTH, HEIGHT = 500, 500
BACKGROUND_COLOR = (0, 0, 0)
PACMAN_COLOR = (255, 255, 0)
GHOST_COLOR = (255, 0, 0)
PELLET_COLOR = (0, 255, 0)
PACMAN_RADIUS = 20
GHOST_RADIUS = 15
PELLET_RADIUS = 5
PACMAN_SPEED = 5
GHOST_SPEED = 2
PELLET_COUNT = 10
FPS = 30

# Set up the display
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption('Pac-Man Game')

# Initialize game variables
pacman_x, pacman_y = WIDTH // 2, HEIGHT // 2
ghosts = [(random.randint(0, WIDTH), random.randint(0, HEIGHT)) for _ in range(3)]
pellets = [(random.randint(0, WIDTH), random.randint(0, HEIGHT)) for _ in range(PELLET_COUNT)]
score = 0

# Font for displaying score
font = pygame.font.SysFont(None, 36)

def draw_pacman(x, y):
    pygame.draw.circle(screen, PACMAN_COLOR, (x, y), PACMAN_RADIUS)

def draw_ghosts(ghost_positions):
    for gx, gy in ghost_positions:
        pygame.draw.circle(screen, GHOST_COLOR, (gx, gy), GHOST_RADIUS)

def draw_pellets(pellet_positions):
    for px, py in pellet_positions:
        pygame.draw.circle(screen, PELLET_COLOR, (px, py), PELLET_RADIUS)

def draw_score(score):
    score_surface = font.render(f'Score: {score}', True, (255, 255, 255))
    screen.blit(score_surface, (10, 10))

def move_ghosts(ghost_positions, pacman_x, pacman_y):
    new_ghost_positions = []
    for gx, gy in ghost_positions:
        if pacman_x > gx:
            gx += GHOST_SPEED
        elif pacman_x < gx:
            gx -= GHOST_SPEED
        if pacman_y > gy:
            gy += GHOST_SPEED
        elif pacman_y < gy:
            gy -= GHOST_SPEED
        new_ghost_positions.append((gx, gy))
    return new_ghost_positions

# Main game loop
clock = pygame.time.Clock()
running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()

    # Handle key presses
    keys = pygame.key.get_pressed()
    if keys[pygame.K_LEFT]:
        pacman_x -= PACMAN_SPEED
    if keys[pygame.K_RIGHT]:
        pacman_x += PACMAN_SPEED
    if keys[pygame.K_UP]:
        pacman_y -= PACMAN_SPEED
    if keys[pygame.K_DOWN]:
        pacman_y += PACMAN_SPEED

    # Boundary checks
    pacman_x = max(PACMAN_RADIUS, min(WIDTH - PACMAN_RADIUS, pacman_x))
    pacman_y = max(PACMAN_RADIUS, min(HEIGHT - PACMAN_RADIUS, pacman_y))

    # Move ghosts
    ghosts = move_ghosts(ghosts, pacman_x, pacman_y)

    # Check for collisions with pellets
    pellets = [p for p in pellets if not (pacman_x - PELLET_RADIUS < p[0] < pacman_x + PELLET_RADIUS and
                                          pacman_y - PELLET_RADIUS < p[1] < pacman_y + PELLET_RADIUS)]
    score += PELLET_COUNT - len(pellets)

    # Check for collisions with ghosts
    for gx, gy in ghosts:
        if pacman_x - GHOST_RADIUS < gx < pacman_x + GHOST_RADIUS and pacman_y - GHOST_RADIUS < gy < pacman_y + GHOST_RADIUS:
            print(f"Game Over! Your score was: {score}")
            pygame.quit()
            sys.exit()

    # Clear screen
    screen.fill(BACKGROUND_COLOR)

    # Draw game elements
    draw_pacman(pacman_x, pacman_y)
    draw_ghosts(ghosts)
    draw_pellets(pellets)
    draw_score(score)

    # Update display
    pygame.display.flip()
    
    # Cap the frame rate
    clock.tick(FPS)
