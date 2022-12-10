import asyncio
import logging
import signal
import time
from typing import Sequence

from hirsh.services.monitors import DaemonMonitor, Monitor

logger = logging.getLogger(__name__)


async def schedule(monitor: Monitor) -> None:
    """
    Schedule a monitor to execute every X seconds
    """

    def _until_next(last: float) -> float:
        time_took = time.time() - last

        return monitor.check_every_secs - time_took

    while True:
        time_start = time.time()

        try:
            await monitor.check()
        except asyncio.CancelledError:
            break
        except Exception:
            monitor.logger.exception("Error executing monitor check")

        await asyncio.sleep(_until_next(last=time_start))


class Daemon:
    def __init__(self, lifecycle_monitor: DaemonMonitor, monitors: Sequence[Monitor]) -> None:
        self._lifecycle_monitor = lifecycle_monitor
        self._monitors = monitors
        self._monitor_tasks: list[asyncio.Task] = []
        self._stopping = False

    async def start(self) -> None:
        logger.info("Starting up the outage monitor")
        await self._lifecycle_monitor.startup()

        event_loop = asyncio.get_running_loop()

        for monitor in self._monitors:
            self._monitor_tasks.append(
                asyncio.create_task(schedule(monitor)),
            )

        for sig in (signal.SIGTERM, signal.SIGINT, signal.SIGQUIT):
            event_loop.add_signal_handler(sig, self.stop)

        await asyncio.gather(*self._monitor_tasks, return_exceptions=True)

        self.stop()

    def stop(self) -> None:
        if self._stopping:
            return

        self._stopping = True
        logger.info("Shutting down the outage detector")

        # TODO: allow to run async shutdown() method
        # await self._lifecycle_monitor.shutdown()

        for task, _monitor in zip(self._monitor_tasks, self._monitors):
            task.cancel()

        self._monitor_tasks.clear()

        logger.info("The outage detector has shutdown successfully")
