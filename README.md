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
TWITTER_DRY_RUN = True
TWITTER_API_KEY = '<key>'
TWITTER_API_SECRET = '<secret>'
TWITTER_TOKEN = '<token>'
TWITTER_TOKEN_SECRET = '<token secret>'
```

For docker, you can set these also in the `container/.env` file in uppercase (INTERVAL is docker exclusive in seconds):
```dotenv
INTERVAL=300
TWITTER_DRY_RUN=1
TWITTER_API_KEY=<KEY>
TWITTER_API_SECRET=<SECRET>
TWITTER_TOKEN=<TOKEN>
TWITTER_TOKEN_SECRET=<TOKEN_SECRET>
```

You may want to set the first option to `False` after confirming that everything works as expected.

You can configure twiki even more - simply override the values in `config.py`.

Then, please setup the pipenv: (You need to have pipenv installed for this.)

    pipenv install

You can test twiki and your configuration by running `pipenv run ./tweet.py`.

If you don't want to install pipenv just for this application
(you should, your're missing some nice features), you can still use pip:

    pip3 install -r requirements.txt

And then run it with `python3 tweet.py`.

If everything works, set `twitter_dry_run` to `False` and add a cron job (or something similiar).

## docker

```shell
docker-compose up
```

Set the environment variable `INTERVAL` in seconds for the call-delay. Default is 300 seconds (5 minutes).  
You can use `container/.env` file.  Do not commit this with any data, it just has to exist for compose to function.  
```dotenv
INTERVAL=300
```
