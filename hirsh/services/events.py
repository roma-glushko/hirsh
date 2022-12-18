import logging
from datetime import datetime
from typing import AsyncGenerator, Optional, Sequence

from hirsh.entities import Log, Resources, EventContext, EventStatuses


class EventFinder:
    """
    TODO: Finish the event finder
      https://github.com/roma-glushko/hirsh/issues/2
    """
    def __init__(self) -> None:
        self._logger = logging.getLogger(self.__class__.__name__)

    async def find(self, logs: Sequence[Log]) -> AsyncGenerator[EventContext, None]:
        contexts: dict[Resources, EventContext] = {}

        for log in logs:
            resource_type = Resources(log.resource)

            if resource_type == Resources.DAEMON:
                # detected a daemon downtime
                latest_log_before_shutdown: Optional[datetime] = None

                for context in contexts.values():
                    # flush events
                    latest_log_before_shutdown = max(latest_log_before_shutdown, context.ended_at) \
                        if latest_log_before_shutdown \
                        else context.ended_at

                    yield context

                contexts.clear()

                yield EventContext(
                    started_at=latest_log_before_shutdown,
                    ended_at=log.created_at,
                    resource=Resources.DAEMON,
                    status=EventStatuses.DOWN,
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

        # flush events
        for context in contexts.values():
            yield context
