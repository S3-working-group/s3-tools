#!/usr/bin/env python

import os
import yaml


def make_pathname(name):
    return name.lower().replace(" ", '-')

def make_title(name):
    return name.title().replace('s3', 'S3')

def create_directory(directory):
    if not os.path.exists(directory):
        os.mkdir(directory)

def read_config(filename):
	stream = open(filename, "r")
	return yaml.load(stream)

def get_patterns(filename):
	"""Return (handbook_group_order, s3_patterns, all_patterns)"""
	data = read_config(filename)
	s3_patterns = data['s3_patterns']
	return (data['handbook_group_order'], s3_patterns, get_all_patterns(s3_patterns))

def get_all_patterns(s3_patterns):
    """Return a sorted list of all patterns."""
    all_patterns = []
    for group in s3_patterns.keys():
        for pattern in s3_patterns[group]:
            all_patterns.append(pattern)
    return sorted(all_patterns)

def increase_headline_level(line):
    line = '#' + line
    if line.endswith('#'):
        line = line + '#'
    return line

class LineWriter(object):

    def __init__(self, target, newlines):
        self.target = target
        if not newlines:
            self.newlines = '\n'
        else:
            self.newlines = newlines
        self.prev_line_empty = False

    def write(self, line):
        """Write line to target, reset blank line counter, output newline if necessary."""
        if self.prev_line_empty:
            self.target.write(self.newlines)
        self.target.write(line.rstrip())
        self.target.write(self.newlines)
        self.prev_line_empty = False

    def mark_empty_line(self):
        self.prev_line_empty = True
