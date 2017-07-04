#!/usr/bin/python
# -*- coding: utf-8 -*-
"""
Build the All Patterns Explained slide deck in reveal.js format.
"""

import codecs
import os

from common import make_pathname, get_patterns
from revealjs_converter import convert_to_reveal

class RevealJsWriter(object):

    CONTENT_MARKER = "<!-- INSERT-CONTENT -->"

    def __init__(self, args):
        self.args = args
        self.source = self.args.source
        self.template_path = os.path.join(
            os.path.dirname(self.args.target), 'template.html')
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
        self._start_section()
        self._start_slide()
        self._copy_markdown(self.source, 'title.md')
        self._end_slide()
        self._end_section()

    def insert_closing(self):
        self._start_section()
        self._start_slide()
        self._copy_markdown(self.source, 'closing.md')
        self._end_slide()
        self._end_section()

    def insert_group(self, group):
        folder = os.path.join(self.source, make_pathname(group))

        self._start_section()

        if os.path.exists(os.path.join(folder, 'index.md')):
            self._start_slide()
            self._copy_markdown(folder, 'index.md')
            self._end_slide()

        for pattern in self.s3_patterns[group]:
            self._start_slide()
            self._copy_markdown(folder, '%s.md' % make_pathname(pattern))
            self._end_slide()

        self._end_section()

    def _start_section(self):
        self.target.write('<section>')

    def _end_section(self):
        self.target.write('</section>')

    def _start_slide(self):
        self.target.write('<section data-markdown>')
        self.target.write('<script type="text/template">')

    def _end_slide(self):
        self.target.write('</script>')
        self.target.write('</section>')

    def _copy_markdown(self, folder, name):
        with codecs.open(os.path.join(folder, name), 'r', 'utf-8') as section:
            convert_to_reveal(section, self.target)
