import asyncio
import logging
from typing import Sequence

from hirsh.managers.base import schedule, Manager
from hirsh.services.monitors import Monitor

logger = logging.getLogger(__name__)


class LogManager(Manager):
    def __init__(self,  monitors: Sequence[Monitor], check_every_secs: int = 60) -> None:
        self._monitors = monitors
        self._monitor_tasks: list[asyncio.Task] = []

        self._check_every_secs = check_every_secs

    async def start(self) -> None:
        for monitor in self._monitors:
            self._monitor_tasks.append(
                asyncio.create_task(schedule(monitor, check_every_secs=self._check_every_secs)),
            )

        await asyncio.gather(*self._monitor_tasks, return_exceptions=True)

    async def stop(self) -> None:
        for task in self._monitor_tasks:
            task.cancel()

        await asyncio.gather(*self._monitor_tasks, return_exceptions=True)

        self._monitor_tasks.clear()

