from hirsh.managers.base import Manager


class EventManager(Manager):
    async def start(self) -> None:
        ...

    async def stop(self) -> None:
        ...