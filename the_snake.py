import pygame
from random import randint

SCREEN_WIDTH, SCREEN_HEIGHT = 640, 480
GRID_SIZE = 20
GRID_WIDTH = SCREEN_WIDTH // GRID_SIZE
GRID_HEIGHT = SCREEN_HEIGHT // GRID_SIZE

UP = (0, -1)
DOWN = (0, 1)
LEFT = (-1, 0)
RIGHT = (1, 0)

BOARD_BACKGROUND_COLOR = (0, 0, 0)
BORDER_COLOR = (93, 216, 228)
APPLE_COLOR = (255, 0, 0)
SNAKE_COLOR = (0, 255, 0)
GAME_OVER_COLOR = (255, 255, 255)

pygame.init()
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT), 0, 32)
pygame.display.set_caption("Змейка")
clock = pygame.time.Clock()


class GameObject:
    """Base class for game objects."""
    def __init__(self, position=(0, 0)):
        """Initialize the game object with a position."""
        self.position = position
        self.body_color = None

    def draw(self):
        """Draw the game object."""
        raise NotImplementedError()


class Apple(GameObject):
    """Class representing the apple."""

    def __init__(self):
        """Initialize the apple and randomize its position."""
        super().__init__(self.randomize_position())
        self.body_color = APPLE_COLOR

    def randomize_position(self):
        """Randomize the apple's position within the grid."""
        return (
            randint(0, GRID_WIDTH - 1) * GRID_SIZE,
            randint(0, GRID_HEIGHT - 1) * GRID_SIZE,
        )

    def draw(self):
        """Draw the apple on the screen."""
        rect = pygame.Rect(self.position, (GRID_SIZE, GRID_SIZE))
        pygame.draw.rect(screen, self.body_color, rect)
        pygame.draw.rect(screen, BORDER_COLOR, rect, 1)


class Snake(GameObject):
    """Class representing the snake."""

    def __init__(self, initial_position=(GRID_WIDTH // 2 * GRID_SIZE,
                                          GRID_HEIGHT // 2 * GRID_SIZE)):
        """Initialize the snake with a starting position."""
        super().__init__(initial_position)
        self.body = [self.position]
        self.direction = (1, 0)
        self.body_color = SNAKE_COLOR
        self.positions = self.body.copy()

    def update(self):
        """Update the snake's position based on its direction."""
        new_position = (
            self.body[0][0] + self.direction[0] * GRID_SIZE,
            self.body[0][1] + self.direction[1] * GRID_SIZE,
        )
        if new_position[0] < 0:
            new_position = (SCREEN_WIDTH - GRID_SIZE, new_position[1])
        elif new_position[0] >= SCREEN_WIDTH:
            new_position = (0, new_position[1])
        elif new_position[1] < 0:
            new_position = (new_position[0], SCREEN_HEIGHT - GRID_SIZE)
        elif new_position[1] >= SCREEN_HEIGHT:
            new_position = (new_position[0], 0)

        self.body.insert(0, new_position)
        self.positions = self.body.copy()

        if len(self.body) > 1:
            self.body.pop()

    def draw(self):
        """Draw the snake on the screen."""
        for position in self.body:
            rect = pygame.Rect(position, (GRID_SIZE, GRID_SIZE))
            pygame.draw.rect(screen, self.body_color, rect)
            pygame.draw.rect(screen, BORDER_COLOR, rect, 1)

    def grow(self):
        """Grow the snake by adding a new segment."""
        self.body.append(self.body[-1])
        self.positions = self.body.copy()

    def get_head_position(self):
        """Return the current position of the snake's head."""
        return self.body[0]

    def move(self):
        """Move the snake by updating its position."""
        self.update()

    def check_collision(self):
        """Check for collisions with walls or itself."""
        head = self.get_head_position()
        if head[0] < 0 or head[0] >= SCREEN_WIDTH or head[1] < 0 or head[1] >= SCREEN_HEIGHT:
            return True
        if head in self.body[1:]:
            return True
        return False

    def update_direction(self, new_direction):
        """Update the snake's direction if it's not opposite to current direction."""
        if (new_direction[0] * -1, new_direction[1] * -1) != self.direction:
            self.direction = new_direction

    def reset(self):
        """Reset the snake to its initial state."""
        self.body = [self.position]
        self.direction = (1, 0)
        self.positions = self.body.copy()


def handle_keys(snake):
    """Handle keyboard input for controlling the snake."""
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            raise SystemExit
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_UP:
                snake.update_direction(UP)
            elif event.key == pygame.K_DOWN:
                snake.update_direction(DOWN)
            elif event.key == pygame.K_LEFT:
                snake.update_direction(LEFT)
            elif event.key == pygame.K_RIGHT:
                snake.update_direction(RIGHT)


def show_game_over():
    """Display the game over message."""
    font = pygame.font.SysFont('Arial', 36)
    text = font.render('Game Over!', True, GAME_OVER_COLOR)
    screen.blit(
        text,
        (
            SCREEN_WIDTH // 2 - text.get_width() // 2,
            SCREEN_HEIGHT // 2 - text.get_height() // 2
        )
    )
    pygame.display.update()
    pygame.time.wait(2000)


def main():
    """Main function to run the game."""
    snake = Snake()
    apple = Apple()

    while True:
        handle_keys(snake)
        snake.move()

        if snake.check_collision():
            show_game_over()
            break

        if snake.get_head_position() == apple.position:
            snake.grow()
            apple = Apple()

        screen.fill(BOARD_BACKGROUND_COLOR)
        apple.draw()
        snake.draw()

        pygame.display.update()
        clock.tick(10)


if __name__ == "__main__":
    main()
