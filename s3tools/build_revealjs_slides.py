#!/usr/bin/python
# -*- coding: utf-8 -*-
"""
Build the All Patterns Explained slide deck in reveal.js format.
"""

import codecs
import os
import re
from string import Template

from common import make_pathname, get_patterns, LineWrite

#from revealjs_converter import convert_to_reveal

class RevealJsWriter(object):

    CONTENT_MARKER = "<!-- INSERT-CONTENT -->"

    def __init__(self, args, tmp_folder):
        self.args = args
        self.source = self.args.source
        self.template_path = os.path.join(
            os.path.dirname(self.args.target), 'template.html')
        self.tmp_folder = tmp_folder
        (self.handbook_group_order, self.s3_patterns, _) = get_patterns(args.patterns)

    def build(self):
        with codecs.open(self.args.target, 'w+', 'utf-8') as self.target:
            with codecs.open(self.template_path, 'r', 'utf-8') as self.template:

                self.copy_template_header()
                self.insert_title()
                for group in self.handbook_group_order:
                    self.insert_group(group)
                self.insert_closing()
                self.copy_template_footer()

    def copy_template_header(self):
        for line in self.template:
            if line.strip() == self.CONTENT_MARKER:
                break
            else:
                self.target.write(line)

    def copy_template_footer(self):
        for line in self.template:
            self.target.write(line)

    def insert_title(self):
        self._copy_markdown(os.path.join(self.source, 'title.md'))

    def insert_closing(self):
        self._copy_markdown(os.path.join(self.source, 'closing.md'))

    def insert_group(self, group):
        self._copy_markdown(os.path.join(self.tmp_folder, 
                                         '%s.md' % make_pathname(group)))

    def _start_section(self):
        self.target.write('<section>')

    def _end_section(self):
        self.target.write('</section>')

    def _copy_markdown(self, markdown_file):
        print(markdown_file)

        self._start_section()
        with codecs.open(markdown_file, 'r', 'utf-8') as source:
            while True:
                slide = Slide()
                try:
                    slide.read(source)
                except Slide.EndOfFile:
                    break
                finally:
                    slide.render(self.target)
        self._end_section()


class Slide(object):

    IMG_TEMPLATE = '![](%s)'
    IMG_PATTERN = re.compile("\!\[(.*)\]\((.*)\)")
    FLOATING_IMAGE = Template(
        """<img class="float-right" src="$url" width="50%" />""")

    class EndOfFile(Exception):
        pass

    def __init__(self):
        self.headline = None
        self.background_img = None
        self.content = []
        self.floating_image = None
        self.is_empty = True

    def read(self, source):
        """Read source until end of slide or end of file."""
        for line in source:
            self.is_empty = False
            l = line.strip()
            if l.strip() == '---':
                return
            elif l.startswith('#') and not self.headline:
                self.headline = l
            elif l.startswith("![") and l.endswith(')'):
                #process image
                self.process_image(l)
            else:
                self.content.append(line)
        else:
            raise self.EndOfFile()

    def process_image(self, line):
        """Identify background and floating images, add all others to content.."""
        # TODO: convert background images (needs two pass and buffer)
        m = self.IMG_PATTERN.match(line)
        format, image_url = (m.group(1).lower(), m.group(2))
        if 'right' in format:
            self.floating_image = image_url
        elif format == 'fit':
            self.background_img = image_url
        else:
            self.content.append('![](%s)' % image_url)

    def slide_start(self, lw):
        if self.background_img:
            lw.write('<section data-markdown data-background-image="%s">' % self.background_img)
        else: 
            lw.write('<section data-markdown>')
        lw.write('    <script type="text/template">')

    def slide_end(self, lw):
        lw.write('    </script>')
        lw.write('</section>')
            
    def render(self, target):
        if self.is_empty:
            return
        lw = LineWriter(target, None)

        self.slide_start(lw)  
        if self.headline:
            lw.write(self.headline)
            lw.write('')

        if self.floating_image:
            #lw.write('<div class="float-right">')
            #lw.write('</div>')            
            #lw.write('<div>')
            for line in self.content:
                lw.write(line)
            #lw.write('</div>')
            lw.write(self.FLOATING_IMAGE.substitute(url=self.floating_image))


        else:
            for line in self.content:
                lw.write(line)
        self.slide_end(lw)
