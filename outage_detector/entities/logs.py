from datetime import datetime

from sqlalchemy import JSON, Integer, Boolean, Column, DateTime, String

from outage_detector.entities.base import BaseEntity, StrEnum


class LogStatus(StrEnum):
    UP = "up"
    DOWN = "down"


class Log(BaseEntity):
    __tablename__ = "outage_monitor_logs"

    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    created_at = Column(DateTime, default=datetime.utcnow)
    resource = Column(String(60))
    status = Column(String(60))
    processed = Column(Boolean, default=False)
    context = Column(JSON, nullable=True)
