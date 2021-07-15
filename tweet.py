#!/usr/bin/env python3
from twython import Twython
import readwiki
import config
import canTweet
from readwiki import WikiChange
import logging
log = logging.getLogger(__name__)


def setup_logging(log_level: str) -> None:
    """Configure logging."""
    numeric_log_level = getattr(logging, log_level.upper(), None)
    if not numeric_log_level:
        raise Exception("Invalid log level: {}".format(log_level))
    logging.basicConfig(level=numeric_log_level)


def run(api_key, api_secret, token, token_secret, last_revid, max_changes):
    """
    Tweets less than 'max_changes' changes newer than 'last_revid'.
    Returns the new 'last_revid'.
    """
    twitter = Twython(api_key, api_secret, token, token_secret)
    log.debug("set up a connection to the twitter api")
    changes = list()
    changes_overflow = False
    new_tweet_count = 0
    for change in readwiki.get_changes():
        if change.revId <= last_revid:
            break

        new_tweet_count += 1
        changes.append(change)

        if new_tweet_count >= max_changes:
            changes_overflow = True
            break
    log.debug("got the following changes: %s", changes)

    changes.reverse()

    if changes_overflow:
        log.debug("detected a overflow in changes")
        missing_message = \
            "Limit of changes reached. Please see https://{}{}Special:RecentChanges for more information."\
            .format(config.wiki_site, config.wiki_view_path)
        missing_link = WikiChange()
        missing_link.revId = changes[-1].revId
        missing_link.set_message(missing_message)
        
        changes.insert(0, missing_link)

    for change in changes:
        tweet(twitter, change.get_message())

    if not changes:
        return last_revid

    return changes[-1].revId


def tweet(twitter, message):
    logging.debug("Tweeting: %s", message)

    if not config.twitter_dry_run:
        twitter.update_status(status=message)
    else:
        log.warn('DRY RUN!')


if __name__ == '__main__':
    setup_logging(config.log_level)
    cTweet = canTweet.canTweet()

    highestRefId = run(
        config.twitter_api_key,
        config.twitter_api_secret,
        config.twitter_token,
        config.twitter_token_secret,
        cTweet.last_revid,
        config.max_entries)
    log.info("finished, got %s as the latest revid", highestRefId)

    cTweet.set_last_revid(highestRefId)
    cTweet.save()
