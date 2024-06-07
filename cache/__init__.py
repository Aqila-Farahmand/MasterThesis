import pandas as pd
import os
from pathlib import Path

PATH = Path(__file__).parents[0]

# to do add the logic to check if the file exist in the cache skip fetching it again


def save_data_to_csv(data: list[dict], file_name: str):
    file_path = PATH / file_name
    if os.path.isfile(file_path):
        return None
    df = pd.DataFrame(data)
    print(f"Saving data to {file_path}")
    df.to_csv(file_path, index=False)
