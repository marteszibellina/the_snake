# -*- coding: utf-8 -*-
"""
Created on: 09.11.2024

@author: dmitry
"""

from random import randrange

import pygame

# Константы для размеров поля и сетки:
SCREEN_WIDTH, SCREEN_HEIGHT = 640, 480
GRID_SIZE = 20
GRID_WIDTH = SCREEN_WIDTH // GRID_SIZE
GRID_HEIGHT = SCREEN_HEIGHT // GRID_SIZE

# Направления движения:
UP = (0, -1)
DOWN = (0, 1)
LEFT = (-1, 0)
RIGHT = (1, 0)

# Цвет фона - черный:
BOARD_BACKGROUND_COLOR = (0, 0, 0)

# Цвет границы ячейки
BORDER_COLOR = (93, 216, 228)

# Цвет яблока
APPLE_COLOR = (255, 0, 0)

# Цвет змейки
SNAKE_COLOR = (0, 255, 0)

# Скорость движения змейки:
SPEED = 20

# Настройка игрового окна:
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT), 0, 32)

# Заголовок окна игрового поля:
pygame.display.set_caption("Змейка")

# Настройка времени:
clock = pygame.time.Clock()


# Тут опишите все классы игры.
class GameObject:
    """Класс всех объектов"""

    def __init__(self) -> None:
        self.position = ((SCREEN_WIDTH // 2), (SCREEN_HEIGHT // 2))
        self.body_color = BOARD_BACKGROUND_COLOR

    def draw(self):
        """Метод отрисовки объектов"""


class Apple(GameObject):
    """Класс Яблока"""

    def __init__(self):
        super().__init__()
        self.body_color = APPLE_COLOR
        # Метод создания яблока в произвольном месте окна (77).
        self.randomize_position()

    def draw(self):
        """Отрисовка яблока"""
        rect = pygame.Rect(self.position, (GRID_SIZE, GRID_SIZE))
        pygame.draw.rect(screen, self.body_color, rect)
        pygame.draw.rect(screen, BORDER_COLOR, rect, 1)

    def randomize_position(self):
        """Метод создания яблока в произвольном месте окна"""
        self.position = (
            randrange(0, SCREEN_WIDTH, GRID_SIZE),
            randrange(0, SCREEN_HEIGHT, GRID_SIZE),
        )


class Snake(GameObject):
    """Класс змейки"""

    def __init__(self):
        super().__init__()
        self.body_color = SNAKE_COLOR
        self.length = 1
        self.positions = [(self.position)]
        self.direction = RIGHT
        self.next_direction = None
        self.last = None
        # Экземпляр класса Apple() для реализации взаимодействия со Snake()
        self.apple = Apple()

    def draw(self):
        """Отрисовка змейки"""
        # Отрисовка головы змейки.
        for position in self.positions[:-1]:
            rect = (pygame.Rect(position, (GRID_SIZE, GRID_SIZE)))
            pygame.draw.rect(screen, self.body_color, rect)
            pygame.draw.rect(screen, BORDER_COLOR, rect, 1)

        # Отрисовка головы змейки
        head_rect = pygame.Rect(self.positions[0], (GRID_SIZE, GRID_SIZE))
        pygame.draw.rect(screen, self.body_color, head_rect)
        pygame.draw.rect(screen, BORDER_COLOR, head_rect, 1)

        # Затирание последнего сегмента
        if self.last:
            last_rect = pygame.Rect(self.last, (GRID_SIZE, GRID_SIZE))
            pygame.draw.rect(screen, BOARD_BACKGROUND_COLOR, last_rect)

    def move(self):
        """Логика движения змейки"""
        # Метод передача направления смены координат при нажатии клавиши (130).
        self.get_direction()
        # Метод проверки столкновения с границами и телепортация (153).
        self.collide_with_walls()
        # Метод действия змейки с яблоком (167).
        self.eating_apple()
        # Отслеживание головы змейки (175)
        self.get_head_position()
        # Метод обновления направления после нажатия на кнопку (177).
        self.update_direction()
        # Метод проверки столкновения с собой (188)
        self.collide_with_self()

    def get_direction(self):
        """Метод передача направления смены координат при нажатии клавиши"""
        # Получение координат головы в текущий момент
        snake_head_x, snake_head_y = self.get_head_position()

        if self.direction == RIGHT:
            snake_head_x += GRID_SIZE
        elif self.direction == LEFT:
            snake_head_x -= GRID_SIZE
        elif self.direction == UP:
            snake_head_y -= GRID_SIZE
        elif self.direction == DOWN:
            snake_head_y += GRID_SIZE

        # Передача координат новой головы в следующий момент.
        new_head_position = (snake_head_x, snake_head_y)
        # Вставка нового значения головы в следующий момент.
        self.positions.insert(0, new_head_position)
        # Передача координат хвоста.
        self.last = self.positions[-1]
        # Стирание хвоста.
        if len(self.positions) > self.length:
            self.positions.pop()

    def collide_with_walls(self):
        """Метод проверки столкновения с границами и телепортация"""
        if self.positions[0][0] < 0:  # Без равенства для достижения границы
            self.positions[0] = (SCREEN_WIDTH - GRID_SIZE,
                                 self.positions[0][1])
        elif self.positions[0][0] >= SCREEN_WIDTH:  # Ушла за правую границу
            self.positions[0] = (0, self.positions[0][1])
        # Ушла за верхнюю границу
        if self.positions[0][1] < 0:  # Без равенства для достижения границы
            self.positions[0] = (self.positions[0][0],
                                 SCREEN_HEIGHT - GRID_SIZE)
        elif self.positions[0][1] >= SCREEN_HEIGHT:  # Ушла за нижнюю границу
            self.positions[0] = (self.positions[0][0], 0)

    def eating_apple(self):
        """Метод действия змейки с яблоком"""
        if self.positions[0] == self.apple.position:  # Сравниваем с яблоком
            self.length += 1
            self.apple.randomize_position()

    def get_head_position(self):
        """Отслеживание головы змейки"""
        return self.positions[0]

    def update_direction(self):
        """Метод обновления направления после нажатия на кнопку"""
        if self.next_direction:
            self.direction = self.next_direction
            self.next_direction = None

    def collide_with_self(self):
        """Метод проверки столкновения с собой"""
        if self.positions[0] in self.positions[1:]:
            self.reset()

    def reset(self):
        """Логика сброса игры"""
        screen.fill(BOARD_BACKGROUND_COLOR)
        self.length = 1
        self.positions = [(self.position)]
        self.direction = RIGHT
        self.next_direction = None
        self.last = None


def handle_keys(game_object):
    """Функция обработки действий пользователя"""
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            raise SystemExit
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_UP and game_object.direction != DOWN:
                game_object.next_direction = UP
            elif event.key == pygame.K_DOWN and game_object.direction != UP:
                game_object.next_direction = DOWN
            elif event.key == pygame.K_LEFT and game_object.direction != RIGHT:
                game_object.next_direction = LEFT
            elif event.key == pygame.K_RIGHT and game_object.direction != LEFT:
                game_object.next_direction = RIGHT


def main():
    """Инициализация PyGame"""
    pygame.init()
    # Тут нужно создать экземпляры классов.
    apple = Apple()
    snake_player = Snake()

    while True:
        clock.tick(SPEED)
        handle_keys(snake_player)
        apple.draw()
        snake_player.draw()
        snake_player.move()
        snake_player.eating_apple()
        pygame.display.update()

        # Тут дописать основную логику игры.
        if snake_player.positions[0] == apple.position:
            snake_player.length += 1
            apple.randomize_position()


if __name__ == "__main__":
    main()
