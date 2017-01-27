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
