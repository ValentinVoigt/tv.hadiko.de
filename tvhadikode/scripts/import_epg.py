# -*- encoding: utf-8 -*-

import os
import sys
import json
import transaction

from dateutil.parser import parse

from pyramid.paster import bootstrap

from ..models import DBSession, Program, Service

def usage():
    cmd = os.path.basename(sys.argv[0])
    print('usage: %s <config_uri> <epg.json>\n'
          '(example: "%s development.ini ../epg.json")' % (cmd, cmd))
    sys.exit(1)

def import_epg(epg):
    print("Importing EPG data...")
    n_programs = 0
    n_services = 0
    n_services_total = 0
    for sid, epg_service in epg.items():
        service = Service.get_by(sid=sid)
        n_services_total += 1
        if service is not None:
            n_services += 1
            for program in epg_service:
                DBSession.add(Program(
                    service=service,
                    tid=program['tid'],
                    language=program['language'],
                    start_utc=parse(program['start']),
                    end_utc=parse(program['end']),
                    duration=program['duration'],
                    name=program['name'],
                    description=program['description'],
                ))
                n_programs += 1
    print("Imported %i programs in %i channels (%i skipped)!" % (n_programs, n_services, n_services_total-n_services))

def main():
    if len(sys.argv) != 3:
        usage()

    bootstrap(sys.argv[1])

    transaction.begin()
    import_epg(json.loads(open(sys.argv[2], 'r').read()))
    transaction.commit()
