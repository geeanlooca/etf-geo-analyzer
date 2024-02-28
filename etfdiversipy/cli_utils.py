import argparse
import os


def dir_path(path: str) -> str:
    """Verify that the path is a directory. If not, raise an error."""
    if os.path.isdir(path):
        return path
    else:
        raise argparse.ArgumentTypeError(f"{path} is not a valid path")
