# tv.hadiko.de README

## Import EPG data

* Create JSON file with ./utils/epg2json.py
* Use initialize_tv.hadiko.de_db <json> to import database

## Webserver setup

* cd <directory containing this file>
* $VENV/bin/python setup.py develop
* $VENV/bin/initialize_tv.hadiko.de_db development.ini
* $VENV/bin/pserve development.ini
