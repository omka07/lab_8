import pygame
import random
import sys
from pygame.locals import *

# Initialize pygame
pygame.init()

# Constants
SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600
ROAD_WIDTH = 400
CAR_WIDTH = 50
CAR_HEIGHT = 100
COIN_SIZE = 30
FPS = 60

# Colors (all defined now)
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
GRAY = (100, 100, 100)
GREEN = (0, 128, 0)
YELLOW = (255, 255, 0)
RED = (255, 0, 0)
BLUE = (0, 0, 255)  # Added missing color definition

class Car(pygame.sprite.Sprite):
    """Player's car class"""
    def __init__(self):
        super().__init__()
        self.image = pygame.Surface((CAR_WIDTH, CAR_HEIGHT))
        self.image.fill(RED)
        self.rect = self.image.get_rect()
        self.rect.center = (SCREEN_WIDTH // 2, SCREEN_HEIGHT - CAR_HEIGHT - 20)
        self.speed = 5

    def update(self):
        """Update car position based on key presses"""
        keys = pygame.key.get_pressed()
        if keys[K_LEFT] and self.rect.left > (SCREEN_WIDTH - ROAD_WIDTH) // 2:
            self.rect.x -= self.speed
        if keys[K_RIGHT] and self.rect.right < (SCREEN_WIDTH + ROAD_WIDTH) // 2:
            self.rect.x += self.speed
        if keys[K_UP] and self.rect.top > 0:
            self.rect.y -= self.speed
        if keys[K_DOWN] and self.rect.bottom < SCREEN_HEIGHT:
            self.rect.y += self.speed

class Obstacle(pygame.sprite.Sprite):
    """Obstacle cars class"""
    def __init__(self):
        super().__init__()
        self.image = pygame.Surface((CAR_WIDTH, CAR_HEIGHT))
        self.image.fill(BLUE)
        self.rect = self.image.get_rect()
        self.rect.x = random.randint(
            (SCREEN_WIDTH - ROAD_WIDTH) // 2,
            (SCREEN_WIDTH + ROAD_WIDTH) // 2 - CAR_WIDTH
        )
        self.rect.y = -CAR_HEIGHT
        self.speed = random.randint(3, 8)

    def update(self):
        """Move obstacle down the screen"""
        self.rect.y += self.speed
        if self.rect.top > SCREEN_HEIGHT:
            self.kill()

class Coin(pygame.sprite.Sprite):
    """Collectible coins class"""
    def __init__(self):
        super().__init__()
        self.image = pygame.Surface((COIN_SIZE, COIN_SIZE), pygame.SRCALPHA)  # SRCALPHA for transparency
        pygame.draw.circle(self.image, YELLOW, (COIN_SIZE//2, COIN_SIZE//2), COIN_SIZE//2)
        self.rect = self.image.get_rect()
        self.rect.x = random.randint(
            (SCREEN_WIDTH - ROAD_WIDTH) // 2,
            (SCREEN_WIDTH + ROAD_WIDTH) // 2 - COIN_SIZE
        )
        self.rect.y = random.randint(-1000, -COIN_SIZE)
        self.speed = random.randint(2, 5)

    def update(self):
        """Move coin down the screen"""
        self.rect.y += self.speed
        if self.rect.top > SCREEN_HEIGHT:
            self.kill()

class Game:
    """Main game class"""
    def __init__(self):
        self.screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
        pygame.display.set_caption("Racer Game")
        self.clock = pygame.time.Clock()
        self.font = pygame.font.SysFont('Arial', 24)
        self.running = True
        self.score = 0
        self.coins_collected = 0
        self.game_over = False
        
        # Sprite groups
        self.all_sprites = pygame.sprite.Group()
        self.obstacles = pygame.sprite.Group()
        self.coins = pygame.sprite.Group()
        
        # Create player car
        self.car = Car()
        self.all_sprites.add(self.car)
        
        # Timers for spawning objects
        self.obstacle_timer = 0
        self.coin_timer = 0

    def spawn_obstacles(self):
        """Spawn new obstacles at random intervals"""
        self.obstacle_timer += 1
        if self.obstacle_timer > random.randint(60, 120):
            new_obstacle = Obstacle()
            self.obstacles.add(new_obstacle)
            self.all_sprites.add(new_obstacle)
            self.obstacle_timer = 0

    def spawn_coins(self):
        """Spawn new coins at random intervals"""
        self.coin_timer += 1
        if self.coin_timer > random.randint(90, 180):
            new_coin = Coin()
            self.coins.add(new_coin)
            self.all_sprites.add(new_coin)
            self.coin_timer = 0

    def handle_events(self):
        """Handle game events"""
        for event in pygame.event.get():
            if event.type == QUIT:
                self.running = False
            if event.type == KEYDOWN:
                if event.key == K_ESCAPE:
                    self.running = False
                if event.key == K_r and self.game_over:
                    self.__init__()  # Reset game

    def update(self):
        """Update game state"""
        if not self.game_over:
            # Spawn objects
            self.spawn_obstacles()
            self.spawn_coins()
            
            # Update all sprites
            self.all_sprites.update()
            
            # Check for collisions with obstacles
            if pygame.sprite.spritecollide(self.car, self.obstacles, False):
                self.game_over = True
            
            # Check for coin collection
            coins_hit = pygame.sprite.spritecollide(self.car, self.coins, True)
            for coin in coins_hit:
                self.coins_collected += 1
                self.score += 10

    def draw(self):
        """Draw everything to the screen"""
        # Draw background
        self.screen.fill(GREEN)
        pygame.draw.rect(self.screen, GRAY, 
                         ((SCREEN_WIDTH - ROAD_WIDTH) // 2, 0, ROAD_WIDTH, SCREEN_HEIGHT))
        
        # Draw road markings
        for y in range(0, SCREEN_HEIGHT, 40):
            pygame.draw.rect(self.screen, WHITE, 
                             (SCREEN_WIDTH // 2 - 5, y, 10, 20))
        
        # Draw all sprites
        self.all_sprites.draw(self.screen)
        
        # Draw score and coins counter
        score_text = self.font.render(f"Score: {self.score}", True, WHITE)
        coins_text = self.font.render(f"Coins: {self.coins_collected}", True, WHITE)
        self.screen.blit(score_text, (10, 10))
        self.screen.blit(coins_text, (SCREEN_WIDTH - 120, 10))
        
        # Draw game over screen if needed
        if self.game_over:
            game_over_text = self.font.render("GAME OVER - Press R to restart", True, RED)
            self.screen.blit(game_over_text, 
                            (SCREEN_WIDTH // 2 - game_over_text.get_width() // 2, 
                             SCREEN_HEIGHT // 2))
        
        pygame.display.flip()

    def run(self):
        """Main game loop"""
        while self.running:
            self.clock.tick(FPS)
            self.handle_events()
            self.update()
            self.draw()

        pygame.quit()
        sys.exit()

if __name__ == "__main__":
    game = Game()
    game.run()