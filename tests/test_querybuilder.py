# -*- coding: utf-8 -*-
import pytest

from imapy import (imap, mail_folder, exceptions as e)
from imapy.query_builder import Q


def test_query_builder_size_parsing():
    # Byte
    q = Q()
    q.smaller('3')
    assert '3' in q.queries
    # Byte
    q = Q()
    q.smaller(10)
    assert '10' in q.queries
    # Byte
    q = Q()
    q.smaller('3B')
    assert '3' in q.queries
    q = Q()
    q.larger('4Byte')
    assert '4' in q.queries
    q = Q()
    q.smaller('4 Bytes')
    assert '4' in q.queries
    # Kb
    q = Q()
    q.larger('1kb')
    assert '1000' in q.queries
    q = Q()
    q.smaller('5 kB')
    assert '5000' in q.queries
    q = Q()
    q.larger('5Kilobyte')
    assert '5000' in q.queries
    q = Q()
    q.smaller('5 Kilobytes')
    assert '5000' in q.queries
    # Mb
    q = Q()
    q.larger('1mb')
    assert '1000000' in q.queries
    q = Q()
    q.smaller('5 MB')
    assert '5000000' in q.queries
    q = Q()
    q.larger('5Megabyte')
    assert '5000000' in q.queries
    q = Q()
    q.smaller('5 Megabytes')
    assert '5000000' in q.queries
    # Gb
    q = Q()
    q.larger('1 gb')
    assert '1000000000' in q.queries
    q = Q()
    q.smaller('2 GB')
    assert '2000000000' in q.queries
    q = Q()
    q.larger('3Gigabyte')
    assert '3000000000' in q.queries
    q = Q()
    q.smaller('5 gigabytes')
    assert '5000000000' in q.queries

    # exceptions
    q = Q()
    with pytest.raises(e.SizeParsingError):
        q.smaller('5 boobabytes')
    q = Q()
    with pytest.raises(e.SizeParsingError):
        q.larger('5.5 GB')
    q = Q()
    with pytest.raises(e.SizeParsingError):
        q.smaller('5 GBKB')
