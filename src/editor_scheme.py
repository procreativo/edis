# -*- coding: utf-8 -*-
# EDIS - a simple cross-platform IDE for C
#
# This file is part of Edis
# Copyright 2014-2015 - Gabriel Acosta <acostadariogabriel at gmail>
# License: GPLv3 (see http://www.gnu.org/licenses/gpl.html)

# Edis Scheme
EDIS_DARK_SCHEME = {
    'BackgroundEditor': '#272822',
    'Color': '#F8F8F2',
    'Keyword': '#66D9EF',
    'KeywordSet2': '#8d9fc2',
    'Comment': '#75715E',
    'CommentLine': '#75715E',
    'Number': '#AE81FF',
    'DoubleQuotedString': '#E6DB74',
    'SingleQuotedString': '#B8DB74',
    'PreProcessor': '#D50550',
    'Operator': '#FFFFFF',
    'MatchedBraceFore': '#FFFFFF',
    'MatchedBraceBack': '#044888',
    'UnmatchedBraceFore': '#FFFFFF',
    'UnmatchedBraceBack': '#FF0000',
    'Margin': '#333333',
    'CaretLineBack': '#474a3e',
    'CaretLineFore': '#FFFFFF',
    'CaretLineAlpha': 30,
    'SidebarBack': '#272822',
    'SidebarFore': "#8F908A",
    'FoldMarginBack': '#272822',
    'FoldMarginFore': '#272822',
    'FoldMarkerFore': '#FFFFFF',
    'FoldMarkerBack': '#000000',
    'error': '#DF3E3E',
    'UnclosedString': '#FF0000'
    }

# Based on Komodo
EDIS_WHITE_SCHEME = {
    'BackgroundEditor': '#FFFFFF',
    'Color': '#000000',
    'Keyword': '#333399',
    'Comment': '#666666',
    'CommentLine': '#BEBEE6',
    'Number': '#8B0000',
    'DoubleQuotedString': '#996633',
    'SingleQuotedString': '#E0A000',
    'PreProcessor': '#696969',
    'Operator': '#781F87',
    'MatchedBraceFore': '#FFFFFF',
    'MatchedBraceBack': '#333399',
    'UnmatchedBraceFore': '#FFFFFF',
    'UnmatchedBraceBack': '#FF0000',
    'Margin': '#C2C2C2',
    'CaretLineBack': '#DEDEDE',
    'CaretLineFore': '#000000',
    'CaretLineAlpha': 50,
    'SidebarBack': '#F5F5F5',
    'SidebarFore': '#C2C2C2',
    'FoldMarginBack': '#F7F7F7',
    'FoldMarginFore': '#F7F7F7',
    'FoldMarkerFore': '#F7F7F7',
    'FoldMarkerBack': '#C2C2C2',
    'error': '#DF3E3E'
    }

SCHEME = {'dark': EDIS_DARK_SCHEME, 'white': EDIS_WHITE_SCHEME}


def get_scheme(key):
    return SCHEME.get(key, None)