#!/usr/bin/env python3
import logging
from twython import Twython
from MatrixClient import MatrixClient
from mastodon import Mastodon
import config
import helper
from readwiki import WikiChange
import readwiki
import CanMessage

log = logging.getLogger(__name__)


def get_bot_twitter() -> Twython or None:
    if not helper.can_twitter():
        return None

    log.debug("set up a connection to twitter")

    twitter_bot = None
    try:
        twitter_bot = Twython(
            config.TWITTER_API_KEY,
            config.TWITTER_API_SECRET,
            config.TWITTER_TOKEN,
            config.TWITTER_TOKEN_SECRET
        )
    except Exception as ex:
        log.error("ERROR LOGIN TWITTER: " + str(ex))
        twitter_bot = None

    return twitter_bot


def get_bot_matrix() -> MatrixClient() or None:
    if not helper.can_matrix():
        return None

    log.debug("set up a connection to matrix")

    matrix_bot = None
    try:
        matrix_bot = MatrixClient()
        matrix_bot.login()
    except Exception as ex:
        log.error("ERROR LOGIN MATRIX: " + str(ex))
        matrix_bot = None

    return matrix_bot


def get_bot_mastodon() -> Mastodon() or None:
    if not helper.can_mastodon():
        return None

    log.debug("set up a connection to mastodon")

    mastodon_bot = None
    try:
        mastodon_bot = Mastodon(
            access_token=config.MASTODON_ACCESS_TOKEN,
            api_base_url=config.MASTODON_API_BASE_URL
        )
    except Exception as ex:
        log.error("ERROR LOGIN MASTODON: " + str(ex))
        mastodon_bot = None

    return mastodon_bot


def run(last_revid):
    """
    Tweets less than 'max_changes' changes newer than 'last_revid'.
    Returns the new 'last_revid'.
    """
    log.debug("last rev id: %s", last_revid)

    twitter_bot = get_bot_twitter()
    matrix_bot = get_bot_matrix()
    mastodon_bot = get_bot_mastodon()

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
        tweet(twitter_bot, message)
        toot(mastodon_bot, message)
        matrix(matrix_bot, message)

    if not changes:
        log.debug("no changes, rev id: %s", last_revid)
        return last_revid

    log.debug("new rev id: %s", changes[-1].revId)
    return changes[-1].revId


def tweet(twitter, message):
    if twitter is None:
        return

    logging.debug("Send tweet: %s", message)

    if not config.TWITTER_DRY_RUN:
        try:
            twitter.update_status(status=message)
        except Exception as ex:
            log.error('TWITTER SEND ERROR: ' + str(ex))
    else:
        log.warning('TWITTER DRY RUN!')


def toot(_mastodon, message):
    if _mastodon is None:
        return

    logging.debug("Send toot: %s", message)

    if not config.MASTODON_DRY_RUN:
        try:
            _mastodon.toot(message)
        except Exception as ex:
            log.error('MASTODON SEND ERROR: ' + str(ex))
    else:
        log.warning('MASTODON DRY RUN!')


def matrix(_matrix, message):
    if _matrix is None:
        return

    logging.debug("Send matrix: %s", message)

    if not config.MATRIX_DRY_RUN:
        try:
            _matrix.send_message(message)
        except Exception as ex:
            log.error('MATRIX SEND ERROR: ' + str(ex))
    else:
        log.warning('MATRIX DRY RUN!')


if __name__ == '__main__':
    can_message = CanMessage.CanMessage()

    highest_ref_id = run(can_message.last_revid)
    log.info("finished, got %s as the latest revid", highest_ref_id)

    if helper.any_dry_run():
        log.info("DRY_RUN, don't save revid")
    else:
        can_message.set_last_revid(highest_ref_id)
        can_message.save()
