import asyncio

import pytest as pytest

from hirsh.daemon import Daemon
from tests.runtime import IntegrationRuntime


@pytest.mark.integration
async def test__daemon__runs(integration_runtime: IntegrationRuntime) -> None:
    daemon: Daemon = await integration_runtime.daemon()

    await daemon.start()
    await asyncio.sleep(0.1)
    daemon.stop()
