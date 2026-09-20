import logging

logger = logging.getLogger("goal_decomposer")
if not logger.handlers:
    handler = logging.StreamHandler()
    handler.setFormatter(logging.Formatter("[%(asctime)s] %(levelname)s %(message)s"))
    logger.addHandler(handler)
    logger.setLevel(logging.INFO)


def trace(message: str, *args) -> None:
    logger.info(message, *args)
