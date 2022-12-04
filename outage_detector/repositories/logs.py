from outage_detector.entities import Log, Resources


class LogRepository:
    """
    Manage monitor logs in the database
    """

    def __init__(self, session_factory):
        self.session_factory = session_factory

    async def log(self, resource: Resources):
        async with self.session_factory() as session:
            log = Log(
                resource=resource,
            )

            session.add(log)
            session.commit()
