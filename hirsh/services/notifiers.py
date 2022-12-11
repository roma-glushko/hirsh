import logging


from aiogram import Bot, types
from aiogram.utils.exceptions import NetworkError


class Notifier:
    async def notify(self, message: str) -> None:
        raise NotImplementedError()


class TelegramNotifier(Notifier):
    def __init__(self, bot_token: str, channel_ids: list[int]) -> None:
        self.logger = logging.getLogger(self.__class__.__name__)

        self._bot = Bot(token=bot_token, parse_mode=types.ParseMode.HTML)
        self._channel_ids = channel_ids

    async def notify(self, message: str) -> None:
        try:
            for channel_id in self._channel_ids:
                await self._bot.send_message(
                    chat_id=channel_id,
                    text=message,
                    disable_notification=False,
                )
        except NetworkError:
            # TODO: Deferred message sending on no connection
            #  https://github.com/roma-glushko/hirsh/issues/1
            self.logger.warning(
                "No internet connection to notify the targets",
                extra={
                    "notification": message,
                },
            )