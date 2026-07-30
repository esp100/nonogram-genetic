import io
import pandas as pd
from project.domain.csv_port import CSVPort

class CSVAdapter(CSVPort):
    def read_stream(self, stream) -> list:
        df = pd.read_csv(stream, header=None)
        return df.values.tolist()

    def write_stream(self, grid: list[list[int]]) -> io.BytesIO:
        df = pd.DataFrame(grid)
        csv_buffer = io.BytesIO()
        df.to_csv(csv_buffer, index=False, header=False)

        csv_buffer.seek(0)
        return csv_buffer
