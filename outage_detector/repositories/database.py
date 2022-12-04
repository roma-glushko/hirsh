import logging
from asyncio import current_task
from contextlib import AbstractAsyncContextManager, asynccontextmanager
from typing import AsyncGenerator, Generator

from sqlalchemy.ext.asyncio import AsyncSession, async_scoped_session, create_async_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

logger = logging.getLogger(__name__)

BaseEntity = declarative_base()


class Database:
    """
    Low-level SQLite session manager
    """

    def __init__(self, database_uri: str) -> None:
        self._engine = create_async_engine(database_uri, echo=True)

        self._session_factory = async_scoped_session(
            sessionmaker(
                bind=self._engine,
                autocommit=False,
                autoflush=False,
                class_=AsyncSession,
            ),
            scopefunc=current_task,
        )

    async def create_database(self) -> None:
        async with self._engine.begin() as conn:
            await conn.run_sync(BaseEntity.metadata.create_all)

    @asynccontextmanager
    async def session(self) -> AsyncGenerator[AbstractAsyncContextManager[AsyncSession], None]:
        session: AsyncSession = self._session_factory()
        try:
            yield session
        except Exception:
            logger.exception("Session rollback because of exception")
            await session.rollback()
            raise
        finally:
            await session.close()

    async def close(self) -> None:
        await self._engine.dispose()


async def init_database(database_uri: str) -> Generator[Database, None, None]:
    database = Database(database_uri)
    await database.create_database()
    yield database
    await database.close()
