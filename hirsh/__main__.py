import logging
from asyncio import run as aiorun
from pathlib import Path

import typer
import uvloop

from hirsh.daemon import Daemon
from hirsh.runtime import create_runtime

logger = logging.getLogger(__name__)


def run(
    working_dir: Path = typer.Option("~/.hirsh", exists=True, readable=True),  # noqa: B008
    config_filename: str = "config.yaml",
) -> None:
    """
    Hirsh: Be first to know about outages in your apartments
    """

    config_path: Path = working_dir / config_filename

    if not config_path.exists() or not config_path.is_file():
        raise ValueError(f"Make sure the config file {config_path} exists and it's readable")

    async def __run() -> None:
        runtime = create_runtime(config_path=config_path)

        logger.debug("Initializing resources..")
        if init_resources := runtime.init_resources():
            await init_resources

        daemon: Daemon = await runtime.daemon()
        await daemon.start()

        logger.debug("Shutting down resources..")
        if shutdown_resources := runtime.shutdown_resources():
            await shutdown_resources

    aiorun(__run())


if __name__ == "__main__":
    uvloop.install()
    typer.run(run)
