import logging

from outage_detector.services.network import check_internet_connection


class Monitor:
    def __init__(self, check_every_secs: int) -> None:
        self.check_every_secs = check_every_secs
        self.logger = logging.getLogger(self.__class__.__name__)

    async def check(self) -> None:
        raise NotImplementedError()


class NetworkMonitor(Monitor):
    async def check(self) -> None:
        self.logger.debug("Checking network connection")

        await check_internet_connection()


class ElectricityMonitor(Monitor):
    """
    TODO: For the phase 1 of the project, we will implement network monitor only.
        Electricity monitoring could require more effort and planning to implement
    """
