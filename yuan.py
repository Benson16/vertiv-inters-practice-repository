import pygame
import random

# Initialize Pygame
pygame.init()

# Screen dimensions
WIDTH, HEIGHT = 400, 600
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Flappy Bird")

# Colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)

# Load images
bird_img = pygame.image.load(r'C:\Users\CarlYuan.Verzola\Downloads\bird.png')  # Replace with your bird image path
bird_img = pygame.transform.scale(bird_img, (50, 35))  # Adjust size as needed

pipe_img = pygame.image.load(r'C:\Users\CarlYuan.Verzola\Downloads\pipe.png')  # Replace with your pipe image path
pipe_img = pygame.transform.scale(pipe_img, (60, 400))  # Adjust size as needed

# Bird variables
bird_x = 50
bird_y = HEIGHT // 2
bird_velocity = 0
gravity = 0.5
jump_strength = -10
max_tilt_up = 25  # Maximum tilt angle upwards
max_tilt_down = -45  # Maximum tilt angle downwards

# Pipe variables
pipe_width = 60
pipe_height = random.randint(150, 400)
pipe_x = WIDTH
pipe_velocity = 3
pipe_gap = 150

# Game variables
score = 0
font = pygame.font.SysFont(None, 36)
clock = pygame.time.Clock()
running = True
game_over = False
start_game = False

def draw_bird(bird_y, bird_velocity):
    # Calculate the tilt angle based on bird velocity
    if bird_velocity < 0:
        tilt_angle = max(min(max_tilt_up, -bird_velocity * 3), max_tilt_down)
    else:
        tilt_angle = min(max_tilt_down, bird_velocity * 2)

    # Tilt the bird within a limited angle range
    rotated_bird = pygame.transform.rotate(bird_img, tilt_angle)
    bird_rect = rotated_bird.get_rect(center=(bird_x + bird_img.get_width() // 2, bird_y + bird_img.get_height() // 2))
    screen.blit(rotated_bird, bird_rect.topleft)

def draw_pipe(pipe_x, pipe_height):
    # Top pipe (flipped)
    top_pipe = pygame.transform.flip(pipe_img, False, True)
    screen.blit(top_pipe, (pipe_x, pipe_height - top_pipe.get_height()))
    
    # Bottom pipe
    screen.blit(pipe_img, (pipe_x, pipe_height + pipe_gap))

def display_score(score):
    text = font.render(f"Score: {score}", True, BLACK)
    screen.blit(text, (10, 10))

def draw_start_screen():
    screen.fill(WHITE)
    title_text = font.render("Flappy Bird", True, BLACK)
    start_text = font.render("Press SPACE to Start", True, BLACK)
    screen.blit(title_text, (WIDTH // 4, HEIGHT // 3))
    screen.blit(start_text, (WIDTH // 6, HEIGHT // 2))

def draw_game_over_screen():
    screen.fill(WHITE)
    game_over_text = font.render("Game Over!", True, BLACK)
    restart_text = font.render("Press R to Restart", True, BLACK)
    screen.blit(game_over_text, (WIDTH // 4, HEIGHT // 3))
    screen.blit(restart_text, (WIDTH // 6, HEIGHT // 2))

# Main game loop
while running:
    screen.fill(WHITE)

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

        if event.type == pygame.KEYDOWN:
            if not start_game:
                if event.key == pygame.K_SPACE:
                    start_game = True
            if not game_over and start_game:
                if event.key == pygame.K_SPACE:
                    bird_velocity = jump_strength
            if game_over:
                if event.key == pygame.K_r:
                    # Reset the game
                    bird_y = HEIGHT // 2
                    bird_velocity = 0
                    pipe_x = WIDTH
                    score = 0
                    game_over = False
                    start_game = False  # Show start screen again

    if not start_game:
        draw_start_screen()

    elif not game_over:
        # Bird movement
        bird_velocity += gravity
        bird_y += bird_velocity

        # Pipe movement
        pipe_x -= pipe_velocity

        if pipe_x < -pipe_width:
            pipe_x = WIDTH
            pipe_height = random.randint(150, 400)
            score += 1

        # Collision detection
        if (bird_y < 0 or bird_y + bird_img.get_height() > HEIGHT or
                (pipe_x < bird_x + bird_img.get_width() and pipe_x + pipe_width > bird_x and
                 (bird_y < pipe_height or bird_y + bird_img.get_height() > pipe_height + pipe_gap))):
            game_over = True

        draw_bird(bird_y, bird_velocity)
        draw_pipe(pipe_x, pipe_height)
        display_score(score)

    else:
        draw_game_over_screen()

    pygame.display.update()
    clock.tick(60)

pygame.quit()
