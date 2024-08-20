import pygame
import random

# Initialize Pygame
pygame.init()

# Constants
SCREEN_WIDTH = 600
SCREEN_HEIGHT = 400
PLAYER_SIZE = 40
PLAYER_SPEED = 2  # Slow down player movement
BG_COLOR = (50, 150, 200)
TEXT_COLOR = (255, 255, 255)
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
RED = (255, 0, 0)

# Screen setup
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Pokemon Game")

# Load sprites
player_sprite = pygame.image.load(r'C:\Users\CarlYuan.Verzola\Downloads\player.png')  # Replace with actual image paths
npc_sprite = pygame.image.load(r'C:\Users\CarlYuan.Verzola\Downloads\npc.png')

# Resize sprites
player_sprite = pygame.transform.scale(player_sprite, (100, 100))
npc_sprite = pygame.transform.scale(npc_sprite, (100, 100))

# Player and NPC positions
player_pos = [50, SCREEN_HEIGHT - 150]
npc_pos = [SCREEN_WIDTH - 150, 50]

# Font setup
font = pygame.font.SysFont("comicsansms", 30)

# Function to display text on the screen
def display_text(text, x, y, size=30, color=TEXT_COLOR):
    font = pygame.font.SysFont("comicsansms", size)
    label = font.render(text, True, color)
    screen.blit(label, (x, y))

# Function to animate health bar
def animate_health_bar(current_hp, target_hp, x, y, max_hp, is_player=True):
    bar_width = 200
    bar_height = 20
    ratio = current_hp / max_hp
    pygame.draw.rect(screen, WHITE, (x, y, bar_width, bar_height))
    pygame.draw.rect(screen, (255, 0, 0), (x, y, bar_width * ratio, bar_height))
    
    if current_hp > target_hp:
        current_hp -= 1
        pygame.time.delay(5)
    
    return current_hp

# Function to animate attack
def animate_attack(attacker_pos, target_pos, attack_direction):
    original_pos = attacker_pos.copy()
    for _ in range(10):
        if attack_direction == 'right':
            attacker_pos[0] += 5 if attacker_pos[0] < target_pos[0] else -5
        elif attack_direction == 'left':
            attacker_pos[0] -= 5 if attacker_pos[0] > target_pos[0] else 5
        elif attack_direction == 'down':
            attacker_pos[1] += 5 if attacker_pos[1] < target_pos[1] else -5
        elif attack_direction == 'up':
            attacker_pos[1] -= 5 if attacker_pos[1] > target_pos[1] else 5
        
        screen.fill(BLACK)
        screen.blit(player_sprite, player_pos)
        screen.blit(npc_sprite, npc_pos)
        pygame.display.flip()
        pygame.time.delay(30)
    
    attacker_pos = original_pos.copy()

# Function to fade to black
def fade_to_black():
    fade_surface = pygame.Surface((SCREEN_WIDTH, SCREEN_HEIGHT))
    fade_surface.fill(BLACK)
    for alpha in range(0, 256, 5):
        fade_surface.set_alpha(alpha)
        screen.blit(fade_surface, (0, 0))
        pygame.display.flip()
        pygame.time.delay(30)

# Define Pokémon stats
player_pokemon = {
    "name": "Pikachu",
    "hp": 100,
    "max_hp": 100,
    "moves": ["Tackle", "Thunderbolt", "Quick Attack", "Iron Tail"]
}

npc_pokemon = {
    "name": "Charmander",
    "hp": 100,
    "max_hp": 100,
    "moves": ["Scratch", "Ember", "Flamethrower", "Growl"]
}

# Turn tracking
player_turn = True

# Function for battle system in GUI
def battle(player, npc):
    global player_turn  # Track the turn
    running = True
    player_hp = player["hp"]
    npc_hp = npc["hp"]
    
    while running:
        screen.fill(BLACK)
        screen.blit(player_sprite, (50, 200))
        screen.blit(npc_sprite, (400, 50))
        
        player_hp = animate_health_bar(player_hp, player["hp"], 50, 50, player["max_hp"])
        npc_hp = animate_health_bar(npc_hp, npc["hp"], 350, 50, npc["max_hp"])
        
        if player['hp'] > 0 and npc['hp'] > 0:
            if player_turn:
                # Player's turn: Show move buttons
                if create_button(player['moves'][0], 50, 300, 100, 40, WHITE, lambda: player_move(player, npc, 0)):
                    pass
                if create_button(player['moves'][1], 200, 300, 100, 40, WHITE, lambda: player_move(player, npc, 1)):
                    pass
                if create_button(player['moves'][2], 350, 300, 100, 40, WHITE, lambda: player_move(player, npc, 2)):
                    pass
                if create_button(player['moves'][3], 500, 300, 100, 40, WHITE, lambda: player_move(player, npc, 3)):
                    pass
            else:
                # NPC's turn: NPC automatically attacks once
                pygame.time.delay(1000)  # Small delay for NPC's turn
                npc_move(npc, player)
                player_turn = True  # Switch back to player's turn after NPC attacks

        # Check for game over
        if player["hp"] <= 0:
            display_text(f"{player['name']} fainted! You lose!", 150, 200)
            pygame.display.flip()
            pygame.time.delay(2000)
            running = False
        elif npc["hp"] <= 0:
            display_text(f"{npc['name']} fainted! You win!", 150, 200)
            pygame.display.flip()
            pygame.time.delay(2000)
            running = False

        pygame.display.flip()
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

def player_move(player, npc, move_index):
    global player_turn  # Switch turns after player's move
    damage = random.randint(10, 30)
    npc["hp"] -= damage
    npc["hp"] = max(npc["hp"], 0)  # Ensure HP doesn't go below 0
    print(f"{player['name']} used {player['moves'][move_index]}! It dealt {damage} damage.")
    animate_attack(player_pos, npc_pos, 'right')  # Simulate attack animation
    player_turn = False  # Switch to NPC's turn after player's move

def npc_move(npc, player):
    global player_turn  # Switch turns after NPC's move
    npc_move = random.choice(npc["moves"])
    damage = random.randint(10, 30)
    player["hp"] -= damage
    player["hp"] = max(player["hp"], 0)  # Ensure HP doesn't go below 0
    print(f"{npc['name']} used {npc_move}! It dealt {damage} damage.")
    animate_attack(npc_pos, player_pos, 'left')  # Simulate attack animation
    player_turn = True  # Switch back to player's turn after NPC's move

# Function to create buttons
def create_button(text, x, y, w, h, color, action=None):
    pygame.draw.rect(screen, color, (x, y, w, h))
    display_text(text, x + 10, y + 10, 20, BLACK)
    mouse = pygame.mouse.get_pos()
    click = pygame.mouse.get_pressed()

    if x + w > mouse[0] > x and y + h > mouse[1] > y:
        if click[0] == 1 and action is not None:
            return action()

# Main game loop
running = True
battle_initiated = False
while running:
    screen.fill(BG_COLOR)
    screen.blit(player_sprite, player_pos)
    screen.blit(npc_sprite, npc_pos)

    # Player movement
    keys = pygame.key.get_pressed()
    if keys[pygame.K_LEFT]:
        player_pos[0] -= PLAYER_SPEED
    if keys[pygame.K_RIGHT]:
        player_pos[0] += PLAYER_SPEED
    if keys[pygame.K_UP]:
        player_pos[1] -= PLAYER_SPEED
    if keys[pygame.K_DOWN]:
        player_pos[1] += PLAYER_SPEED

    # Check for interaction with NPC
    if abs(player_pos[0] - npc_pos[0]) < 50 and abs(player_pos[1] - npc_pos[1]) < 50 and not battle_initiated:
        display_text("Press 'Enter' to battle", 200, 200)
        if keys[pygame.K_RETURN]:
            display_text("Let's Fight!", SCREEN_WIDTH // 2 - 50, SCREEN_HEIGHT // 2)
            pygame.display.flip()
            pygame.time.delay(1000)
            battle(player_pokemon, npc_pokemon)
            battle_initiated = True

    pygame.display.flip()
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

pygame.quit()
