from typing import Optional, Any

from outage_detector.entities import Log, Resources, LogStatus


class LogRepository:
    """
    Manage monitor logs in the database
    """

    def __init__(self, session_factory) -> None:
        self.session_factory = session_factory

    async def add_log(self, resource: Resources, status: LogStatus, context: Optional[dict[str, Any]] = None) -> None:
        async with self.session_factory() as session:
            log = Log(
                resource=str(resource),
                status=str(status),
                processed=False,
                context=context,
            )

            session.add(log)

            await session.commit()
