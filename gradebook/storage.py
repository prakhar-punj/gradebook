"""Read and write gradebook data.""" 

import json
import logging
from pathlib import Path

DEFAULT_PATH = Path("data/gradebook.json")
LOG_PATH = Path("logs/app.log")


def get_logger():
    """Set up the log file."""
    LOG_PATH.parent.mkdir(parents=True, exist_ok=True)
    logger = logging.getLogger("gradebook")
    if not logger.handlers:
        logger.setLevel(logging.INFO)
        handler = logging.FileHandler(LOG_PATH, encoding="utf-8")
        handler.setFormatter(
            logging.Formatter("%(asctime)s %(levelname)s: %(message)s")
        )
        logger.addHandler(handler)
    return logger


def empty_data():
    """Return an empty gradebook."""
    return {"students": [], "courses": [], "enrollments": []}


def load_data(path=DEFAULT_PATH):
    """Load data from the JSON file."""
    logger = get_logger()
    file_path = Path(path)
    try:
        with file_path.open("r", encoding="utf-8") as file:
            data = json.load(file)
        for key in ("students", "courses", "enrollments"):
            if key not in data or not isinstance(data[key], list):
                raise ValueError(f"Invalid data: '{key}' must be a list.")
        logger.info("Loaded data from %s", file_path)
        return data
    except FileNotFoundError:
        logger.info("Data file not found. Returning empty data.")
        return empty_data()
    except json.JSONDecodeError as error:
        logger.error("Invalid JSON in %s: %s", file_path, error)
        raise ValueError(
            f"The file {file_path} is not valid. Please check the file."
        ) from error
    except (OSError, ValueError):
        logger.exception("Could not load data from %s", file_path)
        raise


def save_data(data, path=DEFAULT_PATH):
    """Save data to the JSON file."""
    logger = get_logger()
    file_path = Path(path)
    try:
        file_path.parent.mkdir(parents=True, exist_ok=True)
        with file_path.open("w", encoding="utf-8") as file:
            json.dump(data, file, indent=4)
            file.write("\n")
        logger.info("Saved data to %s", file_path)
    except OSError:
        logger.exception("Could not save data to %s", file_path)
        raise
