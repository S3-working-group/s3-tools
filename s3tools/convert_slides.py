#!/usr/bin/python
# -*- coding: utf-8 -*-
"""
Convert slides from Deckset to reveal.js, or from Deckset to Markdown for web (e.g. Wordpress with Jetpack.
"""

from build_revealjs_slides import RevealJsWriter
from revealjs_converter import RevealJsHtmlConverter


def cmd_convert_slides(args):
    """Converta file in deckset format to a reveal.js presentation (html)."""

    cw = RevealJsHtmlConverter(args.source)
    rw = RevealJsWriter(args.target, args.template, cw)
    rw.build()
