import pytest

from imapy.exceptions import SizeParsingError, WrongDateFormat
from imapy.query_builder import Q, check_date, convert_units, quote


def test_convert_units():
    @convert_units
    def dummy_func(self, size):
        return size

    obj = object()  # Dummy object to simulate self

    assert dummy_func(obj, 1000) == 1000
    assert dummy_func(obj, "1000") == 1000
    assert dummy_func(obj, "1KB") == 1000
    assert dummy_func(obj, "1 KB") == 1000
    assert dummy_func(obj, "1 Kilobytes") == 1000
    assert dummy_func(obj, "1MB") == 1000000
    assert dummy_func(obj, "1 Megabytes") == 1000000
    assert dummy_func(obj, "1GB") == 1000000000
    assert dummy_func(obj, "1 Gigabytes") == 1000000000

    with pytest.raises(SizeParsingError):
        dummy_func(obj, "invalid")

def test_check_date():
    @check_date
    def dummy_func(self, date_str):
        return date_str

    obj = object()  # Dummy object to simulate self

    assert dummy_func(obj, "1-Jan-2023") == "1-Jan-2023"
    assert dummy_func(obj, "31-Dec-2023") == "31-Dec-2023"

    with pytest.raises(WrongDateFormat):
        dummy_func(obj, "2023-01-01")

    with pytest.raises(WrongDateFormat):
        dummy_func(obj, "invalid")

def test_quote():
    @quote
    def dummy_func(self, text):
        return text

    obj = object()  # Dummy object to simulate self

    assert dummy_func(obj, "hello") == "hello"
    assert dummy_func(obj, "hello world") == '"hello world"'
    assert dummy_func(obj, '"hello world"') == '"hello world"'

def test_q_sender():
    q = Q()
    result = q.sender("test@example.com")
    assert result.queries == ['FROM', '"test@example.com"']

def test_q_answered():
    q = Q()
    result = q.answered()
    assert result.queries == ['ANSWERED']

def test_q_bcc():
    q = Q()
    result = q.bcc("test@example.com")
    assert result.queries == ['BCC', '"test@example.com"']

def test_q_before():
    q = Q()
    result = q.before("1-Jan-2023")
    assert result.queries == ['BEFORE', '1-Jan-2023']

def test_q_body():
    q = Q()
    result = q.body("test content")
    assert result.queries == ['BODY', '"test content"']

def test_q_cc():
    q = Q()
    result = q.cc("test@example.com")
    assert result.queries == ['CC', '"test@example.com"']

def test_q_deleted():
    q = Q()
    result = q.deleted()
    assert result.queries == ['DELETED']

def test_q_draft():
    q = Q()
    result = q.draft()
    assert result.queries == ['DRAFT']

def test_q_flagged():
    q = Q()
    result = q.flagged()
    assert result.queries == ['FLAGGED']

def test_q_larger():
    q = Q()
    result = q.larger("1MB")
    assert result.queries == ['LARGER', '1000000']

def test_q_on():
    q = Q()
    result = q.on("1-Jan-2023")
    assert result.queries == ['ON', '1-Jan-2023']

def test_q_seen():
    q = Q()
    result = q.seen()
    assert result.queries == ['SEEN']

def test_q_subject():
    q = Q()
    result = q.subject("Test Subject")
    assert result.queries == ['SUBJECT', '"Test Subject"']

def test_q_text():
    q = Q()
    result = q.text("Test content")
    assert result.queries == ['TEXT', '"Test content"']

def test_q_uid():
    q = Q()
    result = q.uid("12345")
    assert result.queries == ['UID', '12345']

def test_q_unanswered():
    q = Q()
    result = q.unanswered()
    assert result.queries == ['UNANSWERED']

def test_q_undeleted():
    q = Q()
    result = q.undeleted()
    assert result.queries == ['UNDELETED']

def test_q_unflagged():
    q = Q()
    result = q.unflagged()
    assert result.queries == ['UNFLAGGED']

def test_q_unseen():
    q = Q()
    result = q.unseen()
    assert result.queries == ['UNSEEN']

def test_q_get_query():
    q = Q()
    q.sender("test@example.com").larger("1MB").subject("Test")
    result = q.get_query()
    assert result == ['FROM', '"test@example.com"', 'LARGER', '1000000', 'SUBJECT', 'Test']

def test_q_non_ascii():
    q = Q()
    q.subject("テスト").sender("test@example.com")
    result = q.get_query()
    assert result == ['CHARSET', 'UTF-8', 'SUBJECT', 'テスト', 'FROM', '"test@example.com"']