from dataclasses import dataclass
from pathlib import Path


@dataclass
class Config:
    PROJECT_DIR: Path
    MOVIES_CSV_FILE: Path


PROJECT_DIR = Path(__file__).parent.parent
MOVIES_CSV_FILE = PROJECT_DIR / 'movie_list.csv'

config = Config(PROJECT_DIR, MOVIES_CSV_FILE)
