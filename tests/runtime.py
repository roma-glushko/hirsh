from unittest import mock

from dependency_injector.providers import Singleton

from hirsh.runtime import Runtime
from hirsh.services.notifiers import Notifier


class IntegrationRuntime(Runtime):
    notifier = Singleton[mock.AsyncMock(spec=Notifier)]
