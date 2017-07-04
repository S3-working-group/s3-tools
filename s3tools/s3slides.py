#!/usr/bin/env python

import argparse
import os
import shutil
import re
import os.path
import sys

from build_slides import cmd_build_slides, cmd_create_source_files_for_slides


def add_parser_build(subparsers):
    sp = subparsers.add_parser('build',
                               help="Build s3 patterns slide deck.")
    sp.add_argument('format', help="presentation format, either 'deckset', 'wordpress' or 'revealjs'.")
    sp.add_argument('patterns', help='yaml file with pattern structure')
    sp.add_argument('source', help='Directory with source files.')
    sp.add_argument('target', help='Target file (for reveal.js and deckset) or folder (for wordpress).')
    sp.add_argument('--footer', help='The footer to add to each group for wordpress output')
    sp.add_argument('--group-title', default='none',
        help='What kind of title slide to add to each pattern groups: text, img, both, none (default)')
    sp.add_argument('--add-group-illustration', action='store_true',
        help='What kind of title slide to add to each pattern groups: text, img, both, none (default)')
    sp.set_defaults(func=cmd_build_slides)
    

def add_parser_skeleton(subparsers):
    sp = subparsers.add_parser('skeleton',
                               help="Create skeleton directories and files for slides.")
    sp.add_argument('patterns', help='yaml file with pattern structure')
    sp.add_argument('source', help='Directory with source files.')
    sp.set_defaults(func=cmd_create_source_files_for_slides)


def main():
    # setup argparse
    parser = argparse.ArgumentParser(
        description='Tools for s3 slide decks with all patterns')
    parser.add_argument('--verbose', '-v', action='count')
    subparsers = parser.add_subparsers()
    add_parser_build(subparsers)
    add_parser_skeleton(subparsers)

    args = parser.parse_args()
    args.func(args)


if __name__ == "__main__":
	main()
