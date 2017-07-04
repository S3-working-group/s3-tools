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


def cmd_build_slides(args):
    """Build slides decks"""

    if args.format == 'revealjs':
        build_reveal_slides(args)

    elif args.format == 'deckset':
        build_deckset_slides(args)
    else:
        print("unknown format", args.format)
        sys.exit(1)

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


def build_deckset_slides(args):
    """Create a source file for a deckset presentation."""
    r = DecksetWriter(args)
    r.build()
    r.build_web_markdown()



def build_reveal_slides(args):
    """
    Build reveal.js presentation. <target> is a file inside the reveal.js folder, 
    template.html is expected in the same folder.
    """
    r = RevealJsWriter(args)
    r.build()


