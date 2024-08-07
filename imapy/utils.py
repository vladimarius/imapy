# -*- coding: utf-8 -*-
"""
    imapy.utils
    ~~~~~~~~~~~

    This module contains utilities used mostly to
    make imapy work correctly in Python 2 and 3

    :copyright: (c) 2015 by Vladimir Goncharov.
    :license: MIT, see LICENSE for more details.
"""
from .packages import imap_utf7


def utf7_to_unicode(text):
    """Convert string in utf-7 to unicode"""
    return imap_utf7.decode(text)


def str_to_utf7(text):
    """Convert string to UTF-7"""
    return imap_utf7.encode(text)


def u(text):
    """Convert to Unicode"""
    return text


def to_unescaped_str(text):
    """Convert escaped string to string"""
    return text.encode("utf-8").decode("unicode_escape")


def b_to_str(text):
    """Convert to string"""
    return text.decode("utf-8", "ignore")


def str_to_b(text):
    """Convert string to bytes"""
    return text.encode("utf-8")
