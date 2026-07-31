from abc import ABC, abstractmethod
from .entities import Nonogram
from project.domain.csv_port import CSVPort
from project.domain.nonogram_solver_port import NonogramSolverPort

class NonogramService(ABC):
    @abstractmethod
    def create_nonogram(self, rows, cols, row_hints=[], col_hints=[], grid=None):
        pass

    @abstractmethod
    def solve_nonogram(self, nonogram: Nonogram):
        pass

    @abstractmethod
    def get_nonogram(self, nonogram: Nonogram):
        pass

    @abstractmethod
    def generate_file(self, grid):
        pass


class NonogramServiceImpl(NonogramService):

    def __init__(self, csv_adapter: CSVPort = None, nonogram_solver_adapter: NonogramSolverPort = None ):
        self.csv_adapter = csv_adapter
        self.nonogram_solver_adapter = nonogram_solver_adapter

    def create_nonogram(self, rows, cols, row_hints=[], col_hints=[], grid=None):
        if grid is None:
            grid = [[0 for _ in range(cols)] for _ in range(rows)]
        if row_hints==[] or col_hints==[]:
            row_hints, col_hints = self.nonogram_solver_adapter.generate_hints(grid=grid)
        return Nonogram(grid=grid, row_hints=row_hints, col_hints=col_hints)


    def solve_nonogram(self, nonogram: Nonogram):
        return self.nonogram_solver_adapter.solve(nonogram)


    def get_nonogram(self, nonogram: Nonogram):
        return nonogram.get_nonogram()

    def generate_file(self, grid: list[list[int]]):
        nonogram = Nonogram(grid=grid)
        return self.csv_adapter.write_stream(nonogram.grid)
