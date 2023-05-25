import sys
import pygame
import random
from datetime import datetime
import json

# Initialize Pygame
pygame.init()

# Constants
WIDTH = 640
HEIGHT = 480
CELL_SIZE = 20
FPS = 10
SCOREBOARD_HEIGHT = 40
BORDER_WIDTH = 2

# Colors
BLACK = (0, 0, 0)
GREEN = (0, 255, 0)
RED = (255, 0, 0)
WHITE = (255, 255, 255)
TURQUOISE = (0, 199, 200)
LIGHT_RED = (255, 100, 100)
YELLOW = (255, 255, 0)

# Variables
snake = [(CELL_SIZE * 5, CELL_SIZE * 5), (CELL_SIZE * 4, CELL_SIZE * 5)]
snake_dir = (CELL_SIZE, 0)
next_snake_dir = snake_dir
food = None
score = 0
speed = FPS
game_over = False

# Initialize screen
screen = pygame.display.set_mode((WIDTH, HEIGHT + SCOREBOARD_HEIGHT))
pygame.display.set_caption("Snake Game")
clock = pygame.time.Clock()

def new_food():
    while True:
        x, y = random.randrange(0, WIDTH, CELL_SIZE), random.randrange(SCOREBOARD_HEIGHT, HEIGHT, CELL_SIZE)
        if (x, y) not in snake:
            return x, y

def move_snake():
    global snake, snake_dir, next_snake_dir, food, score, speed, game_over

    if game_over:
        return False

    snake_dir = next_snake_dir

    head_x, head_y = snake[0]
    new_head = (head_x + snake_dir[0], head_y + snake_dir[1])

    if new_head in snake or new_head[0] < 0 or new_head[0] >= WIDTH or new_head[1] < SCOREBOARD_HEIGHT or new_head[1] >= HEIGHT + SCOREBOARD_HEIGHT:
        game_over = True
        return False

    if new_head == food:
        food = new_food()
        score += 1
        speed = FPS + score // 10
    else:
        snake.pop()

    snake.insert(0, new_head)
    return True

def draw_objects():
    screen.fill(BLACK)

    for segment in snake:
        pygame.draw.rect(screen, GREEN, (segment[0], segment[1], CELL_SIZE, CELL_SIZE))

    if food:
        pygame.draw.rect(screen, RED, (food[0], food[1], CELL_SIZE, CELL_SIZE))

    # Draw scoreboard
    font = pygame.font.SysFont("trebuchetms", 36)
    score_text = font.render(f"Score: {score}", True, WHITE)
    speed_text = font.render(f"Speed: {speed - FPS + 1}", True, WHITE)
    screen.blit(score_text, (10, 5))
    screen.blit(speed_text, (WIDTH - 150, 5))

    # Draw game over text
    if game_over:
        game_over_text = font.render("Game Over! Enter: Restart / Esc: Quit", True, LIGHT_RED)
        screen.blit(game_over_text, (WIDTH // 2 - game_over_text.get_width() // 2, HEIGHT // 2))

    # Draw "Game by Batuhan" text
    game_by_text = font.render("Game by Batuhan", True, TURQUOISE)
    screen.blit(game_by_text, (WIDTH // 2 - game_by_text.get_width() // 2, HEIGHT - game_by_text.get_height()))

    # Draw border
   
    pygame.draw.rect(screen, YELLOW, (0, SCOREBOARD_HEIGHT, WIDTH, BORDER_WIDTH))  # top
    pygame.draw.rect(screen, YELLOW, (0, HEIGHT + SCOREBOARD_HEIGHT - BORDER_WIDTH, WIDTH, BORDER_WIDTH))  # bottom
    pygame.draw.rect(screen, YELLOW, (0, SCOREBOARD_HEIGHT, BORDER_WIDTH, HEIGHT))  # left
    pygame.draw.rect(screen, YELLOW, (WIDTH - BORDER_WIDTH, SCOREBOARD_HEIGHT, BORDER_WIDTH, HEIGHT))  # right

    pygame.display.flip()

def reset_game():
    global snake, snake_dir, next_snake_dir, food, score, speed, game_over

    snake = [(CELL_SIZE * 5, CELL_SIZE * 5), (CELL_SIZE * 4, CELL_SIZE * 5)]
    snake_dir = (CELL_SIZE, 0)
    next_snake_dir = snake_dir
    food = new_food()
    score = 0
    speed = FPS
    game_over = False

def handle_input():
    global next_snake_dir, game_over

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
        elif event.type == pygame.KEYDOWN and not game_over:
            if event.key in (pygame.K_UP, pygame.K_w) and snake_dir[1] == 0:
                next_snake_dir = (0, -CELL_SIZE)
            elif event.key in (pygame.K_DOWN, pygame.K_s) and snake_dir[1] == 0:
                next_snake_dir = (0, CELL_SIZE)
            elif event.key in (pygame.K_LEFT, pygame.K_a) and snake_dir[0] == 0:
                next_snake_dir = (-CELL_SIZE, 0)
            elif event.key in (pygame.K_RIGHT, pygame.K_d) and snake_dir[0] == 0:
                next_snake_dir = (CELL_SIZE, 0)
        elif event.type == pygame.KEYDOWN and game_over:
            if event.key == pygame.K_RETURN:
                reset_game()
            elif event.key == pygame.K_ESCAPE:
                pygame.quit()
                sys.exit()


paused = False
leaderboard_file = "leaderboard.json"

def save_score(score):
    date = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    new_score = {"date": date, "score": score}

    leaderboard = []

    try:
        with open(leaderboard_file, "r") as f:
            leaderboard = json.load(f)
    except FileNotFoundError:
        pass

    # Check if the score already exists
    score_exists = False
    for entry in leaderboard:
        if entry["score"] == score:
            score_exists = True
            break

    if not score_exists:
        leaderboard.append(new_score)

    leaderboard = sorted(leaderboard, key=lambda x: x["score"], reverse=True)[:10]

    with open(leaderboard_file, "w") as f:
        json.dump(leaderboard, f)


def draw_leaderboard():
    try:
        with open(leaderboard_file, "r") as f:
            leaderboard = json.load(f)
    except FileNotFoundError:
        return

    font = pygame.font.SysFont("trebuchetms", 24)
    title = font.render("Top Scores:", True, WHITE)
    screen.blit(title, (WIDTH // 2 - title.get_width() // 2, 50))

    for i, entry in enumerate(leaderboard):
        entry_text = font.render(f"{i + 1}. {entry['score']} - {entry['date']}", True, WHITE)
        screen.blit(entry_text, (WIDTH // 2 - entry_text.get_width() // 2, 100 + i * 30))

def handle_input():
    global next_snake_dir, game_over, paused

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_KP_PLUS:
                paused = not paused
                if paused:
                    draw_leaderboard()
                    pygame.display.flip()
                else:
                    draw_objects()
                    pygame.display.flip()
            elif not paused and not game_over:
                if event.key in (pygame.K_UP, pygame.K_w) and snake_dir[1] == 0:
                    next_snake_dir = (0, -CELL_SIZE)
                elif event.key in (pygame.K_DOWN, pygame.K_s) and snake_dir[1] == 0:
                    next_snake_dir = (0, CELL_SIZE)
                elif event.key in (pygame.K_LEFT, pygame.K_a) and snake_dir[0] == 0:
                    next_snake_dir = (-CELL_SIZE, 0)
                elif event.key in (pygame.K_RIGHT, pygame.K_d) and snake_dir[0] == 0:
                    next_snake_dir = (CELL_SIZE, 0)
            elif event.type == pygame.KEYDOWN and game_over:
                if event.key == pygame.K_RETURN:
                    reset_game()
                elif event.key == pygame.K_ESCAPE:
                    pygame.quit()
                    sys.exit()

def main():
    global paused
    while True:
        handle_input()
        if not paused:
            draw_objects()
            if not move_snake():
                save_score(score)
                continue
            clock.tick(speed)

reset_game()
main()