from pathlib import Path


def ensure_directory_exists(directory_path: Path) -> None:
    """
    Create the directory and its ancestors if they do not exist.
    """
    directory_path.resolve().mkdir(parents=True, exist_ok=True)
