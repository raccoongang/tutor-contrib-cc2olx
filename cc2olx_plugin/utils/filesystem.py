from pathlib import Path


def create_directory_if_not_exists(directory_path: Path) -> None:
    """
    Create the directory and its ancestors if they do not exist.
    """
    directory_path.resolve().mkdir(parents=True, exist_ok=True)
