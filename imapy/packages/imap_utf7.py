# This code in this file is based on a code from an IMAPClient Python library which
# was created and is maintained by Menno Smits <menno@freshfoo.com>.
# and is licensed under BSD license.
#
# The contents of this file has been derived code from the Twisted project
# (http://twistedmatrix.com/). The original author is Jp Calderone.

# Twisted project license follows:

# Permission is hereby granted, free of charge, to any person obtaining
# a copy of this software and associated documentation files (the
# "Software"), to deal in the Software without restriction, including
# without limitation the rights to use, copy, modify, merge, publish,
# distribute, sublicense, and/or sell copies of the Software, and to
# permit persons to whom the Software is furnished to do so, subject to
# the following conditions:
#
# The above copyright notice and this permission notice shall be
# included in all copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND,
# EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF
# MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND
# NONINFRINGEMENT. IN NO EVENT SHALL THE AUTHORS OR COPYRIGHT HOLDERS BE
# LIABLE FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY, WHETHER IN AN ACTION
# OF CONTRACT, TORT OR OTHERWISE, ARISING FROM, OUT OF OR IN CONNECTION
# WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE SOFTWARE.

# This file is from an IMAPClient Python library which
# was created and is maintained by Menno Smits <menno@freshfoo.com>.
# and is licensed under BSD license.
#
# The contents of this file has been derived code from the Twisted project
# (http://twistedmatrix.com/). The original author is Jp Calderone.

# Twisted project license follows:

# Permission is hereby granted, free of charge, to any person obtaining
# a copy of this software and associated documentation files (the
# "Software"), to deal in the Software without restriction, including
# without limitation the rights to use, copy, modify, merge, publish,
# distribute, sublicense, and/or sell copies of the Software, and to
# permit persons to whom the Software is furnished to do so, subject to
# the following conditions:
#
# The above copyright notice and this permission notice shall be
# included in all copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND,
# EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF
# MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND
# NONINFRINGEMENT. IN NO EVENT SHALL THE AUTHORS OR COPYRIGHT HOLDERS BE
# LIABLE FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY, WHETHER IN AN ACTION
# OF CONTRACT, TORT OR OTHERWISE, ARISING FROM, OUT OF OR IN CONNECTION
# WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE SOFTWARE.

from typing import List, Set

PRINTABLE: Set[int] = set(range(0x20, 0x26)) | set(range(0x27, 0x7F))


def encode(s: str) -> bytes:
    """Encode a folder name using IMAP modified UTF-7 encoding.

    Input is str (Python 3 unicode string); output is bytes.
    If non-str input is provided, a TypeError is raised.
    """
    r: List[bytes] = []
    _in: List[str] = []

    def extend_result_if_chars_buffered() -> None:
        if _in:
            r.extend([b"&", modified_utf7("".join(_in)), b"-"])
            del _in[:]

    for c in s:
        if ord(c) in PRINTABLE:
            extend_result_if_chars_buffered()
            r.append(c.encode("latin-1"))
        elif c == "&":
            extend_result_if_chars_buffered()
            r.append(b"&-")
        else:
            _in.append(c)

    extend_result_if_chars_buffered()

    return b"".join(r)


def decode(s: bytes) -> str:
    """Decode a folder name from IMAP modified UTF-7 encoding to unicode.

    Input is bytes; output is always str (Python 3 unicode string).
    If non-bytes input is provided, a TypeError is raised.
    """
    if not isinstance(s, bytes):
        raise TypeError("Input must be bytes")

    r: List[str] = []
    _in: bytearray = bytearray()
    for c in s:
        if c == ord(b"&") and not _in:
            _in.append(c)
        elif c == ord(b"-") and _in:
            if len(_in) == 1:
                r.append("&")
            else:
                r.append(modified_deutf7(_in[1:]))
            _in = bytearray()
        elif _in:
            _in.append(c)
        else:
            r.append(chr(c))
    if _in:
        r.append(modified_deutf7(_in[1:]))
    return "".join(r)


def modified_utf7(s: str) -> bytes:
    s_utf7: bytes = s.encode("utf-7")
    return s_utf7[1:-1].replace(b"/", b",")


def modified_deutf7(s: bytes) -> str:
    s_utf7: bytes = b"+" + s.replace(b",", b"/") + b"-"
    return s_utf7.decode("utf-7")
