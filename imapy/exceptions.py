# -*- coding: utf-8 -*-
"""
    imapy.exceptions
    ~~~~~~~~~~~~~~~~

    This module contains imapy exceptions.

    :copyright: (c) 2015 by Vladimir Goncharov.
    :license: MIT, see LICENSE for more details.
"""


class ImapyException(Exception):
    def __init__(self, *args, **kwargs):
        super(ImapyException, self).__init__(*args, **kwargs)


"""
Imapy Exceptions
"""


class ImapyLoggedOut(ImapyException):
    """Raised when user tries to communicate with server after log out"""


class WrongDateFormat(ImapyException):
    """Raised when wrong date format is used in imap search function"""


class UnknownEmailMessageType(ImapyException):
    """Raised when user tries to use email message of unknown type"""


class InvalidFolderName(ImapyException):
    """Raised when user tries to create folder name containing invalid
    characters"""


class InvalidSearchQuery(ImapyException):
    """Raised when user tries to search for email messages without using
    the query_builder Q class"""


class SearchSyntaxNotSupported(ImapyException):
    """Raised when user tries to search for email messages using more
    than 1 parameter containing non-ascii characters"""


class TagNotSupported(ImapyException):
    """Raised when user tries to mark email message with non-standard tag"""


class EmailParsingError(ImapyException):
    """Raised when we cannot correctly parse email field"""


class NonexistentFolderError(ImapyException):
    """Raised when selecting non-existing email folder"""


"""
MailFolder Exceptions
"""


class EmailFolderParsingError(ImapyException):
    """Raised when MailFolder cannot parse folder details"""


"""
QueryBuilder Exceptions
"""


class SizeParsingError(ImapyException):
    """Raised when email size is specified in an unknown format"""


"""
Third-party Exceptions
"""


class ConnectionRefused(ImapyException):
    """Connection refused"""


class InvalidHost(ImapyException):
    """Invalid host"""
