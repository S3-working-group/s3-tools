#!/usr/bin/python
# -*- coding: utf-8 -*-
"""
Build the All Patterns Explained slide deck in Deckset format.
"""

import codecs

import os

from common import make_pathname, make_title, get_patterns


class DecksetWriter(object):
    CONTENT_MARKER = "<!-- INSERT-CONTENT -->"
    GROUP_INDEX_IMAGE = '\n![inline,fit](img/grouped-patterns/group-%s.png)\n\n'

    def __init__(self, args, tmp_folder):
        self.args = args
        self.source = self.args.source
        self.template_path = os.path.join(
            os.path.dirname(self.args.target), 'deckset_template.md')
        self.tmp_folder = tmp_folder
        (self.handbook_group_order, self.s3_patterns, _) = get_patterns(args.patterns)

    def build(self):
        with codecs.open(self.args.target, 'w+', 'utf-8') as self.target:
            with codecs.open(self.template_path, 'r', 'utf-8') as self.template:

                self.copy_template_header()
                # insert title slides
                self._copy_markdown(self.source, 'title.md')
                self.target.write('\n\n---\n\n')

                # insert illustrations for all pattern groups
                if self.args.add_group_illustration:
                    for i, group in enumerate(self.handbook_group_order):
                        self.target.write(self.GROUP_INDEX_IMAGE % str(i + 1))
                        self.target.write('\n\n---\n\n')

                # add all the groups
                for i, group in enumerate(self.handbook_group_order):
                    self._copy_markdown(self.tmp_folder, '%s.md' % make_pathname(group))

                # insert closing slides
                self._copy_markdown(self.source, 'closing.md')
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


    def _copy_markdown(self, folder, name):
        with codecs.open(os.path.join(folder, name), 'r', 'utf-8') as section:
            for line in section:
                self.target.write(line)
        #self.target.write('\n\n---\n\n')

