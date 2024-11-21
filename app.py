import pygame
import random
import sys

# Initialize Pygame
pygame.init()

# Set up the window
screen_width, screen_height = 800, 600
screen = pygame.display.set_mode((screen_width, screen_height))
pygame.display.set_caption("Falling Blocks Game")

# Define the colors
BLUE = (0, 0, 255)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
WHITE = (255, 255, 255)
YELLOW = (255, 255, 0)
BLACK = (0, 0, 0)
CHARACTER_COLOR = BLACK

# Define the grid dimensions
block_width = 100
block_height = 100
columns = 8  # Adjusted number of columns to fit the screen width
rows = 6     # Adjusted number of rows to fit the screen height

# Set the font for text
font = pygame.font.SysFont("Arial", 30)

# Set the character's initial position and speed
char_x, char_y = screen_width // 2, screen_height - 50
char_width, char_height = 50, 50
char_speed = 5

# Global variable for falling block speed
falling_speed = 5

# Function to create falling blocks with empty lines
def create_falling_blocks():
    blocks = []
    for row in range(rows):
        # Random number of blocks in each row (2 to 6) and skipping rows to leave empty space
        if row % 2 == 0:  # Leave an empty line in between
            continue
        num_blocks = random.randint(2, 6)  # Random number of blocks per row (2 to 6)
        row_blocks = random.sample(range(columns), num_blocks)  # Random positions for blocks in this row
        for col in row_blocks:
            blocks.append([col * block_width, row * block_height, block_width, block_height])
    return blocks

# Function to restart the game
def restart_game():
    global char_x, char_y
    char_x, char_y = screen_width // 2, screen_height - 120
    return create_falling_blocks()

# Home screen loop
def home_screen():
    global falling_speed, CHARACTER_COLOR, char_width, char_height

    running = True
    input_text = ''  # To hold the user input for speed
    prompt_active = False  # Flag to check if the speed prompt is active

    while running:
        screen.fill(WHITE)
        # Draw title
        title_text = font.render("Falling Blocks Game", True, BLACK)
        screen.blit(title_text, (screen_width // 2 - title_text.get_width() // 2, 50))

        # Draw instructions
        instructions_text = font.render("Press Enter to Start", True, BLACK)
        screen.blit(instructions_text, (screen_width // 2 - instructions_text.get_width() // 2, 150))

        # Draw speed option
        speed_text = font.render(f"Speed: {falling_speed}", True, BLACK)
        screen.blit(speed_text, (screen_width // 2 - speed_text.get_width() // 2, 200))

        # Character Customization
        customization_text = font.render("Press C to Customize Character", True, BLACK)
        screen.blit(customization_text, (screen_width // 2 - customization_text.get_width() // 2, 250))

        # If prompt is active, display input box
        if prompt_active:
            input_prompt_text = font.render("Enter Speed (1-10):", True, BLACK)
            screen.blit(input_prompt_text, (screen_width // 2 - input_prompt_text.get_width() // 2, 300))

            input_box = pygame.Rect(screen_width // 2 - 50, 350, 100, 40)
            pygame.draw.rect(screen, BLACK, input_box, 2)
            input_display_text = font.render(input_text, True, BLACK)
            screen.blit(input_display_text, (input_box.x + 5, input_box.y + 5))

        # Listen for events
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_RETURN:
                    # If Enter is pressed and prompt is not active, start the game
                    if not prompt_active:
                        return 'start'
                    else:
                        # If prompt is active, confirm speed change
                        try:
                            speed = int(input_text)
                            if 1 <= speed <= 10:
                                falling_speed = speed
                                prompt_active = False  # Close the input prompt
                                input_text = ''
                            else:
                                input_text = ''  # Reset the input if invalid
                        except ValueError:
                            input_text = ''  # Reset the input if not a number
                elif event.key == pygame.K_s:
                    # Activate the prompt to input speed
                    prompt_active = True
                    input_text = ''
                elif event.key == pygame.K_c:  # Customize character
                    CHARACTER_COLOR = (random.randint(0, 255), random.randint(0, 255), random.randint(0, 255))
                    char_width = random.randint(40, 100)
                    char_height = random.randint(40, 100)
                elif event.key == pygame.K_BACKSPACE:
                    input_text = input_text[:-1]  # Remove last character
                else:
                    # Only allow numbers and limited characters for input
                    if event.unicode.isdigit():
                        input_text += event.unicode
# Display the RGB value of the current character color
        color_text = f"RGB: {CHARACTER_COLOR}"
        color_text_surface = font.render(color_text, True, BLACK)
        screen.blit(color_text_surface, (WIDTH // 2 - color_text_surface.get_width() // 2, HEIGHT // 2 + char_height // 2 + 20))

    # If the prompt is active, display the input box
    if prompt_active:
        input_surface = font.render(input_text, True, BLACK)
        screen.blit(input_surface, (WIDTH // 2 - input_surface.get_width() // 2, HEIGHT // 2 - 100))

        pygame.display.flip()
        pygame.time.Clock().tick(60)

# Main game loop
def game_loop():
    global char_x, char_y, char_width, char_height, CHARACTER_COLOR, falling_speed

    blocks = create_falling_blocks()
    clock = pygame.time.Clock()
    running = True

    while running:
        screen.fill(BLUE)  # Fill the screen with blue

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

        # Get the keys pressed
        keys = pygame.key.get_pressed()

        # Move the character with WASD
        if keys[pygame.K_a] and char_x > 0:
            char_x -= char_speed
        if keys[pygame.K_d] and char_x < screen_width - char_width:
            char_x += char_speed

        # Update falling blocks (move them down)
        new_blocks = []
        for block in blocks:
            block[1] += falling_speed  # Move each block down
            if block[1] > screen_height:  # Reset the block if it goes off screen
                block[1] = -block_height
                block[0] = random.choice(range(columns)) * block_width
            new_blocks.append(block)

        blocks = new_blocks

        # Check for collisions (if character touches a block)
        for block in blocks:
            block_rect = pygame.Rect(block)
            char_rect = pygame.Rect(char_x, char_y, char_width, char_height)
            if char_rect.colliderect(block_rect):
                # If collision occurs, restart the game
                return 'restart'

        # Draw the falling blocks
        for block in blocks:
            pygame.draw.rect(screen, RED, block)

        # Draw the character
        pygame.draw.rect(screen, CHARACTER_COLOR, (char_x, char_y, char_width, char_height))

        # Display message
        game_over_text = font.render("Avoid the blocks!", True, WHITE)
        screen.blit(game_over_text, (10, 10))

        pygame.display.flip()

        clock.tick(60)

# Main Program Loop
while True:
    result = home_screen()
    if result == 'start':
        game_result = game_loop()
        if game_result == 'restart':
            continue
