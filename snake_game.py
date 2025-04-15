import pygame, random
pygame.init()

# Fonts
font = pygame.font.SysFont("Arial", 36)
score_font = pygame.font.SysFont("Arial", 24)

# Set screen dimensions
WIDTH, HEIGHT = 600, 400
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Snake Game")

# Load splash screen
splash = pygame.image.load("/home/okills/Documentos/Codedex/Python/Games/Snake/snake.png")
splash = pygame.transform.scale(splash, (WIDTH, HEIGHT))

# Game variables
BLOCK_SIZE = 20
snake_pos = [300, 200]
dx = 0
dy = 0
high_score = 0

direction = 'RIGHT'

# Colors
snake_color = (0, 255, 0)
food_color = (255, 0, 0)
clock = pygame.time.Clock()
FPS = 10

# Snake
snake_body = [snake_pos]
snake_length = 1

# Food
def get_random_food_position():
    x = random.randint(0, (WIDTH - BLOCK_SIZE) // BLOCK_SIZE) * BLOCK_SIZE
    y = random.randint(0, (HEIGHT - BLOCK_SIZE) // BLOCK_SIZE) * BLOCK_SIZE
    return [x, y]

food_pos = get_random_food_position()

# Game Over Screen
def show_game_over(score, high_score):
    screen.fill((0, 0, 0))
    game_over_text = font.render("Game Over!", True, (255, 0, 0))
    screen.blit(game_over_text, (WIDTH // 2 - game_over_text.get_width() // 2, HEIGHT // 2 - 90))
    
    score_text = font.render(f"Score: {score}", True, (255, 255, 0))
    screen.blit(score_text, (WIDTH // 2 - score_text.get_width() // 2, HEIGHT // 2 - 40))
    
    high_text = font.render(f"High Score: {high_score}", True, (0, 255, 255))
    screen.blit(high_text, (WIDTH // 2 - high_text.get_width() // 2, HEIGHT // 2))

    info_text = font.render("Press R to Restart or Q to Quit", True, (255, 255, 255))
    screen.blit(info_text, (WIDTH // 2 - info_text.get_width() // 2, HEIGHT // 2 + 50))
    pygame.display.update()

# Start Screen
def start_screen():
    waiting = True
    while waiting:
        screen.fill((0, 0, 0))
        title = font.render("Welcome to Snake Game!", True, (0, 255, 0))
        prompt = score_font.render("Press SPACE to Start", True, (255, 255, 255))

        screen.blit(title, (WIDTH // 2 - title.get_width() // 2, HEIGHT // 2 - 50))
        screen.blit(prompt, (WIDTH // 2 - prompt.get_width() // 2, HEIGHT // 2 + 10))

        pygame.display.update()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()
            if event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE:
                waiting = False

# Fade functions
def fade_in(surface, speed=5):
    fade = pygame.Surface((WIDTH, HEIGHT))
    fade.fill((0, 0, 0))
    for alpha in range(255, -1, -speed):
        fade.set_alpha(alpha)
        surface.fill((0, 0, 0))
        surface.blit(fade, (0, 0))
        pygame.display.update()
        pygame.time.delay(10)

def fade_out(surface, speed=5):
    fade = pygame.Surface((WIDTH, HEIGHT))
    fade.fill((0, 0, 0))
    for alpha in range(0, 256, speed):
        fade.set_alpha(alpha)
        surface.blit(fade, (0, 0))
        pygame.display.update()
        pygame.time.delay(10)
        
def fade_to_white(surface, speed=5):
    fade = pygame.Surface((WIDTH, HEIGHT))
    fade.fill((255, 255, 255))  # White
    for alpha in range(0, 256, speed):
        fade.set_alpha(alpha)
        surface.blit(fade, (0, 0))
        pygame.display.update()
        pygame.time.delay(10)

# Countdown function
def countdown():
    for i in range(3, 0, -1):
        screen.fill((0, 0, 0))
        count_text = font.render(str(i), True, (255, 255, 255))
        screen.blit(count_text, (WIDTH // 2 - count_text.get_width() // 2, HEIGHT // 2))
        pygame.display.update()
        pygame.time.delay(1000)

    screen.fill((0, 0, 0))
    go_text = font.render("GO!", True, (0, 255, 0))
    screen.blit(go_text, (WIDTH // 2 - go_text.get_width() // 2, HEIGHT // 2))
    pygame.display.update()
    pygame.time.delay(700)

    fade_to_white(screen)
    
def show_splash_screen():
    screen.blit(splash, (0, 0))
    pygame.display.update()
    pygame.time.delay(3000)  # Show for 3 seconds or until key press

# Load splash screen
show_splash_screen()

start_screen()
countdown()

# Initialize snake
dx = BLOCK_SIZE
dy = 0
direction = "RIGHT"

# Freeze zoom function
def follow_snake_zoom(surface,snake_body, zoom_steps=15, zoom_speed=50):
    for i in range(zoom_steps):
        zoom_factor = 1 + i * 0.1
        zoom_width = int(WIDTH * zoom_factor)
        zoom_height = int(HEIGHT * zoom_factor)
        
        # Calculate the center of the snake
        snake_center_x = sum(block[0] for block in snake_body) / len(snake_body)
        snake_center_y = sum(block[1] for block in snake_body) / len(snake_body)

        zoomed = pygame.transform.scale(surface, (zoom_width, zoom_height))

        # Center the zoom on the snake head (target_pos)
        offset_x = int(snake_center_x * zoom_factor - WIDTH // 2)
        offset_y = int(snake_center_y * zoom_factor - HEIGHT // 2)

        screen.blit(zoomed, (-offset_x, -offset_y))
        pygame.display.update()
        pygame.time.delay(zoom_speed)

# Main game loop
running = True
game_over = False
while running:
    # Game Over loop
    if game_over:
        show_game_over(snake_length - 1, high_score)
        if snake_length - 1 > high_score:
            high_score = snake_length - 1

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
                
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_q:
                    running = False
                if event.key == pygame.K_r:
                    # Reset everything to restart the game
                    fade_out(screen)
                    snake_pos = [300, 200]
                    dx = BLOCK_SIZE
                    dy = 0
                    direction = "RIGHT"
                    snake_body = [list(snake_pos)]
                    snake_length = 1
                    food_pos = get_random_food_position()
                    game_over = False
                    
        continue

    # Quit event handling
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
         
        # Key events
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_LEFT and direction != "RIGHT":
                dx = -BLOCK_SIZE
                dy = 0
                direction = "LEFT"
            elif event.key == pygame.K_RIGHT and direction != "LEFT":
                dx = BLOCK_SIZE
                dy = 0
                direction = "RIGHT"
            elif event.key == pygame.K_UP and direction != "DOWN":
                dy = -BLOCK_SIZE
                dx = 0
                direction = "UP"
            elif event.key == pygame.K_DOWN and direction != "UP":
                dy = BLOCK_SIZE
                dx = 0
                direction = "DOWN"

    # Snake movement
    snake_pos[0] += dx
    snake_pos[1] += dy
    new_head = list(snake_pos)
    snake_body.append(new_head)

    # Collision detection
    if (
    snake_pos[0] < 0 or snake_pos[0] >= WIDTH or
    snake_pos[1] < 0 or snake_pos[1] >= HEIGHT
    ):
        # Capture current screen before death
        death_frame = screen.copy()
        follow_snake_zoom(death_frame, snake_body)
        fade_to_white(screen)
        game_over = True

    # Snake body management
    if len(snake_body) > snake_length:
        del snake_body[0]

    # Drawing Background
    screen.fill((0, 0, 0))

    # Food drawing
    pygame.draw.rect(screen, food_color, [food_pos[0], food_pos[1], BLOCK_SIZE, BLOCK_SIZE])

    # Snake drawing
    for block in snake_body:
        pygame.draw.rect(screen, snake_color, [block[0], block[1], BLOCK_SIZE, BLOCK_SIZE])

    # Food logic
    if new_head == food_pos:
        snake_length += 1
        food_pos = get_random_food_position()

    # Collision with self
    for block in snake_body[:-1]:
        if new_head == block:
            # Capture current screen before death
            death_frame = screen.copy()
            follow_snake_zoom(death_frame, snake_body)
            fade_to_white(screen)
            game_over = True

    # Score display
    score_text = score_font.render(f"Score: {snake_length - 1}", True, (255, 255, 255))
    screen.blit(score_text, (10, 10))

    # Update display
    pygame.display.update()

    # Frame rate
    clock.tick(FPS)

pygame.quit()
