# -*- coding: utf-8 -*-
"""
Created on: 13.11.2024

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

# Настройка игрового окна:
screen = pg.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT), 0, 32)

# Заголовок окна игрового поля:
pg.display.set_caption("Змейка")

# Настройка времени:
clock = pg.time.Clock()


class GameObject:
    """Класс всех объектов"""

    def __init__(
        self, position=SCREEN_CENTER, body_color=BOARD_BACKGROUND_COLOR
    ) -> None:
        self.position = position
        self.body_color = body_color

    def draw_block(self, position, color=None) -> None:
        """Метод отрисовки одного блока"""
        if color is None:
            color = self.body_color
        # Отрисовка через контур и заливку, имеющие общие координаты.
        rect_line = pg.Rect(position[0], position[1], GRID_SIZE, GRID_SIZE)
        rect_fill = rect_line
        pg.draw.rect(screen, color, rect_fill)  # Контур.
        pg.draw.rect(screen, BORDER_COLOR, rect_line, 1)  # Заливка.

    def draw(self) -> None:
        """Метод отрисовки объектов"""
        raise NotImplementedError(
            "Метод draw должен быть реализован в дочерних классах."
        )


class Apple(GameObject):
    """Класс Яблока"""

    def __init__(
        self, position=SCREEN_CENTER, body_color=APPLE_COLOR, filled_cell=None
    ) -> None:
        super().__init__(position, body_color)
        self.body_color = body_color
        self.filled_cell = filled_cell if filled_cell is not None else []
        # Метод создания яблока в произвольном месте окна (77).
        self.randomize_position(self.filled_cell)

    def draw(self):
        """Отрисовка яблока"""
        self.draw_block(self.position, self.body_color)

    def randomize_position(self, filled_cell=None):
        """Метод создания яблока в произвольном месте окна"""
        if filled_cell is None:
            filled_cell = self.filled_cell

        while True:
            apple_position = (
                randrange(0, SCREEN_WIDTH, GRID_SIZE),
                randrange(0, SCREEN_HEIGHT, GRID_SIZE),
            )
            if apple_position not in filled_cell:
                self.position = apple_position
                break


class Snake(GameObject):
    """Класс змейки"""

    directions = [UP, DOWN, LEFT, RIGHT]

    def __init__(
        self, position=SCREEN_CENTER, body_color=SNAKE_COLOR, length=1
    ) -> None:
        super().__init__(position, body_color)
        self.body_color = SNAKE_COLOR
        self.length = length
        self.positions = [self.position]
        self.direction = choice(self.directions)
        self.last = None

    def draw(self):
        """Отрисовка змейки"""
        self.draw_block(self.positions[0], self.body_color)

        # Затирание последнего сегмента
        if self.last:
            last_rect = pg.Rect(self.last, (GRID_SIZE, GRID_SIZE))
            pg.draw.rect(screen, BOARD_BACKGROUND_COLOR, last_rect)

    def move(self):
        """Логика движения змейки"""
        # Отслеживание головы змейки (158)
        self.get_head_position()
        # Метод обновления направления после нажатия на кнопку (162).
        self.update_direction(self.direction)

        snake_head_x, snake_head_y = self.get_head_position()

        if self.direction == RIGHT:
            snake_head_x = (snake_head_x + GRID_SIZE) % SCREEN_WIDTH
        elif self.direction == LEFT:
            snake_head_x = (snake_head_x - GRID_SIZE) % SCREEN_WIDTH
        elif self.direction == UP:
            snake_head_y = (snake_head_y - GRID_SIZE) % SCREEN_HEIGHT
        elif self.direction == DOWN:
            snake_head_y = (snake_head_y + GRID_SIZE) % SCREEN_HEIGHT

        # Передача координат новой головы в следующий момент.
        new_head_position = (snake_head_x, snake_head_y)
        # Вставка нового значения головы в следующий момент.
        self.positions.insert(0, new_head_position)
        # Передача координат хвоста.
        self.last = self.positions[-1]
        # Стирание хвоста.
        self.last = self.positions.pop() if len(self.positions) > 1 else None

    def get_head_position(self):
        """Отслеживание головы змейки"""
        return self.positions[0]

    def update_direction(self, snake_direction):
        """Метод обновления направления после нажатия на кнопку"""
        if (
            (self.direction == UP and snake_direction != DOWN)
            or (self.direction == DOWN and snake_direction != UP)
            or (self.direction == LEFT and snake_direction != RIGHT)
            or (self.direction == RIGHT and snake_direction != LEFT)
        ):
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

        self.last = None


def handle_keys(game_object):
    """Функция обработки действий пользователя"""
    # Словарь направлений и нажатий, не применён.
    # controls = {
    #     (UP, pg.K_UP): UP,
    #     (DOWN, pg.K_DOWN): DOWN,
    #     (LEFT, pg.K_LEFT): LEFT,
    #     (RIGHT, pg.K_RIGHT): RIGHT,
    # }

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
                # current_direction = game_object.direction
                # key = event.key
                # if (current_direction, key) in controls:
                #     snake_direction = controls[(current_direction, key)]
                #     game_object.update_direction(snake_direction)
                if event.key == pg.K_UP and game_object.direction != DOWN:
                    game_object.update_direction(UP)
                elif event.key == pg.K_DOWN and game_object.direction != UP:
                    game_object.update_direction(DOWN)
                elif event.key == pg.K_LEFT and game_object.direction != RIGHT:
                    game_object.update_direction(LEFT)
                elif event.key == pg.K_RIGHT and game_object.direction != LEFT:
                    game_object.update_direction(RIGHT)


def main():
    """Инициализация pygame"""
    pg.init()
    snake_player = Snake()
    apple = Apple(filled_cell=snake_player.positions)

    while True:
        clock.tick(SPEED)
        handle_keys(snake_player)
        apple.draw()
        snake_player.draw()

        if snake_player.positions[0] in snake_player.positions[1:]:
            screen.fill(BOARD_BACKGROUND_COLOR)
            snake_player.reset()
            apple.randomize_position(filled_cell=snake_player.positions)
        elif snake_player.positions[0] == apple.position:
            snake_player.grow()
            apple.randomize_position(filled_cell=snake_player.positions)

        snake_player.move()
        pg.display.update()


if __name__ == "__main__":
    main()
