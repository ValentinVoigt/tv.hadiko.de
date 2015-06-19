#!/usr/bin/env python2.7
# -*- coding: utf-8 -*-

import sys
import json

if len(sys.argv) != 2:
	print("Usage: %s <epg.json>" % sys.argv[0])
	sys.exit(1)

epg = json.loads(open(sys.argv[1], 'r').read())
epg_ard = sorted(epg['11100'], key=lambda i: i['start'])

for program in epg_ard[:10]:
	print(program['name'])

