import pygame
import sys
from Model import Model, Position
from ObserverModel import Observer, Subject

WHITE = (255, 255, 255)
GREEN = '#2d8b2c'
BLUE = (0, 0, 255)
BLACK = (0, 0, 0)
TEXT_BACKGROUND_COLOR = (70, 70, 100)  # Slightly lighter blue for text background
TEXT_COLOR = '#fff207'  # Bright yellow text color
HIGHLIGHT_COLOR = (100, 100, 150)  # Optional highlight/border color

# Set up display constants
WINDOW_WIDTH = 800
WINDOW_HEIGHT = 600

# Initialize Pygame
pygame.init()

class CharacterView:
    def __init__(self, character):
        self.image = pygame.image.load(f"assets/vignette_{character.name}.png")
        self.image = pygame.transform.scale(self.image, (128, 128))
        self.rect = self.image.get_rect()
        self.character = character

# View class: Handles rendering of the game
class View(Observer):
    def load_font(self) -> None:
        # Load a fun, playful font
        # Note: Make sure you have a fun font installed, or pygame will use default
        try:
            # Try loading a playful font (you might need to adjust the path)
            self.font = pygame.font.Font(pygame.font.match_font('comic sans ms'), 36)
        except:
            # Fallback to default font if comic sans isn't available
            self.font = pygame.font.Font(None, 36)

    def __init__(self, screen, font, model):
        self.screen = screen
        self.font = font
        self.model = model
        self.character_views = {character.name: CharacterView(character) for character in model.characters}
        self.model.attach(self)
        self.message = ""

    def draw_background(self):
        # draw grass
        self.screen.fill(GREEN)
        # draw river
        pygame.draw.rect(self.screen, '#3861dc', (WINDOW_WIDTH // 2 - 50, 0, 100, WINDOW_HEIGHT))

    def draw_characters(self):
        """Draw characters on the screen."""
        for character_view in self.character_views.values():
            y = 30 + (135 * list(self.character_views.values()).index(character_view))
            if character_view.character.position == Position.LEFT:
                x = 95
            else:
                x = WINDOW_WIDTH - character_view.rect.width - 95
            character_view.rect.topleft = (x, y)
            self.screen.blit(character_view.image, character_view.rect.topleft)

    def draw_text(self):
        """Draw text on the screen."""
        self.text = self.font.render(self.message, True, TEXT_COLOR)
        self.text_rect = self.text.get_rect(center=(WINDOW_WIDTH // 2, WINDOW_HEIGHT- 30))

        # Calculate text position and background rectangle
        text_width = self.text.get_width()
        text_height = self.text.get_height()
        text_x = (WINDOW_WIDTH - text_width) // 2
        text_y = WINDOW_HEIGHT - text_height - 20  # 20 pixels from bottom

        # Create background rectangle with padding
        padding = 10  # Space around the text
        rect_x = text_x - padding
        rect_y = text_y - padding
        rect_width = text_width + (2 * padding)
        rect_height = text_height + (2 * padding)

        # Draw background rectangle for text
        pygame.draw.rect(self.screen, HIGHLIGHT_COLOR,
                         (rect_x - 2, rect_y - 2,
                          rect_width + 4, rect_height + 4),
                         border_radius=10)

        # Main text background
        pygame.draw.rect(self.screen, TEXT_BACKGROUND_COLOR,
                         (rect_x, rect_y, rect_width, rect_height),
                         border_radius=8)

        self.screen.blit(self.text, self.text_rect)

    def is_character_clicked(self, character_view, pos):
        """Check if a character was clicked based on position."""
        return character_view.rect.collidepoint(pos)

    def update(self, subject: Subject):
        self.draw_characters()
        state = self.model.get_state()
        self.message = state[1]

# Main class: Handles the game loop and event handling
class Main:
    def __init__(self):
        self.screen = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
        pygame.display.set_caption("River Crossing Puzzle")
        self.font = pygame.font.SysFont(None, 36)

        self.model = Model()
        self.view = View(self.screen, self.font, self.model)

        self.running = True

    def handle_events(self):
        """Processes all game events."""
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.running = False
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    self.running = False
                elif event.key == pygame.K_r:
                    self.model.reset()
            elif event.type == pygame.MOUSEBUTTONDOWN:
                for character_view in self.view.character_views.values():
                    if self.view.is_character_clicked(character_view, event.pos):
                        self.model.toggle_character_position(character_view.character.name)

    def game_loop(self):
        """Runs the main game loop."""
        while self.running:
            self.handle_events()

            # Draw everything
            self.view.draw_background()
            self.view.draw_characters()
            if self.model.get_state()[1] != "":
                self.view.draw_text()

            # Update display
            pygame.display.flip()

        pygame.quit()
        sys.exit()

# Run the game
if __name__ == "__main__":
    game = Main()
    game.game_loop()
