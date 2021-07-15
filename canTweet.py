import json
import logging
log = logging.getLogger(__name__)


class canTweet(object):

    def __init__(self):
        self.last_revid = 0
        self.memoryFile = 'last_revid.json'
        try:
            with open(self.memoryFile) as fHandle:
                self.last_revid = json.load(fHandle)
        except Exception as ex:
            # TODO: empty file or no file at all, get the propper error
            pass
        log.debug("initialized with %s as the last revid", self.last_revid)

    def can_tweet(self, revid):
        return revid > self.last_revid

    def set_last_revid(self, revid):
        self.last_revid = revid

    def save(self):
        log.debug("saving")
        with open(self.memoryFile, 'w') as fHandle:
            json.dump(self.last_revid, fHandle)


if __name__ == '__main__':
    cTweet = canTweet()
    if cTweet.can_tweet(124):
        print('OK')
    cTweet.set_last_revid(124)
    cTweet.save()
