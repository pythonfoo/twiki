import os
import logging

log = logging.getLogger(__name__)


WIKI_SITE = "en.wikipedia.org"
WIKI_API_PATH = '/w/'
WIKI_VIEW_PATH = '/wiki/'

# log-level: https://docs.python.org/3/library/logging.html#logging-levels
LOG_LEVEL = logging.ERROR
MAX_ENTRIES = 25
IGNORE_MINOR_CHANGES = False
IGNORE_BOTS = False

TWITTER_ACTIVE = False
TWITTER_DRY_RUN = False
TWITTER_API_KEY = ''
TWITTER_API_SECRET = ''
TWITTER_TOKEN = ''
TWITTER_TOKEN_SECRET = ''

MATRIX_ACTIVE = True
MATRIX_DRY_RUN = False
MATRIX_USER_NAME = ''  # @chaosdorf_wiki:matrix.org
MATRIX_PASSWORD = ''
MATRIX_SERVER = ''  # https://matrix-client.matrix.org
MATRIX_ROOM_ID = ''  # !aqsASgGGPgMEVHeMdW:cybre.space

MASTODON_ACTIVE = True
MASTODON_DRY_RUN = False
MASTODON_ACCESS_TOKEN = ''
MASTODON_API_BASE_URL = ''  # https://botsin.space

DISCORD_ACTIVE = True
DISCORD_DRY_RUN = False
DISCORD_APP_ID = ''
DISCORD_TOKEN = ''
DISCORD_CHANNEL_ID = ''

USER_NAME_BLACK_LIST = set()


try:
    from config_local import *
except ImportError as ex:
    pass

logging.basicConfig(level=LOG_LEVEL)

# loop over all local vars and overwrite with found environ vars
for name in list(vars().keys()):
    if name.isupper() and name in os.environ:
        logging.debug("Setting ENV var: %s", name)
        try:
            locals()[name] = int(os.environ[name])
        except ValueError:
            locals()[name] = os.environ[name]
