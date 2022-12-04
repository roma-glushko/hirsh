import asyncio
import contextlib
import socket


async def check_internet_connection() -> bool:
    """
    Check internet connection by trying to access Google's website
    TODO: we may need to try a few times before reporting no internet access
    """
    def _check_connection() -> bool:
        with contextlib.suppress(OSError):
            conn = socket.create_connection(("www.google.com", 80))
            conn.close()

            return True

        return False

    loop = asyncio.get_event_loop()

    return await loop.run_in_executor(None, _check_connection)
