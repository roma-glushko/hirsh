import logging
from pathlib import Path

from dependency_injector import containers, providers

from outage_detector.config import load_from_yaml
from outage_detector.daemon import Daemon
from outage_detector.repositories import init_database
from outage_detector.repositories.logs import LogRepository
from outage_detector.services.monitors import Monitor, NetworkMonitor

logger = logging.getLogger(__name__)

MONITORS: tuple[Monitor, ...] = (
    NetworkMonitor(check_every_secs=60),
)


class Runtime(containers.DeclarativeContainer):
    config = providers.Configuration()

    db = providers.Resource(init_database, database_uri=config.database.uri)

    log_repository = providers.Factory(
        LogRepository,
        session_factory=db.provided.session
    )

    event_repository = providers.Factory(
        LogRepository,
        session_factory=db.provided.session
    )

    outage_detector = providers.Singleton(Daemon, monitors=MONITORS)


def create_runtime(config_path: Path) -> Runtime:
    logger.debug("Initializing runtime container..")

    runtime = Runtime()

    config = load_from_yaml(config_path)
    runtime.config.from_pydantic(config)

    return runtime
