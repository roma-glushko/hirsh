import asyncio
import time

from hirsh.services.monitors import Monitor


async def schedule(monitor: Monitor, check_every_secs: int = 60) -> None:
    """
    Schedule a monitor to execute every X seconds
    """

    def _until_next(last: float) -> float:
        time_took = time.time() - last

        return check_every_secs - time_took

    while True:
        time_start = time.time()

        try:
            await monitor.check()
        except asyncio.CancelledError:
            break
        except Exception:
            monitor.logger.exception("Error executing monitor check", exc_info=True)

        await asyncio.sleep(_until_next(last=time_start))


class Manager:
    async def start(self) -> None:
        ...

    async def stop(self) -> None:
        ...
