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
    PATTERN_NUMBER = ' Pattern %s.%s:'
    GROUP_TITLE_IMAGE = '\n![inline,fit](img/pattern-group-headers/header-group-%s.png)\n\n'
    GROUP_INDEX_IMAGE = '\n![inline,fit](img/grouped-patterns/group-%s.png)\n\n'
    GROUP_INDEX_FILENAME = 'index.md'

    # configuration
    INSERT_GROUP_TEXT_TITLE_SLIDE = False
    INSERT_GROUP_IMG_TITLE_SLIDE = True
    INSERT_ILLUSTRATIONS_FOR_PATTERN_GROUPS = False

    def __init__(self, args):
        self.args = args
        self.source = self.args.source
        self.template_path = os.path.join(
            os.path.dirname(self.args.target), 'deckset_template.md')
        (self.handbook_group_order, self.s3_patterns, _) = get_patterns(args.patterns)
        

    def build(self):
        with codecs.open(self.args.target, 'w+', 'utf-8') as self.target:
            with codecs.open(self.template_path, 'r', 'utf-8') as self.template:

                self.copy_template_header()
                # insert title slides
                self._copy_markdown(self.source, 'title.md')

                # insert illustrations for all pattern groups
                if self.INSERT_ILLUSTRATIONS_FOR_PATTERN_GROUPS:
                    for i, group in enumerate(self.handbook_group_order):
                        self.target.write(self.GROUP_INDEX_IMAGE % str(i + 1))
                        self.target.write('\n\n---\n\n')

                # add all the groups
                for i, group in enumerate(self.handbook_group_order):
                    self.insert_group(group, i + 1)

                # insert closing slides
                self._copy_markdown(self.source, 'closing.md')
                self.copy_template_footer()

    def build_web_markdown(self):
        """Build indivdual markdown files for web publishing."""
        # add all the groups
        for i, group in enumerate(self.handbook_group_order):
            with codecs.open(os.path.join('web', '%s.md' % group), 'w+', 'utf-8') as self.target:
                self.insert_group(group, i + 1, False)


    def copy_template_header(self):
        for line in self.template:
            if line.strip() == self.CONTENT_MARKER:
                break
            else:
                self.target.write(line)

    def copy_template_footer(self):
        for line in self.template:
            self.target.write(line)

    def insert_group(self, group, group_index, write_title_slide=True):
        """Build group index and pattern slides."""
        folder = os.path.join(self.source, make_pathname(group))

        # group title and index slides
        if write_title_slide:
            if self.INSERT_GROUP_TEXT_TITLE_SLIDE:
                self.target.write('\n# %s. %s \n\n---\n\n' % (group_index, make_title(group)))
            if self.INSERT_GROUP_IMG_TITLE_SLIDE:
                self.target.write(self.GROUP_TITLE_IMAGE % str(group_index))
                self.target.write('\n\n---\n\n')
        if self.INSERT_ILLUSTRATIONS_FOR_PATTERN_GROUPS:
            self.target.write(self.GROUP_INDEX_IMAGE % str(group_index))
            self.target.write('\n\n---\n\n')

        # insert group preamble if present
        if os.path.exists(os.path.join(folder, self.GROUP_INDEX_FILENAME)):
            self._copy_markdown(folder, self.GROUP_INDEX_FILENAME)

        # add individual patterns
        for pattern_index, pattern in enumerate(self.s3_patterns[group]):
            self._copy_markdown(folder, '%s.md' % make_pathname(
                pattern), self.PATTERN_NUMBER % (group_index, pattern_index + 1))


    def _copy_markdown(self, folder, name, headline_prefix=''):
        with codecs.open(os.path.join(folder, name), 'r', 'utf-8') as section:
            if headline_prefix:
                # insert patter number into first headline of file
                line = section.next()
                try:
                    pos = line.index('# ')
                except ValueError():
                    raise Exception(
                        "no headline in first line of %s" % os.path.join(folder, name))
                self.target.write(
                    ''.join((line[:pos + 1], headline_prefix, line[pos + 1:])))
            for line in section:
                self.target.write(line)
        self.target.write('\n\n---\n\n')

