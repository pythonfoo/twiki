import readwiki
import canTweet

cTweet = canTweet.canTweet()

maxEntries = 10
entriesToCheck = {}

# we need the entries in oldest to newest order, get_changes only delivers in newest to oldest
msgCount = 0
for message, last_revid in readwiki.get_changes():
    entriesToCheck[last_revid] = message
    msgCount += 1
    if msgCount >= maxEntries:
        break

revIds = sorted(entriesToCheck.keys())
for revid in revIds:
    message = entriesToCheck[revid]
    if cTweet.can_tweet(revid):
        print('you can tweet this:', revid)
        print(message)
        cTweet.set_last_revid(revid)

cTweet.save()
