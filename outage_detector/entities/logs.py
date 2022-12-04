
from enum import Enum

from sqlalchemy import JSON, BigInteger, Boolean, Column, DateTime, String

from outage_detector.repositories import BaseEntity


class LogStatus(str, Enum):
    UP = "up"
    DOWN = "down"


class Log(BaseEntity):
    __tablename__ = "outage_monitor_logs"

    id = Column(BigInteger, primary_key=True, index=True)
    created_at = Column(DateTime)
    resource = Column(String(60))
    status = Column(String(60))
    processed = Column(Boolean, default=False)
    context = Column(JSON, nullable=True)
