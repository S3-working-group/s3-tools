#!/usr/bin/env python

import argparse
import os
import shutil
import re
import os.path
import sys

from export_lists import cmd_list
from slides import cmd_slides


def add_parser_slides(subparsers):
    slides = subparsers.add_parser('slides',
                                   help="Build slide deck.")
    slides.add_argument('--skeleton', action='store_true',
                        help='Build skeleton directories and files for slides.')
    slides.add_argument('--reveal', action='store_true',
                        help='Build reveal.js presentation.')
    slides.add_argument('--deckset', action='store_true',
                        help='Build deckset presentation.')
    slides.add_argument('--target', '-t',
                        help='Target file (for reveal.js and deckset builds.')
    slides.add_argument('patterns', 
                     help='yaml file with pattern structure')
    slides.add_argument('source', 
                        help='Directory for source files.')
    slides.set_defaults(func=cmd_slides)


def add_parser_list(subparsers):
    lst = subparsers.add_parser('list',
                                help="Export pattern list in various formats.")

    lst.add_argument('format', nargs='?', default='list',
                        help='format: list, opml, d3, translation, markdown.')
    lst.add_argument('--language', default='de',
                        help="Language suffix for translation files, e.g. 'de', 'fr'.")
    lst.add_argument('patterns', 
                     help='yaml file with pattern structure')
    lst.set_defaults(func=cmd_list)

def main():
    # setup argparse
    parser = argparse.ArgumentParser(
        description='build files for s3 patterns website and handbooks')

    parser.add_argument('--verbose', '-v', action='count')
    subparsers = parser.add_subparsers()

    add_parser_slides(subparsers)
    add_parser_list(subparsers)

    args = parser.parse_args()
    args.func(args)


if __name__ == "__main__":
	main()
