# -*- encoding: utf-8 -*-

import os
import re
import sys
import json
import transaction
import urllib.request

from datetime import datetime, timedelta

from pyramid.paster import bootstrap

from ..models import DBSession, Program, Service

from .import_services import extract_urls

def usage():
    cmd = os.path.basename(sys.argv[0])
    print('usage: %s <config_uri>\n'
          '(example: "%s development.ini")' % (cmd, cmd))
    sys.exit(1)

def parse_eit_datetime(date, time):
    year, month, day = [int(i) for i in date[:10].split('-')]
    hour, minute, second = [int(i) for i in time.split(':')]
    return datetime(year, month, day, hour, minute, second)

def parse_eit_duration(duration):
    hours, minutes, seconds = [int(i) for i in duration.split(':')]
    return hours * 3600 + minutes * 60 + seconds

def import_epg(url):
    print("Downloading %s..." % url)
    eit = str(urllib.request.urlopen(url).read(), "utf-8", 'replace')
    print("JSON parsing...")
    eit = re.sub(r'"language" : ".*".*",$', r'"language" : "",', eit, flags=re.M)
    eit = re.sub(r'("descr" : "[^"]+")(\s*")', r"\1,\2", eit, flags=re.M)
    eit = re.sub(r'("rating" : "[^"]+")(\s*")', r"\1,\2", eit, flags=re.M)
    eit = re.sub(r'",(\s*)}', r'"\1}', eit, flags=re.M)
    eit = json.loads(eit, strict=False)

    events = {}

    print("Interpreting...")
    for table in eit['EIT_tables']:
        sid = table['sid']
        table_id = table['table_id']
        if not (0x50 <= table_id <= 0x5F or table_id == 0x4E):
            continue
        if not sid in events.keys():
            events[sid] = {}
        for section in table['EIT_sections']:
            for event in section['EIT_events']:
                event_id = event['event_id']
                if not event_id in events[sid].keys():
                    events[sid][event_id] = {
                        'start': parse_eit_datetime(event['start_time day '], event['start_time']),
                        'duration': parse_eit_duration(event['duration']),
                    }
                for descriptor in event['EIT_descriptors']:
                    if 'short_evt' in descriptor.keys():
                        events[sid][event_id]['name'] = descriptor['short_evt']['name']
                        if descriptor['short_evt']['text'] != "":
                            events[sid][event_id]['caption'] = descriptor['short_evt']['text']
                    if 'ext_evt' in descriptor.keys():
                        events[sid][event_id]['descr'] = descriptor['ext_evt']['text']

    print("Importing...")
    n = 0
    for sid, eventsdict in events.items():
        service = Service.get_by(sid=sid)
        if service is not None:
            events = [i for i in eventsdict.values()]
            events.sort(key=lambda i: i['start'])
            programs = []
            for event in events:
                n += 1
                try:
                    program = Program(
                        service=service,
                        start_utc=event['start'],
                        end_utc=event['start'] + timedelta(seconds=event['duration']),
                        duration=event['duration'],
                        name=event['name'],
                        description=event.get('descr'),
                        caption=event.get('caption'),
                    )
                except KeyError:
                    pass
                if len(programs) > 0:
                    if (program.start - programs[-1].end).total_seconds() == 0:
                        program.next = programs[-1]
                    else:
                        print("Warning: there's gap of %s in EIT" % (program.start - programs[-1].end))
                programs.append(program)
            DBSession.add_all(programs)
    print("Imported %i programs!\n" % n)

def main():
    if len(sys.argv) != 2:
        usage()

    data = bootstrap(sys.argv[1])
    urls = extract_urls(data['registry'].settings)

    transaction.begin()
    print("Deleting all programs...")
    DBSession.connection().execute("SET FOREIGN_KEY_CHECKS = 0;")
    DBSession.query(Program).delete()
    DBSession.connection().execute("SET FOREIGN_KEY_CHECKS = 1;")
    print()
    for url in urls:
        import_epg("%s/monitor/EIT.json" % url)
    transaction.commit()
