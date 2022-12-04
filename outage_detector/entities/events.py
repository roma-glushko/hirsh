from sqlalchemy import JSON, BigInteger, Boolean, Column, DateTime, String

from outage_detector.repositories import BaseEntity


class Event(BaseEntity):
    __tablename__ = "outage_monitor_events"

    id = Column(BigInteger, primary_key=True, index=True)
    started_at = Column(DateTime)
    ended_at = Column(DateTime)
    resource = Column(String(60))
    status = Column(String(60))
    notified = Column(Boolean, default=False)
    context = Column(JSON, nullable=True)
