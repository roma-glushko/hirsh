from collections import defaultdict
from datetime import datetime
from typing import Any, Optional, Sequence

from outage_detector.entities import Event, Log, LogStatus, Resources


class EventFinder:
    def __init__(self) -> None:
        ...

    def find(self, logs: Sequence[Log]) -> list[Event]:
        events: dict[Resources, list[Event]] = defaultdict(list)
        context: dict[Resources, Optional[dict[str, Any]]] = {}
        processed_ids: list[int] = []

        for log in logs:
            resource_type = Resources(log.resource)

            if resource_type == Resources.DAEMON:
                # detected a daemon downtime
                latest_log: Optional[datetime] = None

                for type, context in context.items():
                    # flush events
                    latest_log = max(latest_log, context["finished_at"]) if latest_log else context["finished_at"]
                    events[type].append(Event(**context))

                context.clear()
                processed_ids.append(log.id)

                events[Resources.DAEMON] = Event(
                    started_at=latest_log,
                    ended_at=log.created_at,
                    resource=Resources.DAEMON,
                    status="down",
                )

            if resource_type not in context:
                context[resource_type] = {
                    "resource": resource_type,
                    "status": LogStatus(log.status),
                    "started_at": log.created_at,
                    "finished_at": None,
                }
                processed_ids.append(log.id)
                continue

            current_context = context.get(resource_type)

            current_context["finished_at"] = log.created_at

            if current_context["status"] != log.status:
                # end of the interval
                events[resource_type].append(Event(**current_context))

        return events
