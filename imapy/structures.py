# -*- coding: utf-8 -*-
"""
    imapy.structures
    ~~~~~~~~~~~~~~~~

    This module contains data structures used by Imapy

    :copyright: (c) 2015 by Vladimir Goncharov.
    :license: MIT, see LICENSE for more details.
"""


class CaseInsensitiveDict(dict):
    """Case-insensitive dictionary object"""

    def __init__(self, **kwargs):
        super(CaseInsensitiveDict, self).__init__(self)

    def __setitem__(self, key, value):
        super(CaseInsensitiveDict, self).__setitem__(key.lower(), value)

    def __getitem__(self, key):
        return super(CaseInsensitiveDict, self).__getitem__(key.lower())
