# tv.hadiko.de README

## Webserver setup

* cd directory containing this file
* $VENV/bin/python setup.py develop
* cp development.ini.default development.ini
* adjust development.ini to your needs (see TV-settings)

## Import EPG data

* tv_create_tables development.ini
* tv_import_services development.ini
* tv_import_epg development.ini

## Run webserver

* $VENV/bin/pserve development.ini
