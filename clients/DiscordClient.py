import config
import logging
import requests

log = logging.getLogger(__name__)


class DiscordClient:
    def __init__(self):
        self.URL = 'https://discord.com/api/v9/channels/{}/messages'.format(config.DISCORD_CHANNEL_ID)

    def send_message(self, message):
        header = {
            'authorization': 'Bot ' + config.DISCORD_TOKEN,
        }

        payload = {
            'content': message,
        }

        requests.post(self.URL, data=payload, headers=header)
