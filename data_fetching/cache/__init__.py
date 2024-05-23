import pandas as pd
import os
from pathlib import Path


PATH = Path(__file__).parents[0]


def save_data_to_csv(data: dict[str:str], file_name: str):
    file_name = PATH / file_name
    if os.path.isfile(file_name):
        return None
    # Force every value to be a string
    data = {k: str(v) for k, v in data.items()}
    column_names = list(data.keys())
    values = list(data.values())
    df = pd.DataFrame([values], columns=column_names)
    print(f"Saving data to {file_name}")
    df.to_csv(file_name, index=False)
