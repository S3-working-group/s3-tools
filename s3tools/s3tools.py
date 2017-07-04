#!/usr/bin/env python

import argparse

from export_lists import cmd_list

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

    add_parser_list(subparsers)

    args = parser.parse_args()
    args.func(args)


if __name__ == "__main__":
	main()
