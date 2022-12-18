import asyncio
import logging
import signal
from typing import Sequence

from hirsh.managers.base import Manager
from hirsh.services.monitors import DaemonMonitor

logger = logging.getLogger(__name__)


class Daemon:
    def __init__(self, lifecycle_monitor: DaemonMonitor, managers: Sequence[Manager]) -> None:
        self._stopping = False

        self._lifecycle_monitor = lifecycle_monitor
        self._managers = managers
        self._manager_tasks: list[asyncio.Task] = []

    async def start(self) -> None:
        logger.info("Starting up Hirsh daemon")
        await self._lifecycle_monitor.startup()
        await self._register_signal_handlers()

        for manager in self._managers:
            self._manager_tasks.append(
                asyncio.create_task(manager.start()),
            )

        await asyncio.gather(*self._manager_tasks, return_exceptions=True)
        self.stop()

    async def _register_signal_handlers(self) -> None:
        event_loop = asyncio.get_running_loop()

        for sig in (signal.SIGTERM, signal.SIGINT, signal.SIGQUIT):
            event_loop.add_signal_handler(sig, self.stop)

    async def _stop(self) -> None:
        for manager, task in zip(self._managers, self._manager_tasks):
            await manager.stop()
            task.cancel()

        self._manager_tasks.clear()

        # await self._lifecycle_monitor.shutdown()

    def stop(self) -> None:
        if self._stopping:
            return

        self._stopping = True
        logger.info("Shutting down Hirsh daemon")

        event_loop = asyncio.get_event_loop()
        event_loop.create_task(self._stop())

        logger.info("Hirsh daemon has shut down successfully")
