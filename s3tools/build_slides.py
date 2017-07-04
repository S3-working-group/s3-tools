#!/usr/bin/python
# -*- coding: utf-8 -*-
"""
Build "All Patterns Explained" slide deck (either in Deckset format or as reveal.js.
"""

from __future__ import unicode_literals

import codecs
import os
import sys

from common import make_pathname, make_title, create_directory, get_patterns

from build_deckset_slides import DecksetWriter
from build_revealjs_slides import RevealJsWriter
from build_web_content import cmd_convert_to_web

TMP_FOLDER = 'tmp-groups'


def cmd_build_slides(args):
    """Build slides decks"""

    if args.format == 'revealjs':
        build_reveal_slides(args)

    elif args.format == 'deckset':
        build_deckset_slides(args)
    elif args.format == 'wordpress':
        build_wordpress(args)    
    else:
        print("unknown format", args.format)
        sys.exit(1)


def build_deckset_slides(args):
    """Create a source file for a deckset presentation."""
    c = PatternGroupCompiler(args, TMP_FOLDER)
    c.compile_pattern_groups()
    r = DecksetWriter(args, TMP_FOLDER)
    r.build()


def build_reveal_slides(args):
    """
    Build reveal.js presentation. <target> is a file inside the reveal.js folder, 
    template.html is expected in the same folder.
    """
    c = PatternGroupCompiler(args, TMP_FOLDER)
    c.compile_pattern_groups()
    r = RevealJsWriter(args, TMP_FOLDER)
    r.build()


def build_wordpress(args):
    c = PatternGroupCompiler(args, TMP_FOLDER)
    c.compile_pattern_groups()
    cmd_convert_to_web(args, TMP_FOLDER)


def cmd_create_source_files_for_slides(args):
    """Create dummy source files for slides. If file or folder exists, don't touch it."""

    s3_patterns = get_patterns(args.patterns)[1]

    create_directory(args.source)

    def make_file(root, filename_root, title_root, markup='#'):
        """Create file if it does not exist."""
        filename = os.path.join(root, '%s.md' % make_pathname(filename_root))
        if not os.path.exists(filename):
            with codecs.open(filename, 'w+', 'utf-8') as fp:
                fp.write('%s %s\n\n' % (markup, make_title(title_root)))
        else:
            if args.verbose:
                print "skipped %s" % title_root

    for group in s3_patterns.keys():
        # create group dir
        group_root = os.path.join(args.source, make_pathname(group))
        create_directory(group_root)
        # create group index file
        make_file(group_root, "index", group, '#')
        # create individual patterns (add pattern name as headline)
        for pattern in s3_patterns[group]:
            make_file(group_root, pattern, pattern, '##')


class PatternGroupCompiler():
    
    PATTERN_NUMBER = ' Pattern %s.%s:'
    
    GROUP_INDEX_FILENAME = 'index.md'
    GROUP_INDEX_IMAGE = '\n![inline,fit](img/grouped-patterns/group-%s.png)\n\n'    
    GROUP_TITLE_IMAGE = '\n![inline,fit](img/pattern-group-headers/header-group-%s.png)\n\n'

    def __init__(self, args, tmp_folder):
        self.args = args
        self.source = self.args.source
        self.template_path = os.path.join(
            os.path.dirname(self.args.target), 'deckset_template.md')
        self.temp_folder = tmp_folder
        (self.handbook_group_order, self.s3_patterns, _) = get_patterns(args.patterns)
        self.INSERT_GROUP_TEXT_TITLE_SLIDE = False
        self.INSERT_GROUP_IMG_TITLE_SLIDE = False
        if self.args.group_title == 'img':
            self.INSERT_GROUP_IMG_TITLE_SLIDE = True
        elif self.args.group_title == 'text':
            self.INSERT_GROUP_TEXT_TITLE_SLIDE = True
        elif self.args.group_title == 'both':
            self.INSERT_GROUP_IMG_TITLE_SLIDE = True
            self.INSERT_GROUP_TEXT_TITLE_SLIDE = True


    def compile_pattern_groups(self):
        """Compile one temp file for each pattern group."""
        
        if not os.path.exists(self.temp_folder):
            os.makedirs(self.temp_folder)

        for i, group in enumerate(self.handbook_group_order):
            with codecs.open(os.path.join(self.temp_folder, '%s.md' % make_pathname(group)), 'w+', 'utf-8') as self.target:
                self._insert_group(group, i + 1)


    def _insert_group(self, group, group_index):
        """Build group index and pattern slides."""
        folder = os.path.join(self.source, make_pathname(group))

        # group title and index slides
        if self.INSERT_GROUP_TEXT_TITLE_SLIDE:
            self.target.write('\n# %s. %s \n\n---\n\n' % (group_index, make_title(group)))
        if self.INSERT_GROUP_IMG_TITLE_SLIDE:
            self.target.write(self.GROUP_TITLE_IMAGE % str(group_index))
            self.target.write('\n\n---\n\n')
        if self.args.add_group_illustration:
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
