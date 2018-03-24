#!/usr/bin/env python3

from mwclient import Site
import config

site = Site(config.wiki_site, path=config.wiki_api_path)


class WikiChange():
    def __init__(self, _rev_id, _message):
        self.revId = _rev_id
        self.message = _message


def get_changes():
    """ Iterates over the recent changes made to the wiki. """
    _last_revid = -1
    for change in site.recentchanges():
        try:
            revisions = site.revisions([change["revid"]])
            if not revisions:
                continue

            revision = revisions[0]

            if revision["user"] in config.user_name_black_list:
                continue

            link_to_diff = "https://{}{}?type=revision&diff=next&oldid={}".format(
                config.wiki_site,
                config.wiki_view_path,
                change["old_revid"]
            )
            _message = "{} - {} by {}".format(revision["pagetitle"], link_to_diff, revision["user"])
            if revision["comment"] != "":
                _message += " - {}".format(revision["comment"])

            if (len(_message) > 279):
                _message = _message[:275] + '...'

            _last_revid = change["revid"]
        except IndexError as exc:
            _message = "{}: {}".format(type(exc).__name__, exc)

        yield WikiChange(_last_revid, _message)

if __name__ == '__main__':
    for wikiChange in get_changes():
        print(wikiChange.message)
