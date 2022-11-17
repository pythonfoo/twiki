#!/usr/bin/env python3
import logging
from twython import Twython
import config
from readwiki import WikiChange
import readwiki
import CanMessage
import MatrixClient

log = logging.getLogger(__name__)


def run(last_revid):
    """
    Tweets less than 'max_changes' changes newer than 'last_revid'.
    Returns the new 'last_revid'.
    """
    log.debug("last rev id: %s", last_revid)

    log.debug("set up a connection to the twitter api")
    twitter = Twython(
        config.TWITTER_API_KEY,
        config.TWITTER_API_SECRET,
        config.TWITTER_TOKEN,
        config.TWITTER_TOKEN_SECRET
    )

    matrix_bot = None
    if MatrixClient.data_valid():
        log.debug("set up a connection to matrix")
        matrix_bot = MatrixClient.MatrixClient()
        matrix_bot.login()

    changes = list()
    changes_overflow = False
    new_messages_count = 0
    for change in readwiki.get_changes():
        if change.revId <= last_revid:
            break

        new_messages_count += 1
        changes.append(change)

        if new_messages_count >= config.MAX_ENTRIES:
            changes_overflow = True
            break

    log.debug("got the following changes: %s", changes)

    changes.reverse()

    if changes_overflow:
        log.debug("detected a overflow in changes")
        missing_message = \
            "Limit of {} changes reached. Please see https://{}{}Special:RecentChanges for more information."\
            .format(config.MAX_ENTRIES, config.WIKI_SITE, config.WIKI_VIEW_PATH)
        missing_link = WikiChange()
        missing_link.revId = changes[-1].revId
        missing_link.set_message(missing_message)
        
        changes.insert(0, missing_link)

    for change in changes:
        message = change.get_message()
        tweet(twitter, message)
        toot(None, message)
        matrix(matrix_bot, message)

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
        log.warning('TWITTER DRY RUN!')


def toot(_mastodon, message):
    log.warning('MASTODON NOT IMPLEMENTED')


def matrix(_matrix, message):
    if _matrix is None:
        return

    if not config.MATRIX_DRY_RUN:
        _matrix.send_message(message)
    else:
        log.warning('MATRIX DRY RUN!')


if __name__ == '__main__':
    can_message = CanMessage.CanMessage()

    highest_ref_id = run(can_message.last_revid)
    log.info("finished, got %s as the latest revid", highest_ref_id)

    if config.TWITTER_DRY_RUN or config.MATRIX_DRY_RUN:
        log.info("DRY_RUN, don't save revid")
    else:
        can_message.set_last_revid(highest_ref_id)
        can_message.save()
