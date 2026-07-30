from abc import ABC, abstractmethod

class CSVPort(ABC):
    @abstractmethod
    def write_stream(self, grid: list[list[int]]) -> bytes:
        pass

    @abstractmethod
    def read_stream(self, stream) -> list[list[int]]:
        pass