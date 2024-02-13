from random import choice, randint
from typing import Tuple, Any, Optional
import pygame
import sys

# Определение констант направлений
UP: Tuple[int, int] = (0, -1)
DOWN: Tuple[int, int] = (0, 1)
LEFT: Tuple[int, int] = (-1, 0)
RIGHT: Tuple[int, int] = (1, 0)

# Определение константы скорости
SPEED: int = 20

# Выбранные стандартные цвета для игрового поля
BLACK: Tuple[int, int, int] = (0, 0, 0)
WHITE: Tuple[int, int, int] = (255, 255, 255)
GREEN: Tuple[int, int, int] = (0, 255, 0)
RED: Tuple[int, int, int] = (255, 0, 0)

# Размеры игрового поля и ячеек
HEIGHT: int = 480
WIDTH: int = 640
CELL_SIZE: int = 20

# Расположение змейки в начале игры
CENTER: Tuple[int, int] = (HEIGHT // 2, WIDTH // 2)

# Рассчитываем количество рядов (rows) и колонн (columns)
ROWS: int = WIDTH // CELL_SIZE
COLUMNS: int = HEIGHT // CELL_SIZE

# создание экрана
pygame.init()
screen = pygame.display.set_mode((WIDTH, HEIGHT))
clock = pygame.time.Clock()
pygame.display.set_caption('Игровое поле')


class Apple:
    """Класс яблока."""

    def __init__(self):
        self.body_color = RED
        self.randomize_position()

    def randomize_position(self) -> None:
        """Метод для рандомного расположения яблока на экране."""
        self.position = (
            randint(0, ROWS - 1) * CELL_SIZE,
            randint(0, COLUMNS - 1) * CELL_SIZE
        )

    def draw(self, surface):
        """Метод для изображения яблок на поверхности."""
        rectangle = pygame.Rect(
            (self.position[0], self.position[1]),
            (CELL_SIZE, CELL_SIZE)
        )
        pygame.draw.rect(surface, self.body_color, rectangle)
        pygame.draw.rect(surface, WHITE, rectangle, 1)


class Snake:
    """Класс Змеи."""

    length: int = 1
    positions: Any = None
    direction: Any = None
    next_direction: Optional[Tuple[Tuple, Tuple]] = None
    last: Any = None

    def __init__(self):
        self.body_color = GREEN
        self.direction = choice([UP, DOWN, LEFT, RIGHT])
        self.positions = [CENTER]

    def update_direction(self) -> None:
        """Обновление движения змейки."""
        if self.next_direction:
            self.direction = self.next_direction
            self.next_direction = None

    def move(self) -> None:
        """Метод для движения змеи."""
        new_position = (
            self.positions[0][0] + self.direction[0] * CELL_SIZE,
            self.positions[0][1] + self.direction[1] * CELL_SIZE
        )
        list.insert(self.positions, 0, new_position)
        self.last = self.positions[-1]
        self.positions = self.positions[: -1]

    def draw(self, surface):
        """Метод для рисования змеи на экране."""
        # Рисуем голову змеи.
        head = self.positions[0]
        head_rect = pygame.Rect((head[0], head[1]), (CELL_SIZE, CELL_SIZE))
        pygame.draw.rect(surface, GREEN, head_rect)
        pygame.draw.rect(surface, WHITE, head_rect, 1)

        for position in self.positions[1:]:
            rect = (
                pygame.Rect((position[0], position[1]), (CELL_SIZE, CELL_SIZE))
            )
            pygame.draw.rect(surface, self.body_color, rect)
            pygame.draw.rect(surface, WHITE, rect, 1)

        # Затирка последнего сегмента змеи.
        if self.last:
            last_rect = pygame.Rect(
                (self.last[0], self.last[1]),
                (CELL_SIZE, CELL_SIZE)
            )
            pygame.draw.rect(surface, BLACK, last_rect)

    def get_head_position(self) -> Tuple[int, int]:
        """Определение координат змеиной головы."""
        return self.positions[0][0], self.positions[0][1]

    def reset(self, surface) -> None:
        """Метод для возвращения змеи в начальное состояние."""
        for each in self.positions:
            rect = pygame.Rect(
                (each[0], each[1]),
                (CELL_SIZE, CELL_SIZE)
            )
            pygame.draw.rect(surface, BLACK, rect)
        self.positions = [CENTER]
        self.direction = choice([UP, DOWN, LEFT, RIGHT])
        self.last = None


def handle_keys(game_object: Snake) -> None:
    """Функция для управления змеей."""
    console: dict = {
        (pygame.K_UP, RIGHT): UP,
        (pygame.K_UP, LEFT): UP,
        (pygame.K_RIGHT, UP): RIGHT,
        (pygame.K_RIGHT, DOWN): RIGHT,
        (pygame.K_DOWN, LEFT): DOWN,
        (pygame.K_DOWN, RIGHT): DOWN,
        (pygame.K_LEFT, UP): LEFT,
        (pygame.K_LEFT, DOWN): LEFT
    }
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
        elif event.type == pygame.KEYDOWN:
            if (event.key, game_object.direction) in console:
                game_object.next_direction = console[
                    (event.key, game_object.direction)
                ]
            if event.key == pygame.K_ESCAPE:
                pygame.quit()
                sys.exit()


def new_apple(snake: Snake) -> Apple:
    """Функция Для создания новых яблок."""
    while True:
        apple = Apple()
        if apple.position not in snake.positions:
            break
    return apple


def infinite_way(snake: Snake) -> Snake:
    """Функция для перемещения змеи через границы поля."""
    head_pos_x: int = snake.get_head_position()[0]
    head_pos_y: int = snake.get_head_position()[1]

    if head_pos_x >= WIDTH:
        head_pos_x = 0
    elif head_pos_x < 0:
        head_pos_x = WIDTH - CELL_SIZE

    if head_pos_y >= HEIGHT:
        head_pos_y = 0
    elif head_pos_y < 0:
        head_pos_y = HEIGHT - CELL_SIZE

    snake.positions[0] = (head_pos_x, head_pos_y)
    return snake


def main():
    """Главная функиця игры."""
    snake = Snake()
    apple = new_apple(snake)
    speed = SPEED
    while True:
        clock.tick(speed)

        handle_keys(snake)
        snake.update_direction()
        snake.move()
        snake = infinite_way(snake)
        apple.draw(screen)
        snake.draw(screen)
        if snake.positions[0] == apple.position:
            snake.positions.append(snake.last)
            snake.last = None
            apple = new_apple(snake)
            snake.length += 1

        if snake.positions[0] in snake.positions[1:]:
            snake.reset(screen)
            speed = SPEED

        pygame.display.update()


if __name__ == '__main__':
    main()
