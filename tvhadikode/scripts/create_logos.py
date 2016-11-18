# -*- encoding: utf-8 -*-

import os
import sys
import shutil

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

    if shutil.which('convert') is None:
        print('Error: ImageMagick not found ("convert" is not in $PATH)')
        print('Try: sudo apt-get install imagemagick')
        sys.exit(2)

    create_logos()

def create_logos():
    path = AssetResolver().resolve("tvhadikode:static/services/").abspath()
    assert os.path.isdir(path)
    os.chdir(path)

    command = """
    mkdir -p opaque
    convert -size 200x200 gradient:gray50-gray25 -distort SRT -45 opaque/bg.png

    # Some logos need special treatment for dark backgrounds
    convert 11100.png -modulate 200% 11100_opaque.png
    convert 28106.png -modulate 200% 28106_opaque.png
    convert 28721.png -modulate 200% 28721_opaque.png
    convert 12113.png -negate 12113_opaque.png
    convert 24108.png -negate 24108_opaque.png
    convert 24101.png -negate 24101_opaque.png
    convert 12108.png -gamma 1.8 12108_opaque.png

    find -maxdepth 1 -regextype posix-egrep -regex ".*/[0-9]+\.png" | while read fname; do
        echo "> opaque/$(basename $fname)"
        if [ -f "${fname%.png}_opaque.png" ]; then
            in_name="${fname%.png}_opaque.png"
        else
            in_name="$fname"
        fi
        convert -size 200x200 opaque/bg.png -gravity center \\( "$in_name" -resize 160 \\) -composite -colorspace RGB "opaque/$fname"
    done

    rm *_opaque.png opaque/bg.png
    """

    os.system(command)

if __name__ == '__main__':
    main()
