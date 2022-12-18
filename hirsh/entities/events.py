from datetime import datetime
from typing import Optional

from pydantic import BaseModel, Field
from sqlalchemy import JSON, Boolean, Column, DateTime, Integer, String

from hirsh.entities.base import BaseEntity, Resources, StrEnum


class EventStatuses(StrEnum):
    UP = "up"
    DOWN = "down"
    UNKNOWN = "unknown"


class EventContext(BaseModel):
    started_at: datetime
    ended_at: Optional[datetime] = None
    resource: Resources
    status: EventStatuses
    finished: bool = False
    log_ids: list[int] = Field(default_factory=list)  # logs that were grouped into this event


class Event(BaseEntity):
    __tablename__ = "hirsh_events"

    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    started_at = Column(DateTime, default=datetime.utcnow)
    ended_at = Column(DateTime)
    resource = Column(String(60))
    status = Column(String(60))
    notified = Column(Boolean, default=False)
    context = Column(JSON, nullable=True)
