from twython import Twython
import readwiki
import config
import canTweet
from readwiki import WikiChange


def run(api_key, api_secret, token, token_secret, last_revid, max_changes):
    """
    Tweets less than 'max_changes' changes newer than 'last_revid'.
    Returns the new 'last_revid'.
    """
    twitter = Twython(api_key, api_secret, token, token_secret)
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

    changes.reverse()

    if changes_overflow:
        missing_message = "Limit of changes reached. Please see https://{}{}Special:RecentChanges for more information.".format(config.wiki_site, config.wiki_view_path)
        missing_link = WikiChange(changes[-1].revId, missing_message)
        
        changes.insert(0, missing_link)

    for change in changes:
        tweet(twitter, change.message)

    if not changes:
        return last_revid

    return changes[-1].revId


def tweet(twitter, message):
    print("Tweeting:", message)
    if not config.twitter_dry_run:
        twitter.update_status(status=message)
    else:
        print('DRY RUN!')


if __name__ == '__main__':
    cTweet = canTweet.canTweet()

    highestRefId = run(
        config.twitter_api_key,
        config.twitter_api_secret,
        config.twitter_token,
        config.twitter_token_secret,
        cTweet.last_revid,
        config.max_entries)

    cTweet.set_last_revid(highestRefId)
    cTweet.save()
