from datetime import datetime

from sqlalchemy import JSON, Integer, Boolean, Column, DateTime, String

from outage_detector.entities.base import BaseEntity


class Event(BaseEntity):
    __tablename__ = "outage_monitor_events"

    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    started_at = Column(DateTime, default=datetime.utcnow)
    ended_at = Column(DateTime)
    resource = Column(String(60))
    status = Column(String(60))
    notified = Column(Boolean, default=False)
    context = Column(JSON, nullable=True)
