import logging
from pathlib import Path

from dependency_injector import containers, providers

from outage_detector.config import load_from_yaml
from outage_detector.daemon import Daemon
from outage_detector.logging import init_logger
from outage_detector.repositories import EventRepository, LogRepository, init_database
from outage_detector.services.monitors import DaemonMonitor, NetworkMonitor

logger = logging.getLogger(__name__)


class Runtime(containers.DeclarativeContainer):
    config = providers.Configuration()

    db = providers.Resource(init_database, database_uri=config.database.uri)

    log_repository = providers.Factory(
        LogRepository,
        session_factory=db.provided.session
    )

    event_repository = providers.Factory(
        EventRepository,
        session_factory=db.provided.session
    )

    outage_detector = providers.Singleton(
        Daemon,
        lifecycle_monitor=providers.Factory(DaemonMonitor, log_repository=log_repository),
        monitors=providers.List(
            providers.Factory(NetworkMonitor, check_every_secs=60, log_repository=log_repository),
        )
    )


def create_runtime(config_path: Path) -> Runtime:
    logger.debug("Initializing runtime container..")

    runtime = Runtime()

    config = load_from_yaml(config_path)
    runtime.config.from_pydantic(config)

    init_logger(log_level=runtime.config.logging.level())

    return runtime
