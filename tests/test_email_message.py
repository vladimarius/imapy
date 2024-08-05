from email.message import EmailMessage as StdEmailMessage
from unittest.mock import MagicMock, Mock

import pytest

from imapy.email_message import (
    EmailFlag,
    EmailMessage,
    EmailParser,
    EmailRecipients,
    EmailSender,
)
from imapy.exceptions import EmailParsingError


@pytest.fixture
def sample_email_obj():
    email_obj = StdEmailMessage()
    email_obj["Subject"] = "Test Subject"
    email_obj["From"] = "sender@example.com"
    email_obj["To"] = "recipient@example.com"
    email_obj["Date"] = "Sun, 1 Jan 2023 12:00:00 +0000"
    email_obj.set_content("This is a test email body.")
    return email_obj


@pytest.fixture
def mock_email_obj():
    email_obj = MagicMock(spec=StdEmailMessage)
    email_obj.__iter__.return_value = iter([])  # Make it iterable
    email_obj.is_multipart.return_value = False
    email_obj.get_payload.return_value = b"This is a test email body."
    email_obj.get_content.return_value = "This is a test email body."
    email_obj.__getitem__.side_effect = lambda x: {
        "subject": "Test Subject",
        "from": "sender@example.com",
        "to": "recipient@example.com",
        "date": "Thu, 1 Jan 2023 12:00:00 +0000",
    }.get(x.lower())
    return email_obj


@pytest.fixture
def sample_email_message(sample_email_obj):
    return EmailMessage(
        folder="INBOX",
        uid="1234",
        flags=[EmailFlag.SEEN],
        email_obj=sample_email_obj,
        imap_obj=Mock(),
    )


def test_email_message_init(sample_email_message):
    assert sample_email_message.folder == "INBOX"
    assert sample_email_message.uid == "1234"
    assert sample_email_message.flags == [EmailFlag.SEEN]
    assert sample_email_message.subject == "Test Subject"
    assert isinstance(sample_email_message.sender, EmailSender)
    assert isinstance(sample_email_message.recipients, EmailRecipients)


def test_email_message_repr(sample_email_message):
    assert (
        repr(sample_email_message)
        == "sender@example.com: Test Subject (Sun, 01 Jan 2023 12:00:00 +0000)"
    )


def test_email_message_properties(sample_email_message):
    assert sample_email_message.folder == "INBOX"
    assert sample_email_message.uid == "1234"
    assert sample_email_message.flags == [EmailFlag.SEEN]
    assert sample_email_message.subject == "Test Subject"
    assert sample_email_message.date == "Sun, 01 Jan 2023 12:00:00 +0000"


def test_email_message_text(sample_email_message):
    assert len(sample_email_message.text) == 1
    assert sample_email_message.text[0]["text"] == "This is a test email body."


def test_email_message_html(sample_email_message):
    assert sample_email_message.html == []


def test_email_message_attachments(sample_email_message):
    assert sample_email_message.attachments == []


def test_email_message_mark(sample_email_message):
    sample_email_message.mark(EmailFlag.FLAGGED)
    sample_email_message._imap_obj.mark.assert_called_once_with(
        [EmailFlag.FLAGGED], "1234"
    )
    assert EmailFlag.FLAGGED in sample_email_message.flags


def test_email_message_delete(sample_email_message):
    sample_email_message.delete()
    sample_email_message._imap_obj.delete_message.assert_called_once_with(
        "1234", "INBOX"
    )


def test_email_message_copy(sample_email_message):
    sample_email_message.copy("Sent")
    sample_email_message._imap_obj.copy_message.assert_called_once_with(
        "1234", "Sent", sample_email_message
    )


def test_email_message_move(sample_email_message):
    sample_email_message.move("Sent")
    sample_email_message._imap_obj.move_message.assert_called_once_with(
        "1234", "Sent", sample_email_message
    )


def test_email_parser():
    parser = EmailParser()
    contact = parser.parse_email_info("John Doe <john@example.com>")
    assert contact.name == "John Doe"
    assert contact.email == "john@example.com"


def test_email_parser_invalid_format():
    parser = EmailParser()
    with pytest.raises(ValueError):
        parser.parse_email_info("invalid email format")


def test_email_parser_multiple_emails():
    parser = EmailParser()
    contacts = parser.parse_multiple_emails(
        "John Doe <john@example.com>, Jane Doe <jane@example.com>"
    )
    assert len(contacts) == 2
    assert contacts[0].name == "John Doe"
    assert contacts[0].email == "john@example.com"
    assert contacts[1].name == "Jane Doe"
    assert contacts[1].email == "jane@example.com"


def test_email_sender():
    sender = EmailSender("John Doe <john@example.com>")
    assert sender.name == "John Doe"
    assert sender.email == "john@example.com"
    assert str(sender) == "John Doe <john@example.com>"


def test_email_recipients():
    recipients = EmailRecipients(
        "John Doe <john@example.com>, Jane Doe <jane@example.com>"
    )
    assert len(recipients) == 2
    assert recipients[0].name == "John Doe"
    assert recipients[0].email == "john@example.com"
    assert recipients[1].name == "Jane Doe"
    assert recipients[1].email == "jane@example.com"
    assert str(recipients) == "John Doe <john@example.com>, Jane Doe <jane@example.com>"


def test_email_message_parse_multipart(sample_email_obj):
    sample_email_obj.make_alternative()
    sample_email_obj.add_alternative(
        "<p>This is an HTML test email body.</p>", subtype="html"
    )

    email_message = EmailMessage(
        folder="INBOX",
        uid="1234",
        flags=[EmailFlag.SEEN],
        email_obj=sample_email_obj,
        imap_obj=Mock(),
    )

    assert len(email_message.text) == 1
    assert email_message.text[0]["text"] == "This is a test email body."
    assert len(email_message.html) == 1
    assert email_message.html[0] == "<p>This is an HTML test email body.</p>"


def test_email_message_parse_attachment(sample_email_obj):
    attachment_data = b"attachment content"
    sample_email_obj.add_attachment(
        attachment_data,
        maintype="application",
        subtype="octet-stream",
        filename="test.bin",
    )

    email_message = EmailMessage(
        folder="INBOX",
        uid="1234",
        flags=[EmailFlag.SEEN],
        email_obj=sample_email_obj,
        imap_obj=Mock(),
    )

    assert len(email_message.attachments) == 1
    assert email_message.attachments[0].filename == "test.bin"
    assert email_message.attachments[0].data == attachment_data
    assert email_message.attachments[0].content_type == "application/octet-stream"


def test_email_message_cc(sample_email_obj):
    sample_email_obj["CC"] = "cc@example.com"

    email_message = EmailMessage(
        folder="INBOX",
        uid="1234",
        flags=[EmailFlag.SEEN],
        email_obj=sample_email_obj,
        imap_obj=Mock(),
    )

    assert len(email_message.cc) == 1
    assert email_message.cc[0]["cc"] == "cc@example.com"
    assert email_message.cc[0]["cc_email"] == "cc@example.com"


def todo_test_email_message_parse_error():
    invalid_email_obj = Mock()
    invalid_email_obj.is_multipart.side_effect = Exception("Parsing error")

    with pytest.raises(EmailParsingError):
        EmailMessage(
            folder="INBOX",
            uid="1234",
            flags=[EmailFlag.SEEN],
            email_obj=invalid_email_obj,
            imap_obj=Mock(),
        )


def test_email_message_normalize_string(mock_email_obj):
    email_message = EmailMessage(
        folder="INBOX",
        uid="1234",
        flags=[EmailFlag.SEEN],
        email_obj=mock_email_obj,
        imap_obj=Mock(),
    )

    # Test the _normalize_string method directly
    assert email_message._normalize_string("This is a\r\n\ttest") == "This is a test"
    assert email_message._normalize_string("Multiple    spaces") == "Multiple spaces"


def test_email_message_get_links(mock_email_obj):
    email_message = EmailMessage(
        folder="INBOX",
        uid="1234",
        flags=[EmailFlag.SEEN],
        email_obj=mock_email_obj,
        imap_obj=Mock(),
    )

    # Test the _get_links method directly
    text = "Check out https://example.com and http://test.com"
    links = email_message._get_links(text)
    assert set(links) == set(["https://example.com", "http://test.com"])


def test_email_message_body_parsing(mock_email_obj):
    email_message = EmailMessage(
        folder="INBOX",
        uid="1234",
        flags=[EmailFlag.SEEN],
        email_obj=mock_email_obj,
        imap_obj=Mock(),
    )

    assert len(email_message.text) == 1
    assert email_message.text[0]["text"] == "This is a test email body."
    assert email_message.text[0]["text_normalized"] == "This is a test email body."


# Add a new test to verify multipart email handling
def test_email_message_multipart(mock_email_obj):
    mock_email_obj.is_multipart.return_value = True
    mock_email_obj.walk.return_value = [
        MagicMock(
            get_content_type=lambda: "text/plain",
            get_payload=lambda decode=False: b"Plain text content",
        ),
        MagicMock(
            get_content_type=lambda: "text/html",
            get_payload=lambda decode=False: b"<p>HTML content</p>",
        ),
    ]

    email_message = EmailMessage(
        folder="INBOX",
        uid="1234",
        flags=[EmailFlag.SEEN],
        email_obj=mock_email_obj,
        imap_obj=Mock(),
    )

    assert len(email_message.text) == 1
    assert email_message.text[0]["text"] == "Plain text content"
    assert len(email_message.html) == 1
    assert email_message.html[0] == "<p>HTML content</p>"
