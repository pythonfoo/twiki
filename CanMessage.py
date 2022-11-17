import json
import logging
log = logging.getLogger(__name__)


class CanMessage(object):

    def __init__(self):
        self.last_revid = 0
        self.memory_file = 'last_revid.json'
        try:
            with open(self.memory_file) as file_handle:
                self.last_revid = json.load(file_handle)
        except Exception as ex:
            # TODO: empty file or no file at all, get the proper error
            pass
        log.debug("initialized with %s as the last revid", self.last_revid)

    def can_send(self, revid):
        return revid > self.last_revid

    def set_last_revid(self, revid):
        self.last_revid = revid

    def save(self):
        log.debug("saving")
        with open(self.memory_file, 'w') as fHandle:
            json.dump(self.last_revid, fHandle)


if __name__ == '__main__':
    can_message = CanMessage()
    if can_message.can_send(124):
        print('OK')
    can_message.set_last_revid(124)
    can_message.save()
