import os
import logging

log = logging.getLogger(__name__)


def setup_logging(_log_level: str) -> None:
    """Configure logging."""
    numeric_log_level = getattr(logging, _log_level.upper(), None)
    if not numeric_log_level:
        raise Exception("Invalid log level: {}".format(_log_level))
    logging.basicConfig(level=numeric_log_level)


WIKI_SITE = "en.wikipedia.org"
WIKI_API_PATH = '/w/'
WIKI_VIEW_PATH = '/wiki/'

# log-level: https://docs.python.org/3/library/logging.html#logging-levels
LOG_LEVEL = "INFO"
MAX_ENTRIES = 25
IGNORE_MINOR_CHANGES = False
IGNORE_BOTS = False

TWITTER_DRY_RUN = True
TWITTER_API_KEY = ''
TWITTER_API_SECRET = ''
TWITTER_TOKEN = ''
TWITTER_TOKEN_SECRET = ''

USER_NAME_BLACK_LIST = set()


try:
    from config_local import *
except ImportError as ex:
    pass

setup_logging(LOG_LEVEL)

# loop over all local vars and overwrite with found environ vars
for name in list(vars().keys()):
    if name.isupper() and name in os.environ:
        logging.debug("Setting ENV var: %s", name)
        try:
            locals()[name] = int(os.environ[name])
        except ValueError:
            locals()[name] = os.environ[name]
