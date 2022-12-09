import logging
from pathlib import Path

from dependency_injector import containers, providers
from dependency_injector.providers import Singleton, Resource, Configuration

from outage_detector.config import load_from_yaml
from outage_detector.daemon import Daemon
from outage_detector.logging import init_logger
from outage_detector.repositories import EventRepository, LogRepository, init_database, Database
from outage_detector.services.monitors import DaemonMonitor, NetworkMonitor
from outage_detector.services.notifiers import TelegramNotifier

logger = logging.getLogger(__name__)


class Runtime(containers.DeclarativeContainer):
    config = Configuration()

    db: Resource[Database] = Resource(init_database, database_uri=config.database.uri)

    log_repository: Singleton[LogRepository] = Singleton(
        LogRepository,
        session_factory=db.provided.session
    )

    event_repository: Singleton[EventRepository] = Singleton(
        EventRepository,
        session_factory=db.provided.session
    )

    notifier: Singleton[TelegramNotifier] = Singleton(
        TelegramNotifier,
        bot_token=config.telegram.bot_token,
        channel_ids=config.telegram.channel_ids,
    )

    daemon_monitor: Singleton[DaemonMonitor] = Singleton(
        DaemonMonitor,
        log_repository=log_repository,
        notifier=notifier,
    )

    daemon: Singleton[Daemon] = Singleton(
        Daemon,
        lifecycle_monitor=daemon_monitor,
        monitors=providers.List(
            Singleton(NetworkMonitor, check_every_secs=60, log_repository=log_repository),
        )
    )


def create_runtime(config_path: Path) -> Runtime:
    logger.debug("Initializing runtime container..")

    runtime = Runtime()

    config = load_from_yaml(config_path)
    runtime.config.from_pydantic(config)

    init_logger(log_level=runtime.config.logging.level())

    return runtime
