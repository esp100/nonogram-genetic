from abc import ABC, abstractmethod
from .entities import Nonogram
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


class NonogramServiceImpl(NonogramService):
    def create_nonogram(self, rows, cols, row_hints=[], col_hints=[], grid=None):
        return Nonogram(rows, cols, row_hints, col_hints, grid if grid is not None else [[0 for _ in range(cols)] for _ in range(rows)])

    def solve_nonogram(self, nonogram: Nonogram):
        # TODO Solving 
        return nonogram

    def get_nonogram(self, nonogram: Nonogram):
        return nonogram.get_nonogram()