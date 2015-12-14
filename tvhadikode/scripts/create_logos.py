# -*- encoding: utf-8 -*-

import os
import sys

from pyramid.paster import bootstrap
from pyramid.path import AssetResolver

def usage():
    cmd = os.path.basename(sys.argv[0])
    print('usage: %s <config_uri>\n'
          '(example: "%s development.ini")' % (cmd, cmd))
    sys.exit(1)

def main():
    if len(sys.argv) != 2:
        usage()

    bootstrap(sys.argv[1])

    create_logos()

def create_logos():
    path = AssetResolver().resolve("tvhadikode:static/services/").abspath()
    assert os.path.isdir(path)
    os.chdir(path)

    command = """
    mkdir -p opaque
    convert -size 200x200 gradient:white-grey opaque/bg.png
    convert -size 200x200 xc:none -fill gray65 -draw 'circle 130,-300 50,95' opaque/mask_glare.png
    convert -size 200x200 xc:white -draw 'roundrectangle 0,0,200,200,15,15' -negate opaque/mask_rounded.png

    find -maxdepth 1 -regextype posix-egrep -regex ".*/[0-9]+\.png" | while read fname; do
        echo "> opaque/$(basename $fname)"
        convert opaque/bg.png -gravity center "$fname" -geometry 200x200 -composite\
            -compose soft_light opaque/mask_glare.png -composite\
            -compose copy_opacity opaque/mask_rounded.png -composite "opaque/$fname"
    done

    rm opaque/bg.png opaque/mask_glare.png opaque/mask_rounded.png
    """

    os.system(command)
