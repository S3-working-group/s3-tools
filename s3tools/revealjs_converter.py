#!/usr/bin/python
# -*- coding: utf-8 -*-
"""
Convert slides(s) in Deckset Markdown to reveal.js slides.
"""

import re
from string import Template

from common import LineWriter, increase_headline_level


SLIDE_START = """
<section data-markdown>
    <script type="text/template">
"""

SLIDE_END = """
    </script>
</section>
"""

IMG_TEMPLATE = '![](%s)'
IMG_PATTERN = re.compile("\!\[(.*)\]\((.*)\)")
FLOATING_IMAGE = Template(
    """<img class="float-right" src="$url" width="50%" />""")


def convert_to_reveal(source, target):
    lw = LineWriter(target, source.newlines)
    for line in source:
        l = line.strip()
        if not l:
            lw.mark_empty_line()
        elif l == '---':
            lw.write(SLIDE_END)
            lw.write(SLIDE_START)
            # omit line, do not change empty line marker!
            pass
        elif l.startswith('##'):
            lw.write(increase_headline_level(l))
        elif line.lstrip().startswith("!["):
            # fix image
            m = IMG_PATTERN.match(l)
            lw.write(convert_image(m.group(1), m.group(2)))
        else:
            lw.write(line)


def convert_image(format, img_url):
    """Replace floating images with img tag, pass all others."""
    # TODO: convert background images (needs two pass and buffer)
    format = format.lower()
    if 'right' in format:
        return FLOATING_IMAGE.substitute(url=img_url)
    else:
        return '![](%s)' % img_url
