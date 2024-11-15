# -*- coding: utf-8 -*-
"""
Created on: 14.11.2024

@author: dmitry
"""


from random import choice, randrange

import pygame as pg

# Константы для размеров поля и сетки:
SCREEN_WIDTH, SCREEN_HEIGHT = 640, 480
GRID_SIZE = 20
GRID_WIDTH = SCREEN_WIDTH // GRID_SIZE
GRID_HEIGHT = SCREEN_HEIGHT // GRID_SIZE
SCREEN_CENTER = ((SCREEN_WIDTH // 2), (SCREEN_HEIGHT // 2))

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

# Словарь направлений и нажатий.
CONTROLS = {
    (RIGHT, pg.K_UP): UP,  # Змейка вправо, можно вверх
    (LEFT, pg.K_UP): UP,  # Змейка влево, можно вверх
    (UP, pg.K_LEFT): LEFT,  # Змейка вверх, можно влево
    (DOWN, pg.K_LEFT): LEFT,  # Змейка вниз, можно влево
    (UP, pg.K_RIGHT): RIGHT,  # Змейка вверх, можно вправо
    (DOWN, pg.K_RIGHT): RIGHT,  # Змейка вниз, можно вправо
    (LEFT, pg.K_DOWN): DOWN,  # Змейка влево, можно вниз
    (RIGHT, pg.K_DOWN): DOWN,  # Змейка вправо, можно вниз
}

# Настройка игрового окна:
screen = pg.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT), 0, 32)

# Заголовок окна игрового поля:
pg.display.set_caption("Змейка")

# Настройка времени:
clock = pg.time.Clock()


class GameObject:
    """Класс всех объектов"""

    def __init__(
            self,
            position=SCREEN_CENTER,
            body_color=BOARD_BACKGROUND_COLOR,
    ) -> None:
        self.position = position
        self.body_color = body_color

    def draw_block(
            self,
            position,
            color=None,
            border_color=BORDER_COLOR,
    ) -> None:
        """Метод отрисовки одного блока"""
        color = color or self.body_color
        # Отрисовка через контур и заливку, имеющие общие координаты.
        rect_line = pg.Rect(position, (GRID_SIZE, GRID_SIZE))
        pg.draw.rect(screen, color, rect_line)  # Контур.
        pg.draw.rect(screen, border_color, rect_line, 1)  # Заливка.

    def draw(self) -> None:
        """Метод отрисовки объектов"""
        raise NotImplementedError(
            "Метод draw должен быть реализован в дочерних классах."
        )


class Apple(GameObject):
    """Класс Яблока"""

    def __init__(  # Pylint: Dangereous default value [] as an argument.
        self, position=SCREEN_CENTER, body_color=APPLE_COLOR, filled_cells=[]
    ) -> None:
        super().__init__(position, body_color)
        # Метод создания яблока в произвольном месте окна (77).
        self.randomize_position(filled_cells)

    def draw(self):
        """Отрисовка яблока"""
        self.draw_block(self.position, self.body_color)

    def randomize_position(self, filled_cells):
        """Метод создания яблока в произвольном месте окна"""
        # Значение filled_cells запоминается ровно до конца исполнения метода.
        # При каждом вызове метода предаётся аргумент для данного параметра.

        while True:
            self.position = (
                randrange(0, SCREEN_WIDTH, GRID_SIZE),
                randrange(0, SCREEN_HEIGHT, GRID_SIZE),
            )
            if self.position not in filled_cells:
                break


class Snake(GameObject):
    """Класс змейки"""

    directions = [UP, DOWN, LEFT, RIGHT]

    def __init__(self, position=SCREEN_CENTER, body_color=SNAKE_COLOR) -> None:
        super().__init__(position, body_color)
        self.reset()
        self.direction = RIGHT
        self.last = None

    def draw(self):
        """Отрисовка змейки"""
        self.draw_block(self.get_head_position(), self.body_color)

        # Затирание последнего сегмента
        if self.last:
            self.draw_block(
                self.last,
                color=BOARD_BACKGROUND_COLOR,
                border_color=BOARD_BACKGROUND_COLOR,
            )

    def move(self):
        """Логика движения змейки"""
        # Отслеживание головы змейки (158)
        self.get_head_position()
        # Метод обновления направления после нажатия на кнопку (162).

        snake_head_x, snake_head_y = self.get_head_position()
        # Сдвиги по осям X и Y для каждого направления
        # Обновляем координаты головы змейки через self.direction
        snake_head_x += (self.direction[0] * GRID_SIZE)
        snake_head_y += (self.direction[1] * GRID_SIZE)

        # Применяем обёртку по экрану (модуль)
        snake_head_x %= SCREEN_WIDTH
        snake_head_y %= SCREEN_HEIGHT

        # Передача координат новой головы в следующий момент.
        new_head_position = (snake_head_x, snake_head_y)
        # Вставка нового значения головы в следующий момент.
        self.positions.insert(0, new_head_position)
        # Передача координат хвоста.
        self.last = self.positions[-1]
        # Стирание хвоста.
        self.last = self.positions.pop()

    def get_head_position(self):
        """Отслеживание головы змейки"""
        return self.positions[0]

    def update_direction(self, snake_direction):
        """Метод обновления направления после нажатия на кнопку"""
        self.direction = snake_direction

    def grow(self):
        """Метод отращивания хвоста в случае съеденного яблока"""
        if self.last:
            self.positions.append(self.last)
            self.last = None

    def reset(self):
        """Логика сброса позиции змейки"""
        self.length = 1
        self.positions = [self.position]
        self.direction = choice(self.directions)
        self.last = None


def handle_keys(game_obj):
    """Функция обработки действий пользователя"""
    for event in pg.event.get():

        if event.type == pg.QUIT:
            pg.quit()
            raise SystemExit
        elif event.type == pg.KEYDOWN:
            if event.key == pg.K_ESCAPE:
                pg.quit()
                raise SystemExit
            if event.type == pg.KEYDOWN:
                # Создание нового направления.
                # Для направления, кнопки, нового напрвления в значениях
                snake_direction = CONTROLS.get(
                    (game_obj.direction, event.key), game_obj.direction)
                game_obj.update_direction(snake_direction)


def main():
    """Инициализация pygame"""
    pg.init()
    snake_player = Snake()
    apple = Apple(filled_cells=snake_player.positions)

    while True:
        clock.tick(SPEED)
        handle_keys(snake_player)
        snake_player.move()
        snake_player.draw()

        if snake_player.get_head_position() in snake_player.positions[1:]:
            screen.fill(BOARD_BACKGROUND_COLOR)
            snake_player.reset()
            apple.randomize_position(filled_cells=snake_player.positions)
        elif snake_player.get_head_position() == apple.position:
            snake_player.grow()
            apple.randomize_position(filled_cells=snake_player.positions)

        apple.draw()
        pg.display.update()


if __name__ == "__main__":
    main()
