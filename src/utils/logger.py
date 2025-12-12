import logging
import os

def setup_logging(log_level: str = "INFO"):
    level = getattr(logging, log_level.upper(), logging.INFO)
    logging.basicConfig(
        level=level,
        format="%(asctime)s | %(levelname)s | %(name)s | %(message)s",
    )
    # optional: file handler
    logdir = "logs"
    if not os.path.exists(logdir):
        os.makedirs(logdir)
