# -*- encoding: utf-8 -*-

import os
import sys
import json
import urllib2
import transaction

from pyramid.paster import bootstrap
from slugify import slugify

from ..models import DBSession, Base, Service

def usage():
    cmd = os.path.basename(sys.argv[0])
    print('usage: %s <config_uri>\n'
          '(example: "%s development.ini")' % (cmd, cmd))
    sys.exit(1)

def extract_urls(settings):
    for url in settings.get('tv.mumudvb_urls').split("\n"):
        if len(url.strip()) == 0:
            continue
        if url.endswith('/'):
            url = url[:-1]
        yield url

def import_services(urls):
    for url in urls:
        data = json.loads(urllib2.urlopen("%s/monitor/state.json" % url).read())
        for channel in data['channels']:
            DBSession.add(Service(
                sid=channel['service_id'],
                name=channel['name'],
                slug=slugify(channel['name'], to_lower=True, may_length=255),
                multicast_ip="%s:%i" % (channel['ip_multicast'], channel['port_multicast']),
                unicast_url="%s/bysid/%i" % (url, channel['service_id'])
            ))

def main():
    if len(sys.argv) != 2:
        usage()

    data = bootstrap(sys.argv[1])
    urls = extract_urls(data['registry'].settings)

    transaction.begin()
    import_services(urls)
    transaction.commit()
