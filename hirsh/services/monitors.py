import logging

import socket

from hirsh.entities import LogStatus, Resources
from hirsh.repositories import LogRepository
from hirsh.services.network import check_internet_connection
from hirsh.services.notifiers import Notifier


class Monitor:
    def __init__(self, check_every_secs: int) -> None:
        self.check_every_secs = check_every_secs
        self.logger = logging.getLogger(self.__class__.__name__)

    async def check(self) -> None:
        raise NotImplementedError()


class DaemonMonitor:
    """
    Special type of monitors that tracks daemon lifecycle
    """

    def __init__(self, log_repository: LogRepository, notifier: Notifier) -> None:
        self._log_repository = log_repository
        self._notifier = notifier

    def _hostname(self) -> str:
        return socket.gethostname()

    async def startup(self) -> None:
        await self._log_repository.add_log(
            resource=Resources.DAEMON,
            status=LogStatus.UP,
        )

        await self._notifier.notify(f"📟 Hirsh ({self._hostname()}) is starting up..")

    async def shutdown(self) -> None:
        await self._log_repository.add_log(
            resource=Resources.DAEMON,
            status=LogStatus.DOWN,
        )

        await self._notifier.notify(f"📟 Hirsh ({self._hostname()}) is shutting down..")


class NetworkMonitor(Monitor):
    def __init__(self, log_repository: LogRepository, notifier: Notifier, check_every_secs: int = 60) -> None:
        super().__init__(check_every_secs)

        self._log_repository = log_repository
        self._notifier = notifier

    async def check(self) -> None:
        self.logger.debug("Checking network connection")

        network_status: bool = await check_internet_connection()

        if network_status:
            await self._notifier.notify("📡 Network is working at the moment")

        await self._log_repository.add_log(
            resource=Resources.NETWORK,
            status=LogStatus.UP if network_status else LogStatus.DOWN,
        )


class ElectricityMonitor(Monitor):
    """
    TODO: For the phase 1 of the project, we will implement network monitor only.
        Electricity monitoring could require more effort and planning to implement

    """
