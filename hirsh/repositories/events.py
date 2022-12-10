from hirsh.entities import Resources
from hirsh.entities.events import Event


class EventRepository:
    """
    Manage monitor events in the database
    """

    def __init__(self, session_factory) -> None:
        self.session_factory = session_factory

    async def add_event(self, resource: Resources) -> None:
        async with self.session_factory() as session:
            log = Event(
                resource=resource,
            )

            session.add(log)
            session.commit()
