import pygame
import random

# Initialize pygame
pygame.init()

# Screen dimensions
screen_width = 800
screen_height = 600
screen = pygame.display.set_mode((screen_width, screen_height))
pygame.display.set_caption("Simple Ball Game")

# Colors
white = (255, 255, 255)
black = (0, 0, 0)
red = (255, 0, 0)

# Paddle
paddle_width = 100
paddle_height = 10
paddle_x = (screen_width - paddle_width) / 2
paddle_y = screen_height - paddle_height - 10
paddle_speed = 10

# Ball
ball_size = 10
ball_x = random.randint(ball_size, screen_width - ball_size)
ball_y = screen_height // 2
ball_speed_x = random.choice([-5, 5])
ball_speed_y = -5

# Score
score = 0
font = pygame.font.Font(None, 36)

# Function to draw gradient background
def draw_gradient_background():
    for i in range(screen_height):
        # Gradually change from blue to purple
        r = 0 + (i * 255) // screen_height
        g = 0
        b = 255 - (i * 255) // screen_height
        pygame.draw.line(screen, (r, g, b), (0, i), (screen_width, i))

# Game loop
running = True
clock = pygame.time.Clock()

while running:
    # Event handling
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    # Paddle movement
    keys = pygame.key.get_pressed()
    if keys[pygame.K_LEFT] and paddle_x > 0:
        paddle_x -= paddle_speed
    if keys[pygame.K_RIGHT] and paddle_x < screen_width - paddle_width:
        paddle_x += paddle_speed

    # Ball movement
    ball_x += ball_speed_x
    ball_y += ball_speed_y

    # Ball collision with walls
    if ball_x <= 0 or ball_x >= screen_width - ball_size:
        ball_speed_x = -ball_speed_x
    if ball_y <= 0:
        ball_speed_y = -ball_speed_y

    # Ball collision with paddle
    if paddle_y < ball_y + ball_size < paddle_y + paddle_height and paddle_x < ball_x < paddle_x + paddle_width:
        ball_speed_y = -ball_speed_y
        score += 1  # Increase score when the ball hits the paddle

    # Ball out of bounds
    if ball_y >= screen_height:
        print("Game Over!")
        running = False

    # Drawing everything
    draw_gradient_background()  # Draw the gradient background
    pygame.draw.rect(screen, white, (paddle_x, paddle_y, paddle_width, paddle_height))
    pygame.draw.circle(screen, black, (ball_x, ball_y), ball_size)  # Ball is now black

    # Display the score
    score_text = font.render(f"Score: {score}", True, white)
    screen.blit(score_text, (10, 10))

    pygame.display.flip()

    # Frame rate
    clock.tick(60)

pygame.quit()
