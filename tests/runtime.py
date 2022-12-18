from unittest import mock

from dependency_injector import containers
from dependency_injector.providers import Singleton

from hirsh.runtime import Runtime
from hirsh.services.notifiers import Notifier


@containers.copy(Runtime)
class IntegrationRuntime(containers.DeclarativeContainer):
    notifier = Singleton(mock.AsyncMock(spec=Notifier))

