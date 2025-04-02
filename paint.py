import pygame
import sys
from pygame.locals import *

# Initialize pygame
pygame.init()

# Constants
WINDOW_WIDTH = 800
WINDOW_HEIGHT = 600
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)
YELLOW = (255, 255, 0)
PURPLE = (255, 0, 255)
CYAN = (0, 255, 255)
GRAY = (150, 150, 150)

# Tool modes
PEN = 0
RECTANGLE = 1
CIRCLE = 2
ERASER = 3

class PaintApp:
    def __init__(self):
        """Initialize the paint application"""
        self.screen = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
        pygame.display.set_caption("Paint Application")
        
        self.clock = pygame.time.Clock()
        self.drawing = False
        self.last_pos = None
        self.color = BLACK
        self.brush_size = 5
        self.mode = PEN
        self.start_pos = None  # For shapes
        
        # Create a surface for drawing that we can modify
        self.canvas = pygame.Surface((WINDOW_WIDTH, WINDOW_HEIGHT))
        self.canvas.fill(WHITE)
        
        # Available colors
        self.colors = [
            (RED, (10, 10)),
            (GREEN, (50, 10)),
            (BLUE, (90, 10)),
            (YELLOW, (130, 10)),
            (PURPLE, (170, 10)),
            (CYAN, (210, 10)),
            (BLACK, (250, 10))
        ]
        
        # Tool buttons
        self.tools = [
            ("Pen", (350, 10), PEN),
            ("Rect", (400, 10), RECTANGLE),
            ("Circle", (450, 10), CIRCLE),
            ("Eraser", (500, 10), ERASER)
        ]
        
        # Brush size buttons
        self.sizes = [
            ("Small", (600, 10), 3),
            ("Med", (650, 10), 7),
            ("Large", (700, 10), 12)
        ]

    def draw_ui(self):
        """Draw the user interface elements"""
        # Draw color palette
        for color, pos in self.colors:
            pygame.draw.rect(self.screen, color, (*pos, 30, 30))
            if color == self.color:
                pygame.draw.rect(self.screen, BLACK, (*pos, 30, 30), 2)
        
        # Draw tool buttons
        for text, pos, mode in self.tools:
            color = BLUE if self.mode == mode else GRAY
            pygame.draw.rect(self.screen, color, (*pos, 50, 30))
            text_surf = pygame.font.SysFont(None, 20).render(text, True, BLACK)
            self.screen.blit(text_surf, (pos[0] + 5, pos[1] + 5))
        
        # Draw brush size buttons
        for text, pos, size in self.sizes:
            color = BLUE if self.brush_size == size else GRAY
            pygame.draw.rect(self.screen, color, (*pos, 50, 30))
            text_surf = pygame.font.SysFont(None, 20).render(text, True, BLACK)
            self.screen.blit(text_surf, (pos[0] + 5, pos[1] + 5))
        
        # Draw clear button
        pygame.draw.rect(self.screen, RED, (WINDOW_WIDTH - 100, 10, 80, 30))
        text_surf = pygame.font.SysFont(None, 20).render("Clear", True, WHITE)
        self.screen.blit(text_surf, (WINDOW_WIDTH - 90, 15))

    def handle_events(self):
        """Handle user input events"""
        for event in pygame.event.get():
            if event.type == QUIT:
                pygame.quit()
                sys.exit()
            
            elif event.type == MOUSEBUTTONDOWN:
                if event.button == 1:  # Left click
                    # Check if clicking on color palette
                    for color, pos in self.colors:
                        if pygame.Rect(*pos, 30, 30).collidepoint(event.pos):
                            self.color = color
                            return
                    
                    # Check if clicking on tool buttons
                    for _, pos, mode in self.tools:
                        if pygame.Rect(*pos, 50, 30).collidepoint(event.pos):
                            self.mode = mode
                            return
                    
                    # Check if clicking on size buttons
                    for _, pos, size in self.sizes:
                        if pygame.Rect(*pos, 50, 30).collidepoint(event.pos):
                            self.brush_size = size
                            return
                    
                    # Check if clicking clear button
                    if pygame.Rect(WINDOW_WIDTH - 100, 10, 80, 30).collidepoint(event.pos):
                        self.canvas.fill(WHITE)
                        return
                    
                    # Start drawing
                    self.drawing = True
                    self.last_pos = event.pos
                    self.start_pos = event.pos
            
            elif event.type == MOUSEBUTTONUP:
                if event.button == 1:  # Left click release
                    self.drawing = False
                    if self.mode in [RECTANGLE, CIRCLE] and self.start_pos:
                        # Draw the final shape
                        self.draw_shape(self.start_pos, event.pos, True)
                    self.start_pos = None
            
            elif event.type == MOUSEMOTION and self.drawing:
                if self.mode == PEN:
                    self.draw_line(self.last_pos, event.pos)
                    self.last_pos = event.pos
                elif self.mode == ERASER:
                    self.draw_line(self.last_pos, event.pos, True)
                    self.last_pos = event.pos
                elif self.mode in [RECTANGLE, CIRCLE]:
                    # Redraw canvas to remove previous temporary shape
                    temp_canvas = self.canvas.copy()
                    self.draw_shape(self.start_pos, event.pos)
                    self.canvas.blit(temp_canvas, (0, 0))
                    self.draw_shape(self.start_pos, event.pos)

    def draw_line(self, start, end, is_eraser=False):
        """Draw a line between two points"""
        color = WHITE if is_eraser else self.color
        pygame.draw.line(self.canvas, color, start, end, self.brush_size)
        # Draw circles at the ends for smoother lines
        pygame.draw.circle(self.canvas, color, start, self.brush_size // 2)
        pygame.draw.circle(self.canvas, color, end, self.brush_size // 2)

    def draw_shape(self, start, end, final=False):
        """Draw a rectangle or circle"""
        x1, y1 = start
        x2, y2 = end
        rect = pygame.Rect(min(x1, x2), min(y1, y2), abs(x1 - x2), abs(y1 - y2))
        
        if self.mode == RECTANGLE:
            if final:
                pygame.draw.rect(self.canvas, self.color, rect, self.brush_size)
            else:
                # Draw temporary rectangle (on screen, not canvas)
                temp_surf = pygame.Surface((WINDOW_WIDTH, WINDOW_HEIGHT), pygame.SRCALPHA)
                pygame.draw.rect(temp_surf, (*self.color, 128), rect, self.brush_size)
                self.screen.blit(temp_surf, (0, 0))
        
        elif self.mode == CIRCLE:
            center = (x1 + (x2 - x1) // 2, y1 + (y2 - y1) // 2)
            radius = max(abs(x2 - x1) // 2, abs(y2 - y1) // 2)
            if final:
                pygame.draw.circle(self.canvas, self.color, center, radius, self.brush_size)
            else:
                # Draw temporary circle (on screen, not canvas)
                temp_surf = pygame.Surface((WINDOW_WIDTH, WINDOW_HEIGHT), pygame.SRCALPHA)
                pygame.draw.circle(temp_surf, (*self.color, 128), center, radius, self.brush_size)
                self.screen.blit(temp_surf, (0, 0))

    def run(self):
        """Main application loop"""
        while True:
            self.screen.fill(WHITE)
            self.screen.blit(self.canvas, (0, 0))
            
            self.handle_events()
            self.draw_ui()
            
            pygame.display.flip()
            self.clock.tick(60)

if __name__ == "__main__":
    app = PaintApp()
    app.run()