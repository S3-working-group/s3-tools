#!/usr/bin/python
# -*- coding: utf-8 -*-
"""
Build the All Patterns Explained slide deck in reveal.js format.
"""

import codecs
import os

from common import make_pathname
from revealjs_converter import Slide

class RevealJsWriter(object):
    """Inject output of content_writer into a template."""

    CONTENT_MARKER = "<!-- INSERT-CONTENT -->"

    def __init__(self, target_path, template_path, content_writer):
        self.target_path = target_path
        self.template_path = template_path
        self.content_writer = content_writer

    def build(self):
        with codecs.open(self.target_path, 'w+', 'utf-8') as self.target:
            with codecs.open(self.template_path, 'r', 'utf-8') as self.template:

                self.copy_template_header()
                self.content_writer.write(self.target)
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


class RevealJSBuilder(object):
    """TODO: untested, needs some more input data."""

    def __init__(self, source, chapter_order,  tmp_folder):
        self.source = source
        self.tmp_folder = tmp_folder
        self.chapter_order = chapter_order

    def write(self, target):
        self.insert_title()
        for group in self.handbook_group_order:
            self.insert_group(group)
            self.insert_closing()
            self.copy_template_footer()

    def insert_title(self):
        self._copy_section(os.path.join(self.source, 'title.md'))

    def insert_closing(self):
        self._copy_section(os.path.join(self.source, 'closing.md'))

    def insert_group(self, group):
        self._copy_section(os.path.join(self.tmp_folder, 
                                         '%s.md' % make_pathname(group)))

    def _start_section(self):
        self.target.write('<section>')

    def _end_section(self):
        self.target.write('</section>')

    def _copy_section(self, markdown_file):
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


