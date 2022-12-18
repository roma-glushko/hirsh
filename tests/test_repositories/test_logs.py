from typing import Any

import pytest as pytest

from hirsh.entities import Resources, LogStatus, Log
from hirsh.repositories import LogRepository, Database
from tests.runtime import IntegrationRuntime
from sqlalchemy.future import select


@pytest.mark.parametrize(
    "log_data",
    [
        ({"resource": Resources.DAEMON, "status": LogStatus.UP}),
        ({"resource": Resources.NETWORK, "status": LogStatus.DOWN}),
        ({"resource": Resources.NETWORK, "status": LogStatus.UP, "context": {"downtime": "15m"}})
    ]
)
@pytest.mark.integration
async def test_adding_new_log(integration_runtime: IntegrationRuntime, log_data: dict[str, Any]) -> None:
    db: Database = await integration_runtime.db()
    log_repository: LogRepository = await integration_runtime.log_repository()

    await log_repository.add_log(**log_data)

    async with db.session() as session:
        result = await session.execute(select(Log).order_by(Log.id))

        record = result.scalars().first()

        for field, value in log_data.items():
            assert getattr(record, field) == value

        assert not record.processed
