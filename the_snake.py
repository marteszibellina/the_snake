# -*- coding: utf-8 -*-
"""
Author: @marteszibelina
Created on: 29.04.2025
Project: The Snake Game
File: Game
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

    def __init__(
        self, position=SCREEN_CENTER, body_color=APPLE_COLOR, filled_cells=[]
    ) -> None:
        super().__init__(position, body_color)
        self.randomize_position(filled_cells)

    def draw(self):
        """Отрисовка яблока"""
        self.draw_block(self.position, self.body_color)

    def randomize_position(self, filled_cells):
        """Метод создания яблока в произвольном месте окна"""
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
        self.get_head_position()

        snake_head_x, snake_head_y = self.get_head_position()
        snake_head_x += (self.direction[0] * GRID_SIZE)
        snake_head_y += (self.direction[1] * GRID_SIZE)

        snake_head_x %= SCREEN_WIDTH
        snake_head_y %= SCREEN_HEIGHT

        new_head_position = (snake_head_x, snake_head_y)
        self.positions.insert(0, new_head_position)
        self.last = self.positions[-1]
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
        screen.fill(BOARD_BACKGROUND_COLOR)
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
                snake_direction = CONTROLS.get(
                    (game_obj.direction, event.key), game_obj.direction)
                game_obj.update_direction(snake_direction)


def draw_text(text, font, color, x, y, border_color=None):
    """Функция для отрисовки текста с рамкой"""
    label = font.render(text, True, color)
    label_rect = label.get_rect(topleft=(x, y))
    
    if border_color:
        # Рисуем рамку
        border_rect = label_rect.inflate(10, 10)
        pg.draw.rect(screen, border_color, border_rect)
    screen.blit(label, (x, y))


def main():
    """Основная логика игры"""
    pg.init()

    global screen
    screen = pg.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
    pg.display.set_caption("The Snake Game")

    clock = pg.time.Clock()

    font = pg.font.Font(None, 36)
    game_state = "MENU"

    score = 0
    snake_player = Snake()
    apple = Apple(filled_cells=snake_player.positions)

    while True:
        clock.tick(SPEED)

        if game_state == "MENU":
            screen.fill(BOARD_BACKGROUND_COLOR)
            draw_text("The Snake Game", font, (255, 255, 255), SCREEN_WIDTH // 3, SCREEN_HEIGHT // 4)
            draw_text("Press SPACE to START", font, (255, 255, 255), SCREEN_WIDTH // 3.5, SCREEN_HEIGHT // 2.5)
            draw_text("Press ESC to QUIT", font, (255, 255, 255), SCREEN_WIDTH // 3, SCREEN_HEIGHT // 2)

        elif game_state == "RUNNING":
            handle_keys(snake_player)
            snake_player.move()

            if snake_player.get_head_position() in snake_player.positions[1:]:
                game_state = "GAME_OVER"
                score = 0
            elif snake_player.get_head_position() == apple.position:
                snake_player.grow()
                apple.randomize_position(filled_cells=snake_player.positions)
                score += 1

            snake_player.draw()
            apple.draw()
            pg.draw.rect(screen, BOARD_BACKGROUND_COLOR, (10, 10, 95, 20))
            draw_text(f"Score: {score}", font, (255, 255, 255), 10, 10, BORDER_COLOR)

        elif game_state == "GAME_OVER":
            screen.fill(BOARD_BACKGROUND_COLOR)
            draw_text("Game Over!", font, (255, 0, 0), SCREEN_WIDTH // 3, SCREEN_HEIGHT // 4)
            draw_text("Press Space to START", font, (255, 255, 255), SCREEN_WIDTH // 3.5, SCREEN_HEIGHT // 2.5)
            draw_text("Press ESC to QUIT", font, (255, 255, 255), SCREEN_WIDTH // 3.5, SCREEN_HEIGHT // 2)

        pg.display.update()

        for event in pg.event.get():
            if event.type == pg.QUIT:
                pg.quit()
                raise SystemExit
            if event.type == pg.KEYDOWN:
                if event.key == pg.K_ESCAPE:
                    pg.quit()
                    raise SystemExit
                if game_state == "MENU" and event.key == pg.K_SPACE:
                    game_state = "RUNNING"
                    screen.fill(BOARD_BACKGROUND_COLOR)
                elif game_state == "GAME_OVER" and event.key == pg.K_SPACE:
                    game_state = "RUNNING"
                    snake_player.reset()
                    apple.randomize_position(filled_cells=snake_player.positions)


if __name__ == "__main__":
    main()
