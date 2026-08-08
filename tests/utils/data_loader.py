import json
from pathlib import Path


DATA_DIR = Path(__file__).resolve().parent.parent / "data"


def load_test_data(filename: str):
    file_path = DATA_DIR / filename

    with file_path.open("r", encoding="utf-8") as file:
        return json.load(file)