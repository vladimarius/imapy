# -*- coding: utf-8 -*-
"""
    imapy.query_builder
    ~~~~~~~~~~~~~~~~~~~

    This module contains Q class for constructing queries
    for IMAP search function.
    Note: this class allows to create simple, non-nested
    AND queries. It means that all search conditions specified
    by user should be met in search results. Class doesn't
    currently support joining query conditions with OR and NOT
    statements.

    :copyright: (c) 2015 by Vladimir Goncharov.
    :license: MIT, see LICENSE for more details.
"""
import locale
import re
from datetime import datetime
from datetime import date
from .exceptions import (
    SearchSyntaxNotSupported, WrongDateFormat, SizeParsingError
)

loc = locale.getlocale()


def convert_units(func):
    """Decorator used to convert units (KB, MB, B) from string representation
       to a number.
    """
    def wrapper(*args):
        what = args[1]
        if isinstance(what, int):
            size = what
        else:
            what = what.strip('" \'').lower()
            # Units: B, KB, MB, GB
            # Byte, Bytes, KiloByte, KiloBytes, MegaByte, MegaBytes, GigaByte,
            # Gigabytes
            multiplicator = 1
            if ('giga' in what or 'gb' in what):
                multiplicator = 1000000000
            elif ('mega' in what or 'mb' in what):
                multiplicator = 1000000
            elif ('kilo' in what or 'kb' in what):
                multiplicator = 1000

            # clean string
            what = re.sub(
                (
                    "(((giga)|(mega)|(kilo))(bytes?))|"
                    "(gb)|(mb)|(kb)|(bytes?)|(byte)|(b)"
                ),
                '', what, count=1)
            try:
                what = int(what.strip())
            except ValueError:
                raise SizeParsingError(
                    "Incorrect format used to define message size: {what}."
                    "Please use integer number + one of the following: "
                    "B, Byte, Bytes, Megabyte, Megabytes, Gigabyte, Gigabytes".
                    format(what=args[1])
                )
            size = multiplicator * what
        f = func(*[args[0], size])
        return f
    return wrapper


def check_date(func):
    """Decorator used to check the validity of supplied date."""
    def wrapper(*args, **kwargs):
        date_str = args[-1]
        locale.setlocale(locale.LC_ALL, 'en_US')
        try:
            # 1-Feb-2027
            datetime.strptime(date_str, '%d-%b-%Y')
        except ValueError:
            raise WrongDateFormat(
                "Wrong date format used. Please "
                "use \"en-US\" date format. For example: \"2-Nov-{year}\"".
                format(year=date.today().year))
        locale.setlocale(locale.LC_ALL, loc)
        f = func(*args, **kwargs)
        return f
    return wrapper


def quote(func):
    """Decorator used to quote query parameters."""
    '''It is here because imaplib v2.58 quotes params differently
    under different python versions so running UID search
    under Python 2.7 actually calls:
        UID SEARCH FROM "Test Account"
    under Python 3.4:
        UID SEARCH FROM Test Account
    (no quotes in later example)
    '''
    def wrapper(*args, **kwargs):
        # quote last argument if needed
        last_arg = str(args[-1]).strip('"')
        if " " in last_arg:
            last_arg = '"' + last_arg + '"'
        new_args = args[:-1] + (last_arg,)
        f = func(*new_args, **kwargs)
        return f
    return wrapper


class Q:
    """Class for constructing queries for IMAP search function."""

    def __init__(self, **kwargs):
        self.queries = []
        self.capabilities = None
        self.non_ascii_params = []

    def is_ascii(self, txt):
        """Returns True if string consists of ASCII characters only,
        False otherwise
        """
        try:
            txt.encode('utf-8').decode('ASCII')
        except UnicodeDecodeError:
            return False
        return True

    def get_query(self):
        """Returns list containing queries"""
        non_ascii = self._get_non_ascii_params()
        if len(non_ascii) > 1:
            raise SearchSyntaxNotSupported(
                "Searching using more than 1 parameter "
                "containing non-ascii characters is "
                "not supported")
        # do we have non-ascii characters in query ?
        if len(non_ascii):
            for k, v in enumerate(self.queries[:]):
                if v == non_ascii[0]:
                    del self.queries[k]
                    # put list member to the end of list
                    self.queries.append(self.queries.pop(k - 1))
            if 'CHARSET' not in self.queries:
                self.queries = ['CHARSET', 'UTF-8'] + self.queries

        return self.queries

    def _get_non_ascii_params(self):
        """Checks how much query parameters have non-ascii symbols and
        returns them"""
        if not self.non_ascii_params:
            for q in self.queries:
                if not isinstance(q, int) and not self.is_ascii(q):
                    self.non_ascii_params.append(q)
        return self.non_ascii_params

    @quote
    def sender(self, what):
        """Messages that contain the specified string in FROM field."""
        self.queries += ['FROM', what]
        return self

    def answered(self):
        """Messages with the \Answered flag set."""
        self.queries += ['ANSWERED']
        return self

    @quote
    def bcc(self, what):
        """Messages that contain the specified string in the envelope
         structure's BCC field."""
        self.queries += ['BCC', what]
        return self

    @quote
    def before(self, what):
        """Messages whose internal date (disregarding time and timezone)
         is earlier than the specified date."""
        self.queries += ['BEFORE', what]
        return self

    @quote
    def body(self, what):
        """Messages that contain the specified string in the body of the
         message."""
        self.queries += ['BODY', what]
        return self

    @quote
    def cc(self, what):
        """Messages that contain the specified string in CC field."""
        self.queries += ['CC', what]
        return self

    def deleted(self):
        """Messages with the \Deleted flag set."""
        self.queries += ['DELETED']
        return self

    def draft(self):
        """Messages with the \Draft flag set."""
        self.queries.append('DRAFT')
        return self

    def flagged(self):
        """Messages with the \Flagged flag set."""
        self.queries += ['FLAGGED']
        return self

    @quote
    def header(self, header, what):
        """Messages that have a header with the specified field-name (as
         defined in [RFC-2822]) and that contains the specified string
         in the text of the header"""
        self.queries += ['HEADER', header, what]
        return self

    @quote
    def keyword(self, what):
        """Messages with the specified keyword flag set."""
        self.queries += ['KEYWORD', what]
        return self

    @convert_units
    @quote
    def larger(self, what):
        """Messages with an [RFC-2822] size larger than the specified
         number of octets (1 Octet = 1 Byte)"""
        self.queries += ['LARGER', what]
        return self

    def new(self):
        """Messages that have the \Recent flag set but not the \Seen flag.
         This is functionally equivalent to "(RECENT UNSEEN)"."""
        self.queries += ['NEW']
        return self

    def old(self):
        """Messages that do not have the \Recent flag set.  This is
         functionally equivalent to "NOT RECENT" (as opposed to "NOT
         NEW")."""
        self.queries += ['OLD']
        return self

    @quote
    @check_date
    def on(self, what):
        """Messages whose internal date (disregarding time and timezone)
         is within the specified date."""
        self.queries += ['ON', what]
        return self

    def recent(self):
        """Messages that have the \Recent flag set."""
        self.queries += ['RECENT']
        return self

    def seen(self):
        """Messages that have the \Seen flag set."""
        self.queries += ['SEEN']
        return self

    @quote
    @check_date
    def sent_before(self, what):
        """Messages whose [RFC-2822] Date: header (disregarding time and
         timezone) is earlier than the specified date"""
        self.queries += ['SENTBEFORE', what]
        return self

    @quote
    @check_date
    def sent_on(self, what):
        """Messages whose [RFC-2822] Date: header (disregarding time and
         timezone) is within the specified date."""
        self.queries += ['SENTON', what]
        return self

    @quote
    @check_date
    def sent_since(self, what):
        """Messages whose [RFC-2822] Date: header (disregarding time and
         timezone) is within or later than the specified date."""
        self.queries += ['SENTSINCE', what]
        return self

    @quote
    @check_date
    def since(self, what):
        """Messages whose internal date (disregarding time and timezone)
         is within or later than the specified date."""
        self.queries += ['SINCE', what]
        return self

    @convert_units
    @quote
    def smaller(self, what):
        """Messages with an [RFC-2822] size smaller than the specified
         number of octets (1 Octet = 1 Byte)"""
        self.queries += ['SMALLER', what]
        return self

    @quote
    def subject(self, what):
        """Messages that contain the specified string in the envelope
         structure's SUBJECT field."""
        self.queries += ['SUBJECT', what]
        return self

    @quote
    def text(self, what):
        """Messages that contain the specified string in the header or
         body of the message."""
        self.queries += ['TEXT', what]
        return self

    @quote
    def recipient(self, what):
        """Messages that contain the specified string in the envelope
         structure's TO field."""
        self.queries += ['TO', what]
        return self

    @quote
    def uid(self, what):
        """Messages with unique identifiers corresponding to the specified
         unique identifier set.  Sequence set ranges are permitted."""
        self.queries += ['UID', what]
        return self

    def unanswered(self):
        """Messages that do not have the \Answered flag set."""
        self.queries += ['UNANSWERED']
        return self

    def undeleted(self):
        """Messages that do not have the \Deleted flag set."""
        self.queries += ['UNDELETED']
        return self

    def undraft(self):
        """Messages that do not have the \Draft flag set."""
        self.queries += ['UNDRAFT']
        return self

    def unflagged(self):
        """Messages that do not have the \Flagged flag set."""
        self.queries += ['UNFLAGGED']
        return self

    @quote
    def unkeyword(self, what):
        """Messages that do not have the specified keyword flag set."""
        self.queries += ['UNKEYWORD', what]
        return self

    def unseen(self):
        """Messages that do not have the \Seen flag set."""
        self.queries += ['UNSEEN']
        return self
