import logging
from datetime import datetime
from typing import AsyncGenerator, Optional, Sequence

from hirsh.entities import EventContext, EventStatuses, Log, Resources


class EventFinder:
    """
    Event Finder for the Basic Setup
    Given a sequence of logs/time series, it groups them into events that represents intervals
    where resources have similar status (e.g. downtimes, uptimes)
    """
    def __init__(self) -> None:
        self._logger = logging.getLogger(self.__class__.__name__)

    async def find(self, logs: Sequence[Log]) -> AsyncGenerator[EventContext, None]:
        contexts: dict[Resources, EventContext] = {}

        for log in logs:
            resource_type = Resources(log.resource)

            if resource_type == Resources.DAEMON:
                # detected a daemon downtime
                self._logger.debug("daemon shutdown is detected", extra={"log": log})

                latest_log_before_shutdown: Optional[datetime] = None

                for context in contexts.values():
                    # flush events
                    latest_log_before_shutdown = max(latest_log_before_shutdown, context.ended_at) \
                        if latest_log_before_shutdown \
                        else context.ended_at

                    context.finished = True

                    yield context

                self._logger.debug("last log before shutdown", extra={"at": latest_log_before_shutdown})

                contexts.clear()

                yield EventContext(
                    started_at=latest_log_before_shutdown,
                    ended_at=log.created_at,
                    resource=Resources.DAEMON,
                    status=EventStatuses.DOWN,
                    finished=True,
                )

                # if daemon was down then network was most likely down as well [the basic setup]
                contexts[Resources.NETWORK] = EventContext(
                    started_at=latest_log_before_shutdown,
                    resource=Resources.NETWORK,
                    status=EventStatuses.DOWN,
                    log_ids=[log.id],
                )

                continue

            if resource_type not in contexts:
                # detected a new event
                self._logger.debug("beginning of a new event is detected", extra={"log": log})

                content = EventContext(
                    resource=resource_type,
                    status=EventStatuses(log.status),
                    started_at=log.created_at,
                    log_ids=[log.id],
                )

                contexts[resource_type] = content
                continue

            # detected logs for the same resource (either with the same or different status)

            current_context = contexts[resource_type]
            current_context.ended_at = log.created_at

            if current_context.status != log.status:
                # status has changed which means the end of the prev event
                self._logger.debug("end of the current event", extra={
                    "resource": current_context.resource,
                    "context.status": current_context.status,
                    "log.status": log.status,
                })

                current_context.finished = True

                yield current_context

                # detected a new event
                content = EventContext(
                    resource=resource_type,
                    status=EventStatuses(log.status),
                    started_at=log.created_at,
                    log_ids=[log.id],
                )
                contexts[resource_type] = content
            else:
                # same status? Include the log into the event
                current_context.log_ids.append(log.id)

        self._logger.debug("flushing remaining events")

        # flush events
        for context in contexts.values():
            # we don't mark the remaining events as finished
            #  in order to finish, the event should be interrupted by status change or duration
            yield context
