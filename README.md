# twiki

This tool is meant to be run regularily and tweets recent changes made to a MediaWiki.

It can be seen in action at [@chaosdorf_wiki](https://twitter.com/chaosdorf_wiki).

## requirements

twiki needs a few things to work:

 * Python 3
 * a MediaWiki to monitor (it needs no account or key, though)
 * a Twitter account to post from (with credentials)
 * a few Python libraries

## installation

To get started, please clone this repo somewhere first.

Then create a new file called `config_local.py` containing at least these options:

```python
twitter_dry_run = True
twitter_api_key = '<key>'
twitter_api_secret = '<secret>'
twitter_token = '<token>'
twitter_token_secret = '<token secret>'
```

You may want to set the first option to `False` after confirming that everything works as expected.

You can configure twiki even more - simply override the values in `config.py`.

Then, please setup the pipenv: (You need to have pipenv installed for this.)

    pipenv install

You can test twiki and your configuration by running `pipenv run ./tweet.py`.

If everything works, set `twitter_dry_run` to `False` and add a cron job (or something similiar).
