class Nonogram:
    def __init__(self, rows, cols, row_hints=[], col_hints=[]):
        self.rows = rows
        self.cols = cols
        self.row_hints = row_hints
        self.col_hints = col_hints
        self.grid = [[0 for _ in range(cols)] for _ in range(rows)]

    def set_grid(self, grid):
        self.grid = grid

    def set_hints(self, row_hints, col_hints):
        self.row_hints = row_hints
        self.col_hints = col_hints

    def get_solver(self):
        return {
            "rows": self.rows,
            "cols": self.cols,
            "row_hints": self.row_hints,
            "col_hints": self.col_hints
        }

    def get_nonogram(self):
        return {
            "rows": self.rows,
            "cols": self.cols,
            "row_hints": self.row_hints,
            "col_hints": self.col_hints,
            "grid": self.grid
        }