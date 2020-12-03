import copy
import random
import typing as tp

import pygame
from pygame.locals import *

Cell = tp.Tuple[int, int]
Cells = tp.List[int]
Grid = tp.List[Cells]


class GameOfLife:
    def __init__(
        self, width: int = 640, height: int = 480, cell_size: int = 20, speed: int = 10
    ) -> None:
        self.width = width
        self.height = height
        self.cell_size = cell_size

        # Устанавливаем размер окна
        self.screen_size = width, height
        # Создание нового окна
        self.screen = pygame.display.set_mode(self.screen_size)

        # Вычисляем количество ячеек по вертикали и горизонтали
        self.cell_width = self.width // self.cell_size
        self.cell_height = self.height // self.cell_size

        # Скорость протекания игры
        self.speed = speed

    def draw_lines(self) -> None:
        """ Отрисовать сетку """
        for x in range(0, self.width, self.cell_size):
            pygame.draw.line(self.screen, pygame.Color("black"), (x, 0), (x, self.height))
        for y in range(0, self.height, self.cell_size):
            pygame.draw.line(self.screen, pygame.Color("black"), (0, y), (self.width, y))

    def run(self) -> None:
        """ Запустить игру """
        pygame.init()
        clock = pygame.time.Clock()
        pygame.display.set_caption("Game of Life")
        self.screen.fill(pygame.Color("white"))

        # Создание списка клеток
        # Создание списка клеток
        self.grid = self.create_grid(randomize=True)

        pause = True

        running = True
        while running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False

                elif event.type == pygame.MOUSEBUTTONUP and event.button == 1:
                    w, h = event.pos[0] // self.cell_size, event.pos[1] // self.cell_size
                    self.grid[h][w] = 0 if self.grid[h][w] else 1

                elif event.type == pygame.KEYUP and event.key == pygame.K_SPACE:
                    pause = not pause

                elif event.type == pygame.KEYUP and event.key == pygame.K_ESCAPE:
                    running = False
            self.draw_lines()

            # Отрисовка списка клеток
            self.draw_grid()
            # Выполнение одного шага игры (обновление состояния ячеек)
            if not pause:
                self.grid = self.get_next_generation()

            pygame.display.flip()
            clock.tick(self.speed)
        pygame.quit()

    def create_grid(self, randomize: bool = False) -> Grid:
        """
        Создание списка клеток.

        Клетка считается живой, если ее значение равно 1, в противном случае клетка
        считается мертвой, то есть, ее значение равно 0.

        Parameters
        ----------
        randomize : bool
            Если значение истина, то создается матрица, где каждая клетка может
            быть равновероятно живой или мертвой, иначе все клетки создаются мертвыми.

        Returns
        ----------
        out : Grid
            Матрица клеток размером `cell_height` х `cell_width`.
        """
        return [
            [random.choice([0, 1]) if randomize else 0 for _ in range(self.cell_width)]
            for _ in range(self.cell_height)
        ]

    def draw_grid(self) -> None:
        """
        Отрисовка списка клеток с закрашиванием их в соответствующе цвета.
        """
        white = pygame.Color("white")
        green = pygame.Color("green")

        for h in range(self.cell_height):
            for w in range(self.cell_width):
                y = h * self.cell_size
                x = w * self.cell_size

                color = white if self.grid[h][w] == 0 else green
                pygame.draw.rect(
                    self.screen, color, [x + 1, y + 1, self.cell_size - 1, self.cell_size - 1]
                )

    def get_neighbours(self, cell: Cell) -> Cells:
        """
        Вернуть список соседних клеток для клетки `cell`.

        Соседними считаются клетки по горизонтали, вертикали и диагоналям,
        то есть, во всех направлениях.

        Parameters
        ----------
        cell : Cell
            Клетка, для которой необходимо получить список соседей. Клетка
            представлена кортежем, содержащим ее координаты на игровом поле.

        Returns
        ----------
        out : Cells
            Список соседних клеток.
        """
        neighbours = []

        for i in range(-1, 2):
            for j in range(-1, 2):
                h = cell[0] + i
                w = cell[1] + j

                if i == 0 and j == 0:
                    continue

                if 0 <= w < self.cell_width and 0 <= h < self.cell_height:
                    neighbours.append(self.grid[h][w])

        return neighbours

    def get_next_generation(self) -> Grid:
        """
        Получить следующее поколение клеток.

        Returns
        ----------
        out : Grid
            Новое поколение клеток.
        """
        new_grid = copy.deepcopy(self.grid)

        for h in range(self.cell_height):
            for w in range(self.cell_width):
                neighbours = self.get_neighbours((h, w))
                alive_neighbours = sum(neighbours)

                if alive_neighbours != 2 and alive_neighbours != 3:
                    new_grid[h][w] = 0

                elif alive_neighbours == 3:
                    new_grid[h][w] = 1

        return new_grid


if __name__ == "__main__":
    game = GameOfLife(320, 240, 20)
    game.run()
