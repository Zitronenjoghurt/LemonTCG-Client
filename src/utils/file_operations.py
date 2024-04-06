import os
from pathlib import Path


ROOT_DIR = str(Path(__file__).parent.parent.parent)

def construct_path(relative_path: str) -> str:
    path_parts = relative_path.split("/")
    absolute_path = os.path.join(ROOT_DIR, *path_parts)
    return absolute_path