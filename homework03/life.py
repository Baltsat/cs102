import copy
import pathlib
import random
import typing as tp

import pygame
from pygame.locals import *

Cell = tp.Tuple[int, int]
Cells = tp.List[int]
Grid = tp.List[Cells]


class GameOfLife:
    def __init__(
        self,
        size: tp.Tuple[int, int] = (24, 80),
        randomize: bool = True,
        max_generations: tp.Optional[float] = float("inf"),
    ) -> None:
        # Размер клеточного поля
        self.rows, self.cols = size
        # Предыдущее поколение клеток
        self.prev_generation = self.create_grid()
        # Текущее поколение клеток
        self.curr_generation = self.create_grid(randomize=randomize)
        # Максимальное число поколений
        self.max_generations = max_generations
        # Текущее число поколений
        self.generations = 1

    def create_grid(self, randomize: bool = False) -> Grid:
        # Copy from previous assignment
        return [
            [random.choice([0, 1]) if randomize else 0 for _ in range(self.cols)]
            for _ in range(self.rows)
        ]

    def get_neighbours(self, cell: Cell) -> Cells:
        # Copy from previous assignment
        neighbours = []

        for i in range(-1, 2):
            for j in range(-1, 2):
                h = cell[0] + i
                w = cell[1] + j

                if i == 0 and j == 0:
                    continue

                if 0 <= w < self.cols and 0 <= h < self.rows:
                    neighbours.append(self.curr_generation[h][w])

        return neighbours

    def get_next_generation(self) -> Grid:
        # Copy from previous assignment
        new_grid = copy.deepcopy(self.curr_generation)

        for h in range(self.rows):
            for w in range(self.cols):
                neighbours = self.get_neighbours((h, w))
                alive_neighbours = sum(neighbours)

                if alive_neighbours != 2 and alive_neighbours != 3:
                    new_grid[h][w] = 0

                elif alive_neighbours == 3:
                    new_grid[h][w] = 1

        return new_grid

    def step(self) -> None:
        """
        Выполнить один шаг игры.
        """
        self.generations += 1
        self.prev_generation, self.curr_generation = (
            self.curr_generation,
            self.get_next_generation(),
        )

    @property
    def is_max_generations_exceeded(self) -> bool:
        """
        Не превысило ли текущее число поколений максимально допустимое.
        """
        for row in range(self.rows):
            for col in range(self.cols):
                if self.prev_generation[row][col] != self.curr_generation[row][col]:
                    return True
        return False

    @property
    def is_changing(self) -> bool:
        """
        Изменилось ли состояние клеток с предыдущего шага.
        """
        for row in range(self.rows):
            for col in range(self.cols):
                if self.prev_generation[row][col] != self.curr_generation[row][col]:
                    return True
        return False

    @staticmethod
    def from_file(filename: pathlib.Path) -> "GameOfLife":
        """
        Прочитать состояние клеток из указанного файла.
        """
        with filename.open() as file:
            grid = [list(map(int, col.strip())) for col in file.readlines()]

        size = len(grid), len(grid[0])

        new_game = GameOfLife(size, randomize=False)
        new_game.curr_generation = grid
        return new_game

    def save(self, filename: pathlib.Path) -> None:
        """
        Сохранить текущее состояние клеток в указанный файл.
        """
        grid_txt = "\n".join(["".join(map(str, col)) for col in self.curr_generation])

        with filename.open(mode="w") as file:
            file.write(grid_txt)
