from io import StringIO
import pandas as pd

class CSVArticleLoader:
    def __init__(self, file):
        self.file = file

    async def parse(self):
        content = await self.file.read()
        csv_data = content.decode("utf-8")
        df = pd.read_csv(StringIO(csv_data))
        return df