import pygame
from random import randint

# Константы для размеров поля и сетки
SCREEN_WIDTH, SCREEN_HEIGHT = 640, 480
GRID_SIZE = 20
GRID_WIDTH = SCREEN_WIDTH // GRID_SIZE
GRID_HEIGHT = SCREEN_HEIGHT // GRID_SIZE

# Направления движения
UP = (0, -1)
DOWN = (0, 1)
LEFT = (-1, 0)
RIGHT = (1, 0)

# Цвета
BOARD_BACKGROUND_COLOR = (0, 0, 0)
BORDER_COLOR = (93, 216, 228)
APPLE_COLOR = (255, 0, 0)
SNAKE_COLOR = (0, 255, 0)

# Настройка игрового окна
pygame.init()
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT), 0, 32)
pygame.display.set_caption("Змейка")

# Настройка времени
clock = pygame.time.Clock()


class GameObject:

    def __init__(self, position=(0, 0)):
        self.position = position
        self.body_color = None  # Это будет переопределено в подклассах

    def draw(self):
        raise NotImplementedError()


class Apple(GameObject):

    def __init__(self):
        super().__init__(self.randomize_position())
        self.body_color = APPLE_COLOR

    def randomize_position(self):
        return (
            randint(0, GRID_WIDTH - 1) * GRID_SIZE,
            randint(0, GRID_HEIGHT - 1) * GRID_SIZE,
        )

    def draw(self):
        rect = pygame.Rect(self.position, (GRID_SIZE, GRID_SIZE))
        pygame.draw.rect(screen, self.body_color, rect)
        pygame.draw.rect(screen, BORDER_COLOR, rect, 1)


class Snake(GameObject):

    def __init__(
        self,
        initial_position=(GRID_WIDTH // 2 * GRID_SIZE, GRID_HEIGHT // 2 * GRID_SIZE),
    ):
        super().__init__(initial_position)
        self.body = [self.position]
        self.positions = self.body  # Новый атрибут positions
        self.direction = (1, 0)  # Начальное направление вправо
        self.body_color = SNAKE_COLOR

    def update(self):
        new_position = (
            self.body[0][0] + self.direction[0] * GRID_SIZE,
            self.body[0][1] + self.direction[1] * GRID_SIZE,
        )
        self.body.insert(0, new_position)
        self.position = new_position
        self.positions = self.body  # Обновление атрибута positions

        if len(self.body) > 1:
            self.body.pop()  # Удаляем последний сегмент

    def draw(self):
        for position in self.body:
            rect = pygame.Rect(position, (GRID_SIZE, GRID_SIZE))
            pygame.draw.rect(screen, self.body_color, rect)
            pygame.draw.rect(screen, BORDER_COLOR, rect, 1)

    def grow(self):
        self.body.append(self.body[-1])  # Увеличиваем длину змейки
        self.positions = self.body  # Обновление атрибута positions

    def get_head_position(self):
        return self.body[0]

    def move(self):
        self.update()

    def reset(self):
        self.body = [self.position]  # Сбрасываем тело
        self.direction = (1, 0)  # Сбрасываем направление

    def update_direction(self, new_direction):
        if (new_direction[0] * -1, new_direction[1] * -1) != self.direction:
            self.direction = new_direction


def handle_keys(snake):
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


def main():
    snake = Snake()
    apple = Apple()

    while True:
        handle_keys(snake)

        snake.move()

        # Обработка столкновений с яблоком
        if snake.get_head_position() == apple.position:
            snake.grow()
            apple = Apple()  # Генерация нового яблока

        screen.fill(BOARD_BACKGROUND_COLOR)
        apple.draw()
        snake.draw()

        pygame.display.update()
        clock.tick(10)  # Установить скорость игры


if __name__ == "main":
    main()
