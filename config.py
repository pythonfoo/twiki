wiki_site = "en.wikipedia.org"
wiki_api_path = '/w/'
wiki_view_path = '/wiki/'

max_entries = 100
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
