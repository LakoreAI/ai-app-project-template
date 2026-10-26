import logging

import colorlog

_FORMAT = "%(log_color)s%(asctime)s %(levelname)-8s%(reset)s %(cyan)s%(name)s%(reset)s: %(message)s"


def get_logger(name: str, level: int = logging.INFO) -> logging.Logger:
    """Return a logger that prints colored records to stderr (configured once per name)."""
    logger = logging.getLogger(name)
    if not logger.handlers:
        handler = colorlog.StreamHandler()
        handler.setFormatter(colorlog.ColoredFormatter(_FORMAT, datefmt="%H:%M:%S"))
        logger.addHandler(handler)
        logger.setLevel(level)
        logger.propagate = False
    return logger
