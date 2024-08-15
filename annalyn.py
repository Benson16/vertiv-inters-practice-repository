import pygame
import time
import random

# Initialize Pygame
pygame.init()

# Define colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (213, 50, 80)
GREEN = (0, 255, 0)
BLUE = (50, 153, 213)
BACKGROUND_COLORS = [BLUE, BLACK, GREEN, WHITE, (200, 200, 200)]
SNAKE_COLORS = [BLACK, GREEN, WHITE, BLUE]

# Set display dimensions
DIS_WIDTH = 600
DIS_HEIGHT = 400

# Set up the display
DIS = pygame.display.set_mode((DIS_WIDTH, DIS_HEIGHT))
pygame.display.set_caption('Snake Game')

# Set the clock
CLOCK = pygame.time.Clock()

# Define the snake block size and speed
SNAKE_BLOCK = 10
SNAKE_SPEED = 15

# Define font style
FONT_STYLE = pygame.font.SysFont(None, 50)
SMALL_FONT = pygame.font.SysFont(None, 35)

def message(msg, color, size=25):
    font = FONT_STYLE if size == 25 else SMALL_FONT
    mesg = font.render(msg, True, color)
    return mesg

def draw_snake(snake_block, snake_list, color):
    for x in snake_list:
        pygame.draw.rect(DIS, color, [x[0], x[1], snake_block, snake_block])

def gameLoop(background_color, snake_color):
    game_over = False
    game_close = False
    score = 0

    # Initial position of the snake
    x1 = DIS_WIDTH / 2
    y1 = DIS_HEIGHT / 2

    # Initial changes in position
    x1_change = 0
    y1_change = 0

    # Define the snake
    snake_List = []
    Length_of_snake = 1

    # Define food position
    foodx = round(random.randrange(0, DIS_WIDTH - SNAKE_BLOCK) / 10.0) * 10.0
    foody = round(random.randrange(0, DIS_HEIGHT - SNAKE_BLOCK) / 10.0) * 10.0

    while not game_over:

        while game_close == True:
            DIS.fill(background_color)
            msg = message(f"Score: {score}", RED, size=35)
            DIS.blit(msg, [DIS_WIDTH / 2 - msg.get_width() / 2, DIS_HEIGHT / 2 - msg.get_height() / 2 - 50])
            msg = message("You Lost! Press Q-Quit or C-Play Again", BLACK, size=14)
            DIS.blit(msg, [DIS_WIDTH / 2 - msg.get_width() / 2, DIS_HEIGHT / 2 - msg.get_height() / 2 + 50])
            pygame.display.update()

            for event in pygame.event.get():
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_q:
                        game_over = True
                        game_close = False
                    if event.key == pygame.K_c:
                        gameLoop(background_color, snake_color)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                game_over = True
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_LEFT:
                    x1_change = -SNAKE_BLOCK
                    y1_change = 0
                elif event.key == pygame.K_RIGHT:
                    x1_change = SNAKE_BLOCK
                    y1_change = 0
                elif event.key == pygame.K_UP:
                    y1_change = -SNAKE_BLOCK
                    x1_change = 0
                elif event.key == pygame.K_DOWN:
                    y1_change = SNAKE_BLOCK
                    x1_change = 0

        if x1 >= DIS_WIDTH or x1 < 0 or y1 >= DIS_HEIGHT or y1 < 0:
            game_close = True
        x1 += x1_change
        y1 += y1_change
        DIS.fill(background_color)
        pygame.draw.rect(DIS, GREEN, [foodx, foody, SNAKE_BLOCK, SNAKE_BLOCK])
        snake_Head = []
        snake_Head.append(x1)
        snake_Head.append(y1)
        snake_List.append(snake_Head)
        if len(snake_List) > Length_of_snake:
            del snake_List[0]

        for x in snake_List[:-1]:
            if x == snake_Head:
                game_close = True

        draw_snake(SNAKE_BLOCK, snake_List, snake_color)

        pygame.display.update()

        if x1 == foodx and y1 == foody:
            foodx = round(random.randrange(0, DIS_WIDTH - SNAKE_BLOCK) / 10.0) * 10.0
            foody = round(random.randrange(0, DIS_HEIGHT - SNAKE_BLOCK) / 10.0) * 10.0
            Length_of_snake += 1
            score += 10

        CLOCK.tick(SNAKE_SPEED)

    pygame.quit()
    quit()

def settings_menu():
    global BACKGROUND_COLORS, SNAKE_COLORS
    selected_background = 0
    selected_snake_color = 0
    settings_running = True

    while settings_running:
        DIS.fill(WHITE)
        
        # Draw color selection rectangles
        pygame.draw.rect(DIS, BACKGROUND_COLORS[selected_background], [50, 100, 200, 50])
        pygame.draw.rect(DIS, SNAKE_COLORS[selected_snake_color], [50, 200, 200, 50])
        
        # Draw option labels
        msg = message("Background Color", BLACK, size=15)
        DIS.blit(msg, [50 + 200 / 2 - msg.get_width() / 2, 100 + 50 / 2 - msg.get_height() / 2])
        
        msg = message("Snake Color", BLACK, size=15)
        DIS.blit(msg, [50 + 200 / 2 - msg.get_width() / 2, 200 + 50 / 2 - msg.get_height() / 2])
        
        # Draw instruction text
        msg = message("Use Arrow Keys to Select, ENTER to Start", BLACK, size=20)
        DIS.blit(msg, [DIS_WIDTH / 2 - msg.get_width() / 2, DIS_HEIGHT - 50])
        
        # Draw selectors
        pygame.draw.rect(DIS, BLACK, [40, 100 + selected_background * 100 + 20, 10, 10])
        pygame.draw.rect(DIS, BLACK, [40, 200 + (selected_snake_color - 1) * 100 + 20, 10, 10])
        
        pygame.display.update()

        for event in pygame.event.get():
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_DOWN:
                    selected_snake_color = (selected_snake_color + 1) % len(SNAKE_COLORS)
                elif event.key == pygame.K_UP:
                    selected_snake_color = (selected_snake_color - 1) % len(SNAKE_COLORS)
                elif event.key == pygame.K_RIGHT:
                    selected_background = (selected_background + 1) % len(BACKGROUND_COLORS)
                elif event.key == pygame.K_LEFT:
                    selected_background = (selected_background - 1) % len(BACKGROUND_COLORS)
                elif event.key == pygame.K_RETURN:
                    settings_running = False
                    gameLoop(BACKGROUND_COLORS[selected_background], SNAKE_COLORS[selected_snake_color])

def main_menu():
    menu_running = True

    while menu_running:
        DIS.fill(WHITE)
        pygame.draw.rect(DIS, GREEN, [DIS_WIDTH / 2 - 100, DIS_HEIGHT / 2 - 80, 200, 50])
        pygame.draw.rect(DIS, RED, [DIS_WIDTH / 2 - 100, DIS_HEIGHT / 2 + 20, 200, 50])
        msg = message("Play", BLACK, size=35)
        DIS.blit(msg, [DIS_WIDTH / 2 - msg.get_width() / 2, DIS_HEIGHT / 2 - 80 + 50 / 2 - msg.get_height() / 2])
        msg = message("Settings", BLACK, size=35)
        DIS.blit(msg, [DIS_WIDTH / 2 - msg.get_width() / 2, DIS_HEIGHT / 2 + 20 + 50 / 2 - msg.get_height() / 2])
        pygame.display.update()

        for event in pygame.event.get():
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_p:
                    menu_running = False
                    gameLoop(BLUE, BLACK)  # Default colors
                elif event.key == pygame.K_s:
                    menu_running = False
                    settings_menu()

if __name__ == "__main__":
    main_menu()
