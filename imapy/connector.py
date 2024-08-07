# -*- coding: utf-8 -*-
"""
    imapy.connector
    ~~~~~~~~~~~~~~~

    This module contains alias function which passes connection variables
    to imapy.connect() method.

    :copyright: (c) 2015 by Vladimir Goncharov.
    :license: MIT, see LICENSE for more details.
"""
from . import imap


def connect(**kwargs):
    """Alias function which passes connection variables
    to imapy.connect() method.
    """
    return imap.IMAP(**kwargs)
