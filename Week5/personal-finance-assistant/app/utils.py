import logging
from pathlib import Path


LOG_PATH = Path(__file__).parent.parent / "logs" / "app.log"


def setup_logging():
    LOG_PATH.parent.mkdir(exist_ok=True)

    logging.basicConfig(
        filename=LOG_PATH,
        level=logging.INFO,
        format="%(asctime)s | %(levelname)s | %(name)s | %(message)s"
    )