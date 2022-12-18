from typing import Generator

import pytest

from tests.runtime import IntegrationRuntime


@pytest.fixture
async def integration_runtime() -> Generator[IntegrationRuntime, None, None]:
    runtime = IntegrationRuntime(config={
        "database": {
            "uri": "sqlite+aiosqlite://",
        }
    })
    await runtime.init_resources()
    yield runtime
    await runtime.shutdown_resources()