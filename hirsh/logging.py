import logging


def init_logger(log_level: str = "DEBUG", third_party_level: str = "WARNING") -> None:
    log_level = log_level.upper()
    third_party_level = third_party_level.upper()

    logging.basicConfig(
        format="[%(levelname)s] - %(asctime)s - %(name)s::%(funcName)s() - %(message)s",
        level=log_level,
    )

    logging.getLogger("aiosqlite").setLevel(third_party_level)
    logging.getLogger("sqlalchemy").setLevel(third_party_level)
    logging.getLogger("sqlalchemy.engine").setLevel(third_party_level)
    logging.getLogger("aiogram").setLevel(third_party_level)
