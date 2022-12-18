from typing import Sequence

import pytest
from datetime import datetime

from hirsh.entities import Log, Resources, LogStatus, Event, EventContext, EventStatuses
from hirsh.services.events import EventFinder


def dtime(date: str) -> datetime:
    return datetime.strptime(date, '%m/%d/%Y %H:%M:%S')


@pytest.mark.parametrize(
    "logs,events",
    [
        (
                (
                        Log(id=0, created_at=dtime("12/18/2022 11:53:00"), resource=Resources.NETWORK, status=LogStatus.UP),
                        Log(id=1, created_at=dtime("12/18/2022 11:58:00"), resource=Resources.NETWORK, status=LogStatus.UP),
                        Log(id=2, created_at=dtime("12/18/2022 12:00:00"), resource=Resources.NETWORK, status=LogStatus.UP),
                        Log(id=3, created_at=dtime("12/18/2022 12:15:00"), resource=Resources.NETWORK, status=LogStatus.UP),
                        Log(id=4, created_at=dtime("12/18/2022 12:30:00"), resource=Resources.NETWORK, status=LogStatus.DOWN),
                ),
                (
                        EventContext(
                            started_at=dtime("12/18/2022 11:53:00"),
                            ended_at=dtime("12/18/2022 12:30:00"),
                            resource=Resources.NETWORK,
                            status=EventStatuses.UP,
                            log_ids=[0, 1, 2, 3],
                        ),
                        EventContext(
                            started_at=dtime("12/18/2022 12:30:00"),
                            ended_at=None,
                            resource=Resources.NETWORK,
                            status=EventStatuses.DOWN,
                            log_ids=[4],
                        ),
                )
        ),
        (
            (
                    Log(id=0, created_at=dtime("12/18/2022 11:53:00"), resource=Resources.NETWORK, status=LogStatus.UP),
                    Log(id=1, created_at=dtime("12/18/2022 12:15:00"), resource=Resources.NETWORK, status=LogStatus.UP),
                    Log(id=2, created_at=dtime("12/18/2022 12:30:00"), resource=Resources.NETWORK, status=LogStatus.DOWN),
                    Log(id=3, created_at=dtime("12/18/2022 13:00:00"), resource=Resources.NETWORK, status=LogStatus.DOWN),
                    Log(id=4, created_at=dtime("12/18/2022 13:10:00"), resource=Resources.NETWORK, status=LogStatus.UP),
                    Log(id=5, created_at=dtime("12/18/2022 13:15:00"), resource=Resources.NETWORK, status=LogStatus.UP),
            ),
            (
                EventContext(
                    started_at=dtime("12/18/2022 11:53:00"),
                    ended_at=dtime("12/18/2022 12:30:00"),
                    resource=Resources.NETWORK,
                    status=EventStatuses.UP,
                    log_ids=[0, 1],
                ),
                EventContext(
                    started_at=dtime("12/18/2022 12:30:00"),
                    ended_at=dtime("12/18/2022 13:10:00"),
                    resource=Resources.NETWORK,
                    status=EventStatuses.DOWN,
                    log_ids=[2, 3],
                ),
                EventContext(
                    started_at=dtime("12/18/2022 13:10:00"),
                    ended_at=dtime("12/18/2022 13:15:00"),
                    resource=Resources.NETWORK,
                    status=EventStatuses.UP,
                    log_ids=[4, 5],
                ),
            )
        ),
        (
                (
                        Log(id=0, created_at=dtime("12/18/2022 11:53:00"), resource=Resources.NETWORK, status=LogStatus.UP),
                        Log(id=1, created_at=dtime("12/18/2022 13:15:00"), resource=Resources.NETWORK, status=LogStatus.UP),
                        Log(id=2, created_at=dtime("12/18/2022 14:00:00"), resource=Resources.DAEMON, status=LogStatus.UP),
                        Log(id=3, created_at=dtime("12/18/2022 14:00:05"), resource=Resources.NETWORK, status=LogStatus.DOWN),
                        Log(id=4, created_at=dtime("12/18/2022 14:05:00"), resource=Resources.NETWORK, status=LogStatus.UP),
                ),
                (
                        EventContext(
                            started_at=dtime("12/18/2022 11:53:00"),
                            ended_at=dtime("12/18/2022 13:15:00"),
                            resource=Resources.NETWORK,
                            status=EventStatuses.UP,
                            log_ids=[0, 1],
                        ),
                        EventContext(
                            started_at=dtime("12/18/2022 13:15:00"),
                            ended_at=dtime("12/18/2022 14:00:00"),
                            resource=Resources.DAEMON,
                            status=EventStatuses.DOWN,
                        ),
                        EventContext(
                            started_at=dtime("12/18/2022 13:15:00"),
                            ended_at=dtime("12/18/2022 14:05:00"),
                            resource=Resources.NETWORK,
                            status=EventStatuses.DOWN,
                            log_ids=[2, 3],
                        ),
                        EventContext(
                            started_at=dtime("12/18/2022 14:05:00"),
                            ended_at=None,
                            resource=Resources.NETWORK,
                            status=EventStatuses.UP,
                            log_ids=[4],
                        ),
                )
        ),
    ],
    ids=(
            "uptime-and-then-ongoing-downtime",
            "uptime-downtime-ongoing-uptime",
            "uptime-startup",
    )
)
async def test__eventfinder__find_donwtime(logs: Sequence[Log], events: Sequence[Event]) -> None:
    event_finder = EventFinder()

    actual_events = []
    async for event in event_finder.find(logs):
        actual_events.append(event)

    assert len(actual_events) == len(events)

    for actual_event, expected_event in zip(actual_events, events):
        assert actual_event == expected_event


@pytest.mark.parametrize(
    "logs,events",
    [
        (
            (
                Log(id=0, created_at=dtime("12/18/2022 11:53:00"), resource=Resources.NETWORK, status=LogStatus.UP),
                Log(id=1, created_at=dtime("12/18/2022 13:15:00"), resource=Resources.NETWORK, status=LogStatus.UP),
                Log(id=2, created_at=dtime("12/18/2022 14:00:00"), resource=Resources.NETWORK, status=LogStatus.UP),
            ),
            (
                EventContext(
                    started_at=dtime("12/18/2022 11:53:00"),
                    ended_at=dtime("12/18/2022 14:00:00"),
                    resource=Resources.NETWORK,
                    status=EventStatuses.UP,
                    log_ids=[0, 1, 2]
                ),
            )
        )
    ],
    ids=(
        "uptime-for-long-time",
    )
)
async def test__eventfinder__slice_long_intervals_into_events(logs: Sequence[Log], events: Sequence[Event]) -> None:
    event_finder = EventFinder()

    actual_events = []
    async for event in event_finder.find(logs):
        actual_events.append(event)

    assert len(actual_events) == len(events)

    for actual_event, expected_event in zip(actual_events, events):
        assert actual_event == expected_event
