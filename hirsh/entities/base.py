from enum import Enum

from sqlalchemy.ext.declarative import declarative_base


class StrEnum(str, Enum):
    def __str__(self):
        return str(self.value)


class Resources(StrEnum):
    DAEMON = "daemon"
    NETWORK = "network"


class Setups(StrEnum):
    """
    Supported IoT Setups
    """
    BASIC = "basic"


BaseEntity = declarative_base()
