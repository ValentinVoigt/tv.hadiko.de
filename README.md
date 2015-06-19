# tv.hadiko.de README

## Webserver setup

* cd <directory containing this file>
* $VENV/bin/python setup.py develop
* cp development.ini.default development.ini
* adjust development.ini to your needs (see TV-settings)

## Import EPG data

* Create JSON file with ./utils/epg2json.py
* tv_create_tables development.ini
* tv_import_services
* <my-json-file>

## Run webserver

* $VENV/bin/pserve development.ini
