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
GRAY = (120, 120, 120)
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
    global char_x, char_y, char_width, char_height
    char_x, char_y = screen_width // 2, screen_height - 120
    # Reset character size to default values
    char_width, char_height = 50, 50
    blocks = create_falling_blocks()  # Ensure blocks are created anew
    return blocks

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
        screen.blit(title_text, (screen_width // 2 - title_text.get_width() // 2, 10))

        # Draw instructions
        instructions_text = font.render("Press Enter to Start", True, BLACK)
        screen.blit(instructions_text, (screen_width // 2 - instructions_text.get_width() // 2, 150))

        # Draw speed option
        speed_text = font.render(f"Press S to change Speed: {falling_speed}", True, BLACK)
        screen.blit(speed_text, (screen_width // 2 - speed_text.get_width() // 2, 200))

        # Character Customization
        customization_text = font.render("Press C to Customize Character", True, BLACK)
        screen.blit(customization_text, (screen_width // 2 - customization_text.get_width() // 2, 250))

        instructions_text = font.render("Hold SPACE to Accelerate", True, BLACK)
        screen.blit(instructions_text, (screen_width // 2 - instructions_text.get_width() // 2, 100))

        # If prompt is active, display input box
        if prompt_active:
            input_prompt_text = font.render("Enter Speed (1-10):", True, BLACK)
            screen.blit(input_prompt_text, (screen_width // 2 - input_prompt_text.get_width() // 2, 300))

            input_box = pygame.Rect(screen_width // 2 - 50, 350, 100, 40)
            pygame.draw.rect(screen, BLACK, input_box, 2)
            input_display_text = font.render(input_text, True, BLACK)
            screen.blit(input_display_text, (input_box.x + 5, input_box.y + 5))

        # Display the RGB value of the current character color
        color_text = f"RGB: {CHARACTER_COLOR}"
        color_text_surface = font.render(color_text, True, BLACK)
        screen.blit(color_text_surface, (screen_width // 2 - color_text_surface.get_width() // 2, screen_height - 100))

        char_x = screen_width // 2 - char_width // 2  # Center horizontally
        char_y = screen_height // 2 - char_height + 180  # Center vertically
        pygame.draw.rect(screen, CHARACTER_COLOR, (char_x, char_y, char_width, char_height))


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
                elif event.key == pygame.K_BACKSPACE:
                    input_text = input_text[:-1]  # Remove last character
                else:
                    # Only allow numbers and limited characters for input
                    if event.unicode.isdigit():
                        input_text += event.unicode

        pygame.display.flip()

# Main game loop with invincibility period
def game_loop():
    global char_x, char_y, char_width, char_height, CHARACTER_COLOR, falling_speed

    blocks = create_falling_blocks()
    clock = pygame.time.Clock()
    running = True

    # Start invincibility period (e.g., 3 seconds)
    invincibility_time = 3000  # Invincibility lasts for 3000 ms (3 seconds)
    invincibility_start_time = pygame.time.get_ticks()  # Get the current time in milliseconds

    # Initialize the score
    score = 0

    normal_speed = 5  # Default speed for the character
    accelerated_speed = 12  # Speed when accelerate button is pressed
    char_speed = normal_speed  # Start with normal speed

    # Set font for text on blocks
    block_font = pygame.font.SysFont("Arial", 20)

    while running:
        screen.fill(WHITE)  # Fill the screen with white

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
        if keys[pygame.K_LEFT] and char_x > 0:
            char_x -= char_speed
        if keys[pygame.K_RIGHT] and char_x < screen_width - char_width:
            char_x += char_speed

        if keys[pygame.K_SPACE]:
            char_speed = accelerated_speed  # Increase character speed  
        else:
            char_speed = normal_speed  # Revert to normal speed

        # Update falling blocks (move them down)
        new_blocks = []
        for block in blocks:
            block[1] += falling_speed  # Move each block down
            if block[1] > screen_height:  # Reset the block if it goes off screen
                block[1] = -block_height
                block[0] = random.choice(range(columns)) * block_width

                # Increase the score when the block hits the ground
                score += 1

            new_blocks.append(block)

        blocks = new_blocks

        # Check if invincibility period is over
        current_time = pygame.time.get_ticks()
        invincible = current_time - invincibility_start_time < invincibility_time

        # If not invincible, check for collisions
        if not invincible:
            for block in blocks:
                block_rect = pygame.Rect(block)
                char_rect = pygame.Rect(char_x, char_y, char_width, char_height)
                if char_rect.colliderect(block_rect):
                    # If collision occurs, restart the game
                    return 'restart'

        # Draw the falling blocks with text
        for block in blocks:
            pygame.draw.rect(screen, BLACK, block)  # Draw the block (rectangle)

            # Add text inside the block
            block_rect = pygame.Rect(block)
            text = block_font.render("♪", True, WHITE)  # Text to display in the block
            block_font = pygame.font.SysFont("Arial", 40)
            text_rect = text.get_rect(center=block_rect.center)  # Center the text inside the block
            screen.blit(text, text_rect)  # Draw the text

        # Draw the character
        pygame.draw.rect(screen, CHARACTER_COLOR, (char_x, char_y, char_width, char_height))

        # Display message
        game_over_text = font.render("Avoid the blocks!", True, GRAY)
        screen.blit(game_over_text, (10, 10))

        # Display invincibility warning if active
        if invincible:
            invincibility_text = font.render("Invincible!", True, RED)
            screen.blit(invincibility_text, (screen_width // 2 - invincibility_text.get_width() // 2, screen_height // 2 - 50))
            score = 0

        # Display the current score
        score_text = font.render(f"Score: {score}", True, BLACK)
        screen.blit(score_text, (10, screen_height - 40))  # Place score at bottom left

        pygame.display.flip()

        clock.tick(60)



# Main Program Loop
while True:
    result = home_screen()
    if result == 'start':
        game_result = game_loop()
        if game_result == 'restart':
            continue
