import pygame
import random
import sys

# Initialize Pygame
pygame.init()

# Constants
WIDTH, HEIGHT = 600, 600
GRID_SIZE = 20
GRID_WIDTH = WIDTH // GRID_SIZE
GRID_HEIGHT = HEIGHT // GRID_SIZE
FPS = 10

# Colors
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
RED = (255, 0, 0)
GRAY = (100, 100, 100)

# Initialize screen
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Snake Game")
clock = pygame.time.Clock()
font_large = pygame.font.Font(None, 72)
font_medium = pygame.font.Font(None, 48)
font_small = pygame.font.Font(None, 36)

# Game states
START = 0
PLAYING = 1
GAME_OVER = 2

class Snake:
    def __init__(self):
        self.positions = [(GRID_WIDTH // 2, GRID_HEIGHT // 2)]
        self.direction = (1, 0)
        self.grow = False
    
    def move(self):
        head_x, head_y = self.positions[0]
        dir_x, dir_y = self.direction
        new_head = ((head_x + dir_x) % GRID_WIDTH, (head_y + dir_y) % GRID_HEIGHT)
        
        if new_head in self.positions[1:]:
            return False  # Game over - snake hit itself
        
        self.positions.insert(0, new_head)
        if not self.grow:
            self.positions.pop()
        else:
            self.grow = False
        
        return True
    
    def change_direction(self, direction):
        # Prevent moving in opposite direction
        if (direction[0] * -1, direction[1] * -1) != self.direction:
            self.direction = direction
    
    def draw(self, surface):
        for i, pos in enumerate(self.positions):
            x, y = pos
            rect = pygame.Rect(x * GRID_SIZE, y * GRID_SIZE, GRID_SIZE, GRID_SIZE)
            color = (255,0,255) if i == 0 else (122,0,122)
            pygame.draw.rect(surface, color, rect)
            pygame.draw.rect(surface, BLACK, rect, 1)

class Food:
    def __init__(self, snake_positions):
        self.position = self.random_position(snake_positions)
    
    def random_position(self, snake_positions):
        while True:
            pos = (random.randint(0, GRID_WIDTH - 1), random.randint(0, GRID_HEIGHT - 1))
            if pos not in snake_positions:
                return pos
    
    def draw(self, surface):
        x, y = self.position
        rect = pygame.Rect(x * GRID_SIZE, y * GRID_SIZE, GRID_SIZE, GRID_SIZE)
        pygame.draw.rect(surface, RED, rect)
        pygame.draw.rect(surface, BLACK, rect, 1)

def draw_text(surface, text, x, y, font, color=WHITE):
    text_surface = font.render(text, True, color)
    text_rect = text_surface.get_rect(center=(x, y))
    surface.blit(text_surface, text_rect)

def draw_start_screen(surface):
    surface.fill(BLACK)
    
    # Title
    draw_text(surface, "SNAKE GAME", WIDTH // 2, HEIGHT // 3, font_large, (255,0,255))
    
    # Instructions
    draw_text(surface, "Press SPACE to Start", WIDTH // 2, HEIGHT // 2, font_medium, WHITE)
    draw_text(surface, "Use Arrow Keys to Move", WIDTH // 2, HEIGHT // 2 + 60, font_small, GRAY)
    draw_text(surface, "Eat Red Food to Grow", WIDTH // 2, HEIGHT // 2 + 100, font_small, GRAY)
    draw_text(surface, "Don't Hit Yourself!", WIDTH // 2, HEIGHT // 2 + 140, font_small, GRAY)

def draw_game_over_screen(surface, score, high_score):
    surface.fill(BLACK)
    
    # Game Over text
    draw_text(surface, "GAME OVER!", WIDTH // 2, HEIGHT // 3 - 20, font_large, RED)
    
    # Scores
    draw_text(surface, f"Score: {score}", WIDTH // 2, HEIGHT // 2, font_medium, WHITE)
    
    if score == high_score and score > 0:
        draw_text(surface, "NEW HIGH SCORE!", WIDTH // 2, HEIGHT // 2 + 50, font_small, (255,0,255))
        draw_text(surface, f"High Score: {high_score}", WIDTH // 2, HEIGHT // 2 + 90, font_small, GRAY)
    else:
        draw_text(surface, f"High Score: {high_score}", WIDTH // 2, HEIGHT // 2 + 50, font_small, GRAY)
    
    # Instructions
    draw_text(surface, "Press SPACE to Play Again", WIDTH // 2, HEIGHT - 120, font_small, WHITE)
    draw_text(surface, "Press ESC to Quit", WIDTH // 2, HEIGHT - 80, font_small, GRAY)

def main():
    game_state = START
    snake = None
    food = None
    score = 0
    high_score = 0
    running = True
    
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.KEYDOWN:
                if game_state == START:
                    if event.key == pygame.K_SPACE:
                        # Start new game
                        snake = Snake()
                        food = Food(snake.positions)
                        score = 0
                        game_state = PLAYING
                    elif event.key == pygame.K_ESCAPE:
                        running = False
                
                elif game_state == PLAYING:
                    if event.key == pygame.K_UP:
                        snake.change_direction((0, -1))
                    elif event.key == pygame.K_DOWN:
                        snake.change_direction((0, 1))
                    elif event.key == pygame.K_LEFT:
                        snake.change_direction((-1, 0))
                    elif event.key == pygame.K_RIGHT:
                        snake.change_direction((1, 0))
                
                elif game_state == GAME_OVER:
                    if event.key == pygame.K_SPACE:
                        # Restart game
                        snake = Snake()
                        food = Food(snake.positions)
                        score = 0
                        game_state = PLAYING
                    elif event.key == pygame.K_ESCAPE:
                        running = False
        
        # Game logic
        if game_state == PLAYING:
            # Move snake
            if not snake.move():
                if score > high_score:
                    high_score = score
                game_state = GAME_OVER
            
            # Check if snake ate food
            if snake.positions[0] == food.position:
                snake.grow = True
                score += 10
                food = Food(snake.positions)
        
        # Draw everything
        if game_state == START:
            draw_start_screen(screen)
        elif game_state == PLAYING:
            screen.fill(BLACK)
            snake.draw(screen)
            food.draw(screen)
            draw_text(screen, f"Score: {score}", 60, 20, font_small)
            if high_score > 0:
                draw_text(screen, f"High: {high_score}", WIDTH - 60, 20, font_small, GRAY)
        elif game_state == GAME_OVER:
            draw_game_over_screen(screen, score, high_score)
        
        pygame.display.flip()
        clock.tick(FPS if game_state == PLAYING else 60)
    
    pygame.quit()
    sys.exit()

if __name__ == "__main__":
    main()
