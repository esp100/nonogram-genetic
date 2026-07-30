from abc import ABC, abstractmethod
from .entities import Nonogram
from project.domain.csv_port import CSVPort
#TODO: Solving algorithm for Nonogram

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

    def __init__(self, csv_adapter: CSVPort = None):
        self.csv_adapter = csv_adapter

    def create_nonogram(self, rows, cols, row_hints=[], col_hints=[], grid=None):
        if grid is None:
            grid = [[0 for _ in range(cols)] for _ in range(rows)]
        return Nonogram(grid=grid, row_hints=row_hints, col_hints=col_hints)


    def solve_nonogram(self, nonogram: Nonogram):
        # TODO Solving 
        #Also return time, generations, etc. 
        return nonogram

    def get_nonogram(self, nonogram: Nonogram):
        return nonogram.get_nonogram()

    def generate_file(self, grid: list[list[int]]):
        nonogram = Nonogram(grid=grid)
        return self.csv_adapter.write_stream(nonogram.grid)
