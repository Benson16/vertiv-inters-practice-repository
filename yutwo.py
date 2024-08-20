import pygame
import sys

# Initialize pygame
pygame.init()

# Define screen dimensions
screen_width = 800
screen_height = 1000
screen = pygame.display.set_mode((screen_width, screen_height))
pygame.display.set_caption("Simple Visual Novel with Choices")

# Define colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
GRAY = (200, 200, 200)

# Define fonts
font = pygame.font.Font(None, 36)

# Define a function to display text on the screen
def display_text(text, pos, color=BLACK):
    text_surface = font.render(text, True, color)
    screen.blit(text_surface, pos)

# Define a function to create buttons
def create_button(text, pos, width, height, color, hover_color, action=None):
    mouse = pygame.mouse.get_pos()
    click = pygame.mouse.get_pressed()
    
    if pos[0] < mouse[0] < pos[0] + width and pos[1] < mouse[1] < pos[1] + height:
        pygame.draw.rect(screen, hover_color, (pos[0], pos[1], width, height))
        if click[0] == 1 and action is not None:
            action()
    else:
        pygame.draw.rect(screen, color, (pos[0], pos[1], width, height))
    
    display_text(text, (pos[0] + 10, pos[1] + 10))

# Define the dialogue with choices
dialogue = [
    {"character": "Ryan", "text": "Hello! How are you today?", "choices": [
        {"text": "I'm doing well, thank you.", "next": 1},
        {"text": "Not so good.", "next": 2}
    ]},
    {"character": "AI", "text": "That's great to hear!", "choices": [
        {"text": "Thanks!", "next": 3},
        {"text": "How about you?", "next": 4}
    ]},
    {"character": "AI", "text": "I'm sorry to hear that. Anything I can help with?", "choices": [
        {"text": "Just a bit tired.", "next": 4},
        {"text": "Yeah, can you give me some advice?", "next": 5}
    ]},
    {"character": "AI", "text": "You're welcome! Have a great day!", "choices": []},
    {"character": "AI", "text": "I'm doing great, thanks for asking!", "choices": []},
    {"character": "AI", "text": "Of course! Always happy to help.", "choices": []}
]

# Define the function to handle dialogue
current_index = 0

def show_dialogue():
    global current_index
    
    screen.fill(WHITE)  # Fill the screen with white color
    
    if current_index < len(dialogue):
        character = dialogue[current_index]["character"]
        text = dialogue[current_index]["text"]
        choices = dialogue[current_index]["choices"]
        
        display_text(f"{character}:", (50, 450))
        display_text(text, (50, 500))
        
        # Display choices as buttons
        if choices:
            for i, choice in enumerate(choices):
                create_button(choice["text"], (50, 550 + i*50), 300, 40, GRAY, BLACK, lambda index=choice["next"]: select_choice(index))
        else:
            display_text("Press Enter to continue...", (50, 550))
    else:
        display_text("The End", (screen_width // 2 - 50, screen_height // 2))

# Function to handle choice selection
def select_choice(index):
    global current_index
    current_index = index

# Main loop
running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_RETURN and not dialogue[current_index]["choices"]:
                current_index += 1

    # Show the current dialogue
    show_dialogue()

    # Update the display
    pygame.display.flip()

# Quit pygame
pygame.quit()
sys.exit()


