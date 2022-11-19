import config
import logging
import asyncio
import nio

log = logging.getLogger(__name__)


class MatrixClient:
    def __init__(self):
        self.client = nio.AsyncClient(config.MATRIX_SERVER, config.MATRIX_USER_NAME)

    def login(self):
        asyncio.get_event_loop().run_until_complete(self.client.login(config.MATRIX_PASSWORD))

    async def do_send_message(self, message):
        await self.client.room_send(
            room_id=config.MATRIX_ROOM_ID,
            message_type="m.room.message",
            content={
                "msgtype": "m.text",
                "body": message
            }
        )

    def send_message(self, message):
        asyncio.get_event_loop().run_until_complete(self.do_send_message(message))

    def __del__(self):
        asyncio.get_event_loop().run_until_complete(self.client.close())
