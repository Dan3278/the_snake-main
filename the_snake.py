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
    """Базовый класс для игровых объектов."""

    def __init__(self, position=(0, 0), body_color=None):
        self.position = position
        self.body_color = body_color

    def draw(self):
        """Нарисуйте игровой объект."""
        rect = pygame.Rect(self.position, (GRID_SIZE, GRID_SIZE))
        pygame.draw.rect(screen, self.body_color, rect)
        pygame.draw.rect(screen, BORDER_COLOR, rect, 1)


class Apple(GameObject):
    """Класс, представляющий яблоко."""

    def __init__(self):
        super().__init__(self.randomize_position(), APPLE_COLOR)

    def randomize_position(self):
        """Случайная позиция для яблока."""
        return (
            randint(0, GRID_WIDTH - 1) * GRID_SIZE,
            randint(0, GRID_HEIGHT - 1) * GRID_SIZE,
        )


class Snake(GameObject):
    """Класс, представляющий змею."""

    def __init__(self):
        initial_position = (GRID_WIDTH // 2 * GRID_SIZE,
                            GRID_HEIGHT // 2 * GRID_SIZE)
        super().__init__(initial_position, SNAKE_COLOR)
        self.body = [self.position]
        self.direction = (1, 0)
        self.speed = 10  # Начальная скорость
        self.positions = self.body.copy()

    def update(self):
        """Изменение положения змеи в зависимости от направления."""
        new_position = (
            self.body[0][0] + self.direction[0] * GRID_SIZE,
            self.body[0][1] + self.direction[1] * GRID_SIZE,
        )
        self.body.insert(0, new_position)

        if len(self.body) > 1:
            self.body.pop()

        self.positions = self.body.copy()

    def draw(self):
        """Нарисует голову и хвост змеи на экране."""
        head_rect = pygame.Rect(self.body[0], (GRID_SIZE, GRID_SIZE))
        pygame.draw.rect(screen, self.body_color, head_rect)
        pygame.draw.rect(screen, BORDER_COLOR, head_rect, 1)

        if len(self.body) > 1:
            tail_rect = pygame.Rect(self.body[-1], (GRID_SIZE, GRID_SIZE))
            pygame.draw.rect(screen, self.body_color, tail_rect)
            pygame.draw.rect(screen, BORDER_COLOR, tail_rect, 1)

    def grow(self):
        """Увеличивает змею, добавляя новый сегмент."""
        self.body.append(self.body[-1])

    def get_head_position(self):
        """Возвращает текущее положение головы змеи."""
        return self.body[0]

    def move(self):
        """Двигает змею, обновляя её положение."""
        self.update()

    def check_collision(self):
        """Проверяет столкновения змеи с границами или саму себя."""
        head = self.get_head_position()
        if any(coord < 0 or coord >= dim
               for coord, dim in zip(head, (SCREEN_WIDTH, SCREEN_HEIGHT))):
            return True
        if head in self.body[1:]:
            return True
        return False

    def update_direction(self, new_direction):
        """Изменяет направление движения змеи."""
        if (new_direction[0] * -1, new_direction[1] * -1) != self.direction:
            self.direction = new_direction

    def update_speed(self, change):
        """Обновляет скорость змеи."""
        self.speed = max(1, self.speed + change)

    def reset(self):
        """Сбрасывает змею в начальное состояние."""
        self.body = [self.position]
        self.direction = (1, 0)
        self.positions = self.body.copy()


def handle_key(snake, event):
    """Обработка нажатий клавиш."""
    if event.key == pygame.K_UP:
        snake.update_direction(UP)
    elif event.key == pygame.K_DOWN:
        snake.update_direction(DOWN)
    elif event.key == pygame.K_LEFT:
        snake.update_direction(LEFT)
    elif event.key == pygame.K_RIGHT:
        snake.update_direction(RIGHT)
    elif event.key == pygame.K_ESCAPE:
        pygame.quit()
        raise SystemExit
    elif event.key == pygame.K_PLUS:
        snake.update_speed(1)
    elif event.key == pygame.K_MINUS:
        snake.update_speed(-1)


def handle_keys(snake):
    """Управление вводом с клавиатуры для управления змеей."""
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            raise SystemExit
        elif event.type == pygame.KEYDOWN:
            handle_key(snake, event)


def show_game_over():
    """Отобразить сообщение об окончании игры."""
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
    """Основная функция для запуска игры."""
    snake = Snake()
    apple = Apple()
    record_length = 0

    while True:
        handle_keys(snake)
        snake.move()

        if snake.check_collision():
            show_game_over()
            break

        if snake.get_head_position() == apple.position:
            snake.grow()
            apple = Apple()
            record_length = max(record_length, len(snake.body))

        screen.fill(BOARD_BACKGROUND_COLOR)
        apple.draw()
        snake.draw()

        pygame.display.set_caption(
            f"Змейка | Скорость: {snake.speed} | "
            f"Рекорд: {record_length} | ESC для выхода"
        )
        pygame.display.update()
        clock.tick(snake.speed)


if __name__ == "__main__":
    main()
