import logging


def init_logger(log_level: str = logging.DEBUG) -> None:
    logging.basicConfig(
        format="[%(levelname)s] - %(asctime)s - %(name)s::%(funcName)s() - %(message)s",
        level=log_level.upper(),
    )
