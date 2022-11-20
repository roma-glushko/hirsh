import logging


class Monitor:
    def __init__(self, check_every_secs: int) -> None:
        self.check_every_secs = check_every_secs
        self.logger = logging.getLogger(self.__class__.__name__)

    async def check(self) -> None:
        raise NotImplementedError()


class InternetMonitor(Monitor):
    ...


class ElectricityMonitor(Monitor):
    ...
