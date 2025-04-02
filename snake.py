import pygame
import random
import sys
from pygame.locals import *

# Initialize pygame
pygame.init()

# Constants
WINDOW_WIDTH = 600
WINDOW_HEIGHT = 600
GRID_SIZE = 20
GRID_WIDTH = WINDOW_WIDTH // GRID_SIZE
GRID_HEIGHT = WINDOW_HEIGHT // GRID_SIZE
FPS = 10

# Colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
GREEN = (0, 255, 0)
RED = (255, 0, 0)
BLUE = (0, 0, 255)
GRAY = (100, 100, 100)

# Directions
UP = (0, -1)
DOWN = (0, 1)
LEFT = (-1, 0)
RIGHT = (1, 0)

class Snake:
    def __init__(self):
        """Initialize the snake with starting position and length"""
        self.positions = [(GRID_WIDTH // 2, GRID_HEIGHT // 2)]
        self.length = 1
        self.direction = RIGHT
        self.color = GREEN
        self.score = 0
        self.level = 1
        self.foods_eaten = 0
        self.foods_to_next_level = 3  # Foods needed to advance to next level

    def get_head_position(self):
        """Return the position of the snake's head"""
        return self.positions[0]

    def update(self):
        """Update the snake's position based on current direction"""
        head_x, head_y = self.get_head_position()
        dir_x, dir_y = self.direction
        new_x = (head_x + dir_x) % GRID_WIDTH
        new_y = (head_y + dir_y) % GRID_HEIGHT
        
        # Check for wall collision (game over if hits wall)
        if new_x < 0 or new_x >= GRID_WIDTH or new_y < 0 or new_y >= GRID_HEIGHT:
            return True  # Game over
        
        # Check for self collision
        if (new_x, new_y) in self.positions[:-1]:
            return True  # Game over
        
        self.positions.insert(0, (new_x, new_y))
        if len(self.positions) > self.length:
            self.positions.pop()
        
        return False  # Game continues

    def reset(self):
        """Reset the snake to initial state"""
        self.positions = [(GRID_WIDTH // 2, GRID_HEIGHT // 2)]
        self.length = 1
        self.direction = RIGHT
        self.score = 0
        self.level = 1
        self.foods_eaten = 0

    def render(self, surface):
        """Draw the snake on the game surface"""
        for position in self.positions:
            rect = pygame.Rect((position[0] * GRID_SIZE, position[1] * GRID_SIZE), (GRID_SIZE, GRID_SIZE))
            pygame.draw.rect(surface, self.color, rect)
            pygame.draw.rect(surface, BLACK, rect, 1)  # Border

class Food:
    def __init__(self, snake_positions):
        """Initialize food at a random position not occupied by snake"""
        self.position = (0, 0)
        self.color = RED
        self.randomize_position(snake_positions)

    def randomize_position(self, snake_positions):
        """Generate random position for food that doesn't overlap with snake"""
        while True:
            self.position = (random.randint(0, GRID_WIDTH - 1), random.randint(0, GRID_HEIGHT - 1))
            if self.position not in snake_positions:
                break

    def render(self, surface):
        """Draw the food on the game surface"""
        rect = pygame.Rect((self.position[0] * GRID_SIZE, self.position[1] * GRID_SIZE), (GRID_SIZE, GRID_SIZE))
        pygame.draw.rect(surface, self.color, rect)
        pygame.draw.rect(surface, BLACK, rect, 1)  # Border

def draw_grid(surface):
    """Draw grid lines on the game surface"""
    for y in range(0, WINDOW_HEIGHT, GRID_SIZE):
        for x in range(0, WINDOW_WIDTH, GRID_SIZE):
            rect = pygame.Rect((x, y), (GRID_SIZE, GRID_SIZE))
            pygame.draw.rect(surface, GRAY, rect, 1)

def show_game_over(surface, score, level):
    """Display game over screen with final score and level"""
    font = pygame.font.SysFont('arial', 36)
    game_over_text = font.render("GAME OVER", True, RED)
    score_text = font.render(f"Score: {score}", True, WHITE)
    level_text = font.render(f"Level: {level}", True, WHITE)
    restart_text = font.render("Press R to restart", True, WHITE)
    
    surface.blit(game_over_text, (WINDOW_WIDTH // 2 - game_over_text.get_width() // 2, WINDOW_HEIGHT // 2 - 60))
    surface.blit(score_text, (WINDOW_WIDTH // 2 - score_text.get_width() // 2, WINDOW_HEIGHT // 2))
    surface.blit(level_text, (WINDOW_WIDTH // 2 - level_text.get_width() // 2, WINDOW_HEIGHT // 2 + 40))
    surface.blit(restart_text, (WINDOW_WIDTH // 2 - restart_text.get_width() // 2, WINDOW_HEIGHT // 2 + 80))

def show_score(surface, score, level):
    """Display current score and level during gameplay"""
    font = pygame.font.SysFont('arial', 20)
    score_text = font.render(f"Score: {score}", True, WHITE)
    level_text = font.render(f"Level: {level}", True, WHITE)
    surface.blit(score_text, (10, 10))
    surface.blit(level_text, (10, 30))

def main():
    """Main game function"""
    clock = pygame.time.Clock()
    screen = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
    pygame.display.set_caption("Enhanced Snake Game")
    
    snake = Snake()
    food = Food(snake.positions)
    
    game_over = False
    base_speed = FPS
    current_speed = base_speed
    
    while True:
        for event in pygame.event.get():
            if event.type == QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == KEYDOWN:
                if game_over:
                    if event.key == K_r:
                        # Reset game
                        snake.reset()
                        food.randomize_position(snake.positions)
                        game_over = False
                        current_speed = base_speed
                else:
                    # Handle direction changes (no 180-degree turns allowed)
                    if event.key == K_UP and snake.direction != DOWN:
                        snake.direction = UP
                    elif event.key == K_DOWN and snake.direction != UP:
                        snake.direction = DOWN
                    elif event.key == K_LEFT and snake.direction != RIGHT:
                        snake.direction = LEFT
                    elif event.key == K_RIGHT and snake.direction != LEFT:
                        snake.direction = RIGHT
        
        if not game_over:
            # Update snake position
            game_over = snake.update()
            
            # Check if snake ate food
            if snake.get_head_position() == food.position:
                snake.length += 1
                snake.score += 10
                snake.foods_eaten += 1
                food.randomize_position(snake.positions)
                
                # Check for level up
                if snake.foods_eaten >= snake.foods_to_next_level:
                    snake.level += 1
                    snake.foods_eaten = 0
                    current_speed = base_speed + snake.level  # Increase speed with level
            
            # Clear screen
            screen.fill(BLACK)
            draw_grid(screen)
            
            # Draw game elements
            snake.render(screen)
            food.render(screen)
            show_score(screen, snake.score, snake.level)
        else:
            # Show game over screen
            show_game_over(screen, snake.score, snake.level)
        
        pygame.display.update()
        clock.tick(current_speed)

if __name__ == "__main__":
    main()