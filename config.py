import os

wiki_site = "en.wikipedia.org"
wiki_api_path = '/w/'
wiki_view_path = '/wiki/'

log_level = "INFO"
max_entries = 100
ignore_minor_changes = False
ignore_bots = False

twitter_dry_run = True
twitter_api_key = ''
twitter_api_secret = ''
twitter_token = ''
twitter_token_secret = ''

user_name_black_list = set()

try:
    from config_local import *
except ImportError as ex:
    pass

# loop over all local vars and overwrite with found environ vars
for name in list(vars().keys()):
    if name.upper() in os.environ:
        try:
            locals()[name] = int(os.environ[name.upper()])
        except ValueError:
            locals()[name] = os.environ[name.upper()]
