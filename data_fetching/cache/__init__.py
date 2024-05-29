import pandas as pd
import os
from pathlib import Path


PATH = Path(__file__).parents[0]


def save_data_to_csv(data: list[dict], file_name: str):
    file_name = PATH / file_name
    if os.path.isfile(file_name):
        return None

    df = pd.DataFrame(data)
    print(f"Saving data to {file_name}")
    df.to_csv(file_name, index=False)
