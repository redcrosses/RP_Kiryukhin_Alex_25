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
GRAY = (100, 100, 100)

RED = (255, 0, 0)
PURPLE = (128, 0, 255)
BLUE = (0, 0, 255)


# Initialize screen (module-level so ROS and standalone share it)
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Snake Game")
clock = pygame.time.Clock()
font_large = pygame.font.Font(None, 72)
font_medium = pygame.font.Font(None, 48)
font_small = pygame.font.Font(None, 36)

class Snake:
    def __init__(self):
        self.positions = [(GRID_WIDTH // 2, GRID_HEIGHT // 2)]
        self.direction = (1, 0)
        self.grow = False
        self.eaten = 0
    
    def move(self):
        head_x, head_y = self.positions[0]
        dir_x, dir_y = self.direction
        new_head = ((head_x + dir_x) % GRID_WIDTH, (head_y + dir_y) % GRID_HEIGHT)
        
        # Game over if snake hits itself
        if new_head in self.positions[1:]:
            return False
        
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
    
    def draw(self, surface, color):        
        for i, pos in enumerate(self.positions):
            x, y = pos
            rect = pygame.Rect(x * GRID_SIZE, y * GRID_SIZE, GRID_SIZE, GRID_SIZE)
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

def draw_game_over_screen(surface, score, high_score):
    surface.fill(BLACK)
    
    draw_text(surface, "GAME OVER!", WIDTH // 2, HEIGHT // 3 - 20, font_large, RED)
    draw_text(surface, f"Score: {score}", WIDTH // 2, HEIGHT // 2, font_medium, WHITE)
    
    if score == high_score and score > 0:
        draw_text(surface, "NEW HIGH SCORE!", WIDTH // 2, HEIGHT // 2 + 50, font_small, (255, 0, 255))
        draw_text(surface, f"High Score: {high_score}", WIDTH // 2, HEIGHT // 2 + 90, font_small, GRAY)
    else:
        draw_text(surface, f"High Score: {high_score}", WIDTH // 2, HEIGHT // 2 + 50, font_small, GRAY)
    
    draw_text(surface, "Press SPACE to Play Again", WIDTH // 2, HEIGHT - 120, font_small, WHITE)
    draw_text(surface, "Press ESC to Quit", WIDTH // 2, HEIGHT - 80, font_small, GRAY)


class Game:
    """
    Wrapper around your Snake game so ROS can control it.

    Methods ROS will use:
      - handle_command(cmd)
      - update()
      - draw()
      - is_over()
      - get_score()
    """
    def __init__(self):
        self.running = True
        self.high_score = 0
        self.reset()
        self.difficulty = 1
        self.color_param = 'red'

    def reset(self):
        self.game_state = "PLAYING"   # only PLAYING / GAME_OVER for ROS
        self.snake = Snake()
        self.food = [Food(self.snake.positions)]
        self.score = 0
        self.time = 0

    def handle_command(self, cmd: str):
        """
        cmd will be strings sent from ROS, e.g. "UP", "DOWN", "LEFT", "RIGHT", "QUIT".
        """
        if cmd == "QUIT":
            self.running = False
            return

        if self.game_state == "PLAYING":
            if cmd == "UP":
                self.snake.change_direction((0, -1))
            elif cmd == "DOWN":
                self.snake.change_direction((0, 1))
            elif cmd == "LEFT":
                self.snake.change_direction((-1, 0))
            elif cmd == "RIGHT":
                self.snake.change_direction((1, 0))
            elif cmd == '1':
                self.difficulty = 1
            elif cmd == '2':
                self.difficulty = 2
            elif cmd == '3':
                self.difficulty = 3
            

        # Optional: allow restart when game over
        if self.game_state == "GAME_OVER" and cmd == "SPACE":
            self.reset()

    def update(self):
        """Advance the game logic by one step."""
        if self.game_state == "PLAYING":
            # Move snake
            if not self.snake.move():
                # Game over
                if self.score > self.high_score:
                    self.high_score = self.score
                self.game_state = "GAME_OVER"
                # for ROS we can also consider this "finished"
                self.running = False
            else:
                # Check collisions with food
                for i, f in enumerate(self.food):
                    if self.snake.positions[0] == f.position: #collision
                        self.snake.eaten += 1
                        self.food.pop(i)
                
                if self.snake.eaten >= self.difficulty:
                    self.snake.grow = True
                    self.score += 10
                    self.snake.eaten = 0

                # Add more food every 20 ticks
                if self.time % (10*self.difficulty) == 0:
                    self.food.append(Food(self.snake.positions))

        self.time += 1

    def draw(self):
        """Draw one frame."""
        if self.game_state == "PLAYING":
            screen.fill(BLACK)
            if self.color_param == 'red': color = RED
            elif self.color_param == 'purple': color = PURPLE
            elif self.color_param == 'blue': color = BLUE
            else: color = GRAY
            self.snake.draw(screen, color=color)
            for f in self.food:
                f.draw(screen)
            draw_text(screen, f"Score: {self.score}", 60, 20, font_small)
            draw_text(screen, f"Difficulty: {self.difficulty}", 70, 40, font_small)
            draw_text(screen, f"Eaten: {self.snake.eaten}", 40, 60, font_small)
            if self.high_score > 0:
                draw_text(screen, f"High: {self.high_score}", WIDTH - 60, 20, font_small, GRAY)
        elif self.game_state == "GAME_OVER":
            draw_game_over_screen(screen, self.score, self.high_score)

        pygame.display.flip()
        clock.tick(FPS if self.game_state == "PLAYING" else 60)

    def is_over(self) -> bool:
        """Tell ROS or the standalone runner if the game is finished."""
        return not self.running

    def get_score(self) -> int:
        return self.score


# ---------------- Standalone runner (for testing without ROS) ---------------- #

def main():
    game = Game()

    while not game.is_over():
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                game.handle_command("QUIT")
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_UP:
                    game.handle_command("UP")
                elif event.key == pygame.K_DOWN:
                    game.handle_command("DOWN")
                elif event.key == pygame.K_LEFT:
                    game.handle_command("LEFT")
                elif event.key == pygame.K_RIGHT:
                    game.handle_command("RIGHT")
                elif event.key == pygame.K_1:
                    game.handle_command("1")
                elif event.key == pygame.K_2:
                    game.handle_command("2")
                elif event.key == pygame.K_3:
                    game.handle_command("3")
                elif event.key == pygame.K_ESCAPE:
                    game.handle_command("QUIT")

        game.update()
        game.draw()

    pygame.quit()
    sys.exit()


if __name__ == "__main__":
    main()
