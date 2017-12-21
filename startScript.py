import readwiki
import canTweet

for message, last_revid in readwiki.get_changes():
    if canTweet.can_tweet(last_revid):
        print('you can tweet this:', last_revid)
    print(message)