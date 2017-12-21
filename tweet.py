from twython import Twython
import readwiki

def run(api_key, api_secret, token, token_secret, last_revid, max_changes):
    twitter = Twython(api_key, api_secret, token, token_secret)
    changes = list()
    for change in readwiki.get_changes():
        if change[1] <= last_revid:
            break
        changes.append(change[0])
    changes.reverse()
    if len(changes) > max_changes:
        new_changes = list()
        new_changes.append(changes[0])
        new_changes.append("({} changes missing. Please see https://wiki.chaosdorf.de/Special:RecentChanges.)".format(len(changes)-2))
        new_changes.append(changes[-1])
        changes = new_changes
    for change in changes:
        tweet(twitter, change)

def tweet(twitter, change):
    print("Tweeting:", change)
    twitter.update_status(status=change)
