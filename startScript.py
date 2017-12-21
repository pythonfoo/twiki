import readwiki
import canTweet

cTweet = canTweet.canTweet()

for message, last_revid in readwiki.get_changes():
    if cTweet.can_tweet(last_revid):
        print('you can tweet this:', last_revid)
        cTweet.set_last_revid(last_revid)
    print(message)

cTweet.save()