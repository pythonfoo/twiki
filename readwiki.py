#!/usr/bin/env python3

from mwclient import Site
from requests import ReadTimeout

import config
import logging
log = logging.getLogger(__name__)


class ReadWiki:

    class WikiChange:

        def __init__(self):
            self.hasData = False
            self.revision = None
            self.change = None
            self.revId = -1
            self.message = ''

        def set_data(self, _revision, _change):
            self.hasData = True
            self.revision = _revision
            self.change = _change
            self.revId = self.change["revid"]

        def set_message(self, _message):
            self.message = _message

        def can_be_send(self):
            """
            various checks to see if the change might be spam or other unwanted stuff
            """

            # show_params.append("!log") does not work? re-patch
            if self.change["type"] == "log":
                log.debug('exclude log')
                return False

            if not self.hasData:
                log.debug('HAS NO DATA')
                return False

            return True

        def get_message(self):
            if self.message != '':
                return self.message

            if not self.hasData:
                raise Exception('NO MESSAGE AND NO DATA TO PROCESS!')

            if self.change["type"] == "new":
                # new pages have no diff, just link to the revision
                link = "https://{}{}?oldid={}".format(
                    config.WIKI_SITE,
                    config.WIKI_VIEW_PATH,
                    self.change["revid"],
                )
            else:
                link = "https://{}{}?type=revision&diff=next&oldid={}".format(
                    config.WIKI_SITE,
                    config.WIKI_VIEW_PATH,
                    self.change["old_revid"],
                )
            _message = "{} - {} by {}".format(
                self.revision["pagetitle"], link, self.revision["user"]
            )
            if self.revision["comment"] != "":
                _message += " - {}".format(self.revision["comment"])

            if len(_message) > 279:
                _message = _message[:275] + '...'

            self.revId = self.change["revid"]

            self.message = _message
            return self.message


    def __init__(self):
        self.site = None

        try:
            self.site = Site(config.WIKI_SITE, path=config.WIKI_API_PATH)
        except ReadTimeout as ex:
            log.debug("ReadWiki Read TimeOut: %s", ex)

        # all other exceptions may fly
        #except Exception as ex:
        #    log.error('ReadWiki.Site could not be initialized: {}'.format(ex))

    def get_filter(self):
        show_params = list()
        # WARNING:mwclient.client:Unrecognized value for parameter "rcshow": !log
        #show_params.append("!log")

        if config.IGNORE_MINOR_CHANGES:
            show_params.append("!minor")
        if config.IGNORE_BOTS:
            show_params.append("!bot")
        return '|'.join(show_params)


    def get_changes(self):
        """ Iterates over the recent changes made to the wiki. """

        if not  self.site:
            return

        # maybe support more complex queries?
        show = self.get_filter()
        counter_ignored = 0
        counter_blacklist = 0
        counter_revision = 0
        total_changes = 0

        for change in self.site.recentchanges(show=show):
            total_changes += 1
            log.debug("got a change  %s", change)
            change_obj = ReadWiki.WikiChange()

            try:
                revisions = self.site.revisions([change["revid"]])
                if not revisions:
                    counter_revision += 1
                    continue

                revision = revisions[0]

                if revision["user"] in config.USER_NAME_BLACK_LIST:
                    counter_blacklist += 1
                    continue

                change_obj.set_data(revision, change)

                if not change_obj.can_be_send():
                    log.debug('was ignored %s', change_obj.revId)
                    counter_ignored += 1
                    continue

            except IndexError as exc:
                log.error('recentchanges index ERROR: %s', "{}: {}".format(type(exc).__name__, exc))
                change_obj.set_message("{}: {}".format(type(exc).__name__, exc))

            yield change_obj

        log.debug(
            'changes | ignored: %s | blacklisted: %s | no revision: %s | of total %s / %s',
            counter_ignored, counter_blacklist, counter_revision,
            (counter_ignored + counter_blacklist + counter_revision),
            total_changes
        )


if __name__ == '__main__':
    readWiki = ReadWiki()
    for wikiChange in readWiki.get_changes():
        print(wikiChange.get_message())
