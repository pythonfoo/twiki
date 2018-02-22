#!/usr/bin/env python3

from mwclient import Site

site = Site("wiki.chaosdorf.de", path="/")

def get_changes():
    """ Iterates over the recent changes made to the wiki. """
    last_revid = -1
    for change in site.recentchanges():
        try:
            revision = site.revisions([change["revid"]])[0]
            link_to_diff = "https://wiki.chaosdorf.de/?type=revision&diff=prev&oldid={}".format(change["old_revid"])
            message = "{} - {} by {}".format(revision["pagetitle"], link_to_diff, revision["user"])
            if revision["comment"] != "":
                message += " - {}".format(revision["comment"])

            last_revid = change["revid"]
        except IndexError as exc:
            message = "{}: {}".format(type(exc).__name__, exc)
        yield message, last_revid

if __name__ == '__main__':
    for message, last_revid in get_changes():
        print(message)
