from random import randint

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
pygame.display.set_caption('Змейка')

# Настройка времени:
clock = pygame.time.Clock()


class GameObject:
    def __init__(self):
        self.position = ((SCREEN_WIDTH//2), (SCREEN_HEIGHT//2))
        self.body_color = None

    def draw_cell(self, position, color=None):
        if color is None:
            color = self.body_color
        rect = pygame.Rect(position, (GRID_SIZE, GRID_SIZE))
        pygame.draw.rect(screen, color, rect)
        pygame.draw.rect(screen, BORDER_COLOR, rect, 1)

    def draw(self):
        pass


class Snake(GameObject):
    def __init__(self):
        super().__init__()
        self.reset()

    def reset(self):
        self.position = (0, 0)
        self.len = 1
        self.direction = RIGHT
        self.positions = [(0, 0)]
        self.next_direction = None
        self.last = self.positions[-1]
        self.body_color = SNAKE_COLOR

    def get_head_position(self):
        return self.positions[0]

    def update_direction(self):
        if self.next_direction:
            self.direction = self.next_direction
            self.next_direction = None

    def move(self):
        head_x, head_y = self.get_head_position()
        dir_x, dir_y = self.direction

        new_x = (head_x + dir_x * GRID_SIZE) % SCREEN_WIDTH
        new_y = (head_y + dir_y * GRID_SIZE) % SCREEN_HEIGHT
        new_head_position = (new_x, new_y)

        self.last = self.positions[-1] if self.positions else None

        self.positions.insert(0, new_head_position)
        if len(self.positions) > self.len:
            self.positions.pop()

        return new_head_position

    def draw(self):
        for position in self.positions:
            self.draw_cell(position)
        if self.last:
            last_rect = pygame.Rect(self.last, (GRID_SIZE, GRID_SIZE))
            pygame.draw.rect(screen, BOARD_BACKGROUND_COLOR, last_rect)

    def grow(self):
        self.len += 1

    def check_collision(self):
        head = self.get_head_position()
        return head in self.positions[1:]


class Apple(GameObject):
    def __init__(self, snake_positions=None):
        super().__init__()
        self.body_color = APPLE_COLOR
        if snake_positions is None:
            snake_positions = []
        self.randomize_position(snake_positions)

    def randomize_position(self, snake_positions):
        while True:
            self.position = (
                randint(0, GRID_WIDTH - 1) * GRID_SIZE,
                randint(0, GRID_HEIGHT - 1) * GRID_SIZE
            )
            if self.position not in snake_positions:
                break

    def draw(self):
        self.draw_cell(self.position)


def handle_keys(game_object):
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
    pygame.init()
    snake = Snake()
    apple = Apple(snake.positions)
    while True:
        clock.tick(SPEED)
        handle_keys(snake)
        snake.update_direction()
        head_position = snake.move()
        if snake.check_collision():
            pygame.quit()
            break
        if head_position == apple.position:
            snake.grow()
            apple.randomize_position(snake.positions)
        apple.draw()
        snake.draw()
        pygame.display.update()


if __name__ == '__main__':
    main()
