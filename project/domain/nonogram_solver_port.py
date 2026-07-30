from abc import ABC, abstractmethod

class NonogramSolverPort(ABC):
    @abstractmethod
    def solve(self, nonogram):
        pass

    @abstractmethod
    def generate_hints(self, grid):
        pass

    @abstractmethod
    def validate_solution(self, nonogram):
        pass

