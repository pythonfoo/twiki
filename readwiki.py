#!/usr/bin/env python3

from mwclient import Site
import config

site = Site(config.wiki_site, path=config.wiki_api_path)


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

    def get_message(self):
        if self.message != '':
            return self.message

        if not self.hasData:
            raise Exception('NO MESSAGE AND NO DATA TO PROCESS!')

        link_to_diff = "https://{}{}?type=revision&diff=next&oldid={}".format(
            config.wiki_site,
            config.wiki_view_path,
            self.change["old_revid"]
        )
        _message = "{} - {} by {}".format(self.revision["pagetitle"], link_to_diff, self.revision["user"])
        if self.revision["comment"] != "":
            _message += " - {}".format(self.revision["comment"])

        if len(_message) > 279:
            _message = _message[:275] + '...'

        self.revId = self.change["revid"]

        self.message = _message
        return self.message


def get_changes():
    """ Iterates over the recent changes made to the wiki. """

    for change in site.recentchanges():
        change_obj = WikiChange()

        try:
            revisions = site.revisions([change["revid"]])
            if not revisions:
                continue

            revision = revisions[0]

            if revision["user"] in config.user_name_black_list:
                continue

            change_obj.set_data(revision, change)

        except IndexError as exc:
            change_obj.set_message("{}: {}".format(type(exc).__name__, exc))

        yield change_obj


if __name__ == '__main__':
    for wikiChange in get_changes():
        print(wikiChange.get_message())
