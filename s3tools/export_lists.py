# -*- coding: utf-8 -*-

from __future__ import print_function
from __future__ import unicode_literals

import ConfigParser
import sys
import xml.etree.cElementTree as ET

from common import make_title, read_config


def cmd_list(args):
    formats = {
        'opml': make_opml,
        'd3': make_d3,
        'list': make_list,
        'translation': make_translation_list,
        'translate': translate,
        'markdown': make_md,
    }   
    config = read_config(args.config)

    globals()["handbook_group_order"] = config['chapter_order']
    globals()["s3_patterns"] = config['chapters']
    globals()["all_patterns"] = get_all_patterns(config)
    try:
        formats[args.format.lower()](args)
    except KeyError:
        raise Exception('unknown format', args.format)


def get_all_patterns(config):
    """Return a sorted list of all s3 pattern (stored in config as "chapters")."""
    all_patterns = []
    for group in config['chapters'].keys():
        for pattern in config['chapters'][group]:
            all_patterns.append(pattern)
    print(repr(all_patterns))
    return sorted(all_patterns)


def make_opml(args):
    """Export pattern list as opml."""
    opml = ET.Element("opml", version='1.0')
    head = ET.SubElement(opml, 'head')
    ET.SubElement(head, 'title').text = "S3 Patterns"
    ET.SubElement(head, 'expansionState').text = '0,1'
    body = ET.SubElement(opml, 'body')

    root = ET.SubElement(body, 'outline', text="S3 Patterns")

    for group in handbook_group_order:
        add_group(root, group)

    tree = ET.ElementTree(opml)
    tree.write(sys.stdout, encoding='UTF-8', xml_declaration=True)


def add_group(parent, group):
    group_node = ET.SubElement(parent, 'outline', text=make_title(group))
    for pattern in s3_patterns[group]:
        ET.SubElement(group_node, 'outline', text=make_title(pattern))

def make_key(text):
    return text.replace(" ", "-")


def make_d3(args):
    print("id,value")
    print("S3Patterns,")
    for group in handbook_group_order:
        gt = '.'.join(("S3Patterns", make_key(make_title(group))))
        print(gt+',')
        for pattern in s3_patterns[group]:
            t = '.'.join((gt, make_key(make_title(pattern))))
            print(t+',')

def make_list(args):
    for group in handbook_group_order:
        print(make_title(group))
        for pattern in s3_patterns[group]:
            print("\t", make_title(pattern))

def make_md(args):
    print("## Pattern Groups")
    for group in handbook_group_order:
        print("\n\n### %s\n" % make_title(group))
        for pattern in s3_patterns[group]:
            print("* ", make_title(pattern))

SECTION_GROUPS = "Groups"
SECTION_PATTERNS = "Patterns"

def make_translation_list_(args):
    config = ConfigParser.ConfigParser(delimiters=[':'])
    config.add_section(SECTION_GROUPS)
    config.add_section(SECTION_PATTERNS)

    for group in sorted(handbook_group_order):
        config.set(SECTION_GROUPS, make_key(group), '')

    for pattern in sorted(all_patterns):
        config.set(SECTION_PATTERNS, make_key(pattern), '')

    with open('translations.cfg', 'wb') as configfile:
        config.write(configfile)


def make_translation_list(args):
    
    print("[%s]" % SECTION_GROUPS)
    for group in sorted(handbook_group_order):
        print('%s:' % make_key(group))

    print("\n[%s]" % SECTION_PATTERNS)
    for pattern in all_patterns():
        print('%s:' % make_key(pattern))


def translate(args):
    
    cfg = ConfigParser.ConfigParser()
    cfg.read('translations-%s.cfg' % args.language)

    def trans(item, section):
        key = make_key(item)
        trans = cfg.get(section, key)
        return make_title(key), trans

    def print_(text):
        print(text.encode('UTF8'))
    print("\n# Pattern Groups\n\n")
    for group in sorted(handbook_group_order):
        src, translation = trans(group, SECTION_GROUPS)
        foo = u"# %s -> %s" % (src, translation)
        print_("# %s -> %s" % (src, translation))

        for pattern in s3_patterns[group]:
            src, translation = trans(pattern, SECTION_PATTERNS)
            print (translation)
            foo = u"# %s -> %s" % (src, translation.encode("UTF8"))
            print_("* %s -> %s" % (src, translation))


    