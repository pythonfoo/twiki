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

    def is_spam(self):
        """
        various checks to see if the change is/might be spam
        """

        if not self.hasData:
            return False

        if self.change["type"] == "log":
            return True

        return False

    def get_message(self):
        if self.message != '':
            return self.message

        if not self.hasData:
            raise Exception('NO MESSAGE AND NO DATA TO PROCESS!')

        if self.change["type"] == "new":
            # new pages have no diff, just link to the revision
            link = "https://{}{}?oldid={}".format(
                config.wiki_site,
                config.wiki_view_path,
                self.change["revid"],
            )
        else:
            link = "https://{}{}?type=revision&diff=next&oldid={}".format(
                config.wiki_site,
                config.wiki_view_path,
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


def get_filter():
    parts = [
        "!minor" if config.ignore_minor_changes else "",
        "!bot" if config.ignore_bots else ""
    ]

    return '|'.join(part for part in parts if part)


def get_changes():
    """ Iterates over the recent changes made to the wiki. """
    # maybe support more complex queries?
    show = get_filter()

    for change in site.recentchanges(show=show):
        change_obj = WikiChange()

        try:
            revisions = site.revisions([change["revid"]])
            if not revisions:
                continue

            revision = revisions[0]

            if revision["user"] in config.user_name_black_list:
                continue

            change_obj.set_data(revision, change)

            if change_obj.is_spam():
                continue

        except IndexError as exc:
            change_obj.set_message("{}: {}".format(type(exc).__name__, exc))

        yield change_obj


if __name__ == '__main__':
    for wikiChange in get_changes():
        print(wikiChange.get_message())
