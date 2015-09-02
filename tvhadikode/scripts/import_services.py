# -*- encoding: utf-8 -*-

import os
import sys
import json
import urllib.request
import transaction

from sqlalchemy.exc import IntegrityError
from pyramid.paster import bootstrap
from slugify import slugify

from ..models import DBSession, Service

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
    print("Adding services...")
    sids = [s.sid for s in DBSession.query(Service).all()]

    for url in urls:
        print("%s/monitor/state.json" % url)
        data = json.loads(str(urllib.request.urlopen("%s/monitor/state.json" % url).read(), "utf-8"))
        for channel in data['channels']:
            if not channel['service_id'] in sids:
                DBSession.add(Service(
                    sid=channel['service_id'],
                    name=channel['name'],
                    slug=slugify(channel['name'], to_lower=True, may_length=255),
                    multicast_ip_port="%s:%i" % (channel['ip_multicast'], channel['port_multicast']),
                    unicast_port=int(channel['unicast_port'])
                ))
                print ("* %s" % channel['name'])
            else:
                print("%s: already exists" % channel['name'])

def main():
    if len(sys.argv) != 2:
        usage()

    data = bootstrap(sys.argv[1])
    urls = extract_urls(data['registry'].settings)

    transaction.begin()
    import_services(urls)
    transaction.commit()
