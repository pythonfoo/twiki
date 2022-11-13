#!/usr/bin/env python3
from twython import Twython
import readwiki
import config
import canTweet
from readwiki import WikiChange
import logging

log = logging.getLogger(__name__)


def run(api_key, api_secret, token, token_secret, last_revid, max_changes):
    """
    Tweets less than 'max_changes' changes newer than 'last_revid'.
    Returns the new 'last_revid'.
    """
    log.debug("last rev id: %s", last_revid)
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
            .format(config.WIKI_SITE, config.WIKI_VIEW_PATH)
        missing_link = WikiChange()
        missing_link.revId = changes[-1].revId
        missing_link.set_message(missing_message)
        
        changes.insert(0, missing_link)

    for change in changes:
        tweet(twitter, change.get_message())

    if not changes:
        log.debug("no changes, rev id: %s", last_revid)
        return last_revid

    log.debug("new rev id: %s", changes[-1].revId)
    return changes[-1].revId


def tweet(twitter, message):
    logging.debug("Tweeting: %s", message)

    if not config.TWITTER_DRY_RUN:
        twitter.update_status(status=message)
    else:
        log.warning('DRY RUN!')


if __name__ == '__main__':
    cTweet = canTweet.canTweet()

    highestRefId = run(
        config.TWITTER_API_KEY,
        config.TWITTER_API_SECRET,
        config.TWITTER_TOKEN,
        config.TWITTER_TOKEN_SECRET,
        cTweet.last_revid,
        config.MAX_ENTRIES)
    log.info("finished, got %s as the latest revid", highestRefId)

    if config.TWITTER_DRY_RUN:
        log.info("TWITTER_DRY_RUN, don't save revid")
    else:
        cTweet.set_last_revid(highestRefId)
        cTweet.save()
