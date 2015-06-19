import os
import sys

from pyramid.paster import bootstrap

from ..models import DBSession, Base

def usage():
    cmd = os.path.basename(sys.argv[0])
    print('usage: %s <config_uri>\n'
          '(example: "%s development.ini")' % (cmd, cmd))
    sys.exit(1)

def main():
    if len(sys.argv) != 2:
        usage()

    bootstrap(sys.argv[1])

    Base.metadata.create_all()
