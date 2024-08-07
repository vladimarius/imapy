from email.mime.text import MIMEText
from unittest.mock import Mock, patch

import pytest

from imapy.email_message import EmailFlag, EmailMessage
from imapy.exceptions import (
    ConnectionRefused,
    ImapyLoggedOut,
    InvalidHost,
    NonexistentFolderError,
    UnknownEmailMessageType,
)
from imapy.imap import IMAP
from imapy.mail_folder import MailFolder
from imapy.query_builder import Q


@pytest.fixture
def mock_imap():
    with patch("imapy.imap.IMAP.connect"), patch("imapy.imap.IMAP._update_folder_info"):
        mock_imap = IMAP(
            host="imap.example.com", username="user", password="pass", ssl=True
        )

        # Set up the mock IMAP object
        mock_imap.imap = Mock()
        mock_imap.logged_in = True
        mock_imap.mail_folders = ["INBOX", "Sent", "Trash"]
        mock_imap.selected_folder = "INBOX"
        mock_imap.selected_folder_utf7 = b"INBOX"
        mock_imap.separator = "/"

        # Create a proper mock for MailFolder
        mock_mail_folder = Mock(spec=MailFolder)
        mock_mail_folder.separator = "/"
        mock_mail_folder.get_separator.return_value = "/"
        mock_mail_folder.get_folders.return_value = ["INBOX", "Sent", "Trash"]
        mock_mail_folder.get_children.return_value = []
        mock_mail_folder.get_parent_name.return_value = "INBOX"

        mock_imap.mail_folder_class = mock_mail_folder
        mock_imap.folder_capabilities = {"INBOX": ["CAPABILITY1", "CAPABILITY2"]}

        mock_imap.imap.list.return_value = ("OK", [b'(\\HasNoChildren) "/" "INBOX"'])
        mock_imap.imap.capability.return_value = (
            "OK",
            [
                b"IMAP4rev1 UNSELECT IDLE NAMESPACE QUOTA ID XLIST CHILDREN X-GM-EXT-1 UIDPLUS COMPRESS=DEFLATE ENABLE MOVE CONDSTORE ESEARCH UTF8=ACCEPT LIST-EXTENDED LIST-STATUS LITERAL- SPECIAL-USE APPENDLIMIT=35651584"
            ],
        )

        yield mock_imap


def test_connect(mock_imap):
    assert mock_imap.connect.called
    assert mock_imap.logged_in is True


def test_connect_connection_refused():
    with patch("imaplib.IMAP4_SSL", side_effect=ConnectionRefused):
        with pytest.raises(ConnectionRefused):
            IMAP(
                host="imap.example.com", username="user", password="pass", ssl=True
            ).connect()


def test_connect_invalid_host():
    with patch("imaplib.IMAP4_SSL", side_effect=InvalidHost):
        with pytest.raises(InvalidHost):
            IMAP(
                host="invalid.host", username="user", password="pass", ssl=True
            ).connect()


def test_logout(mock_imap):
    mock_imap.logout()
    mock_imap.imap.close.assert_called_once()
    mock_imap.imap.logout.assert_called_once()
    assert mock_imap.logged_in is False
    assert mock_imap.selected_folder is None
    assert mock_imap.selected_folder_utf7 is None


def test_folders(mock_imap):
    assert mock_imap.folders() == ["INBOX", "Sent", "Trash"]


def test_folder_select(mock_imap):
    mock_imap.imap.select.return_value = ("OK", [b"1"])
    mock_imap.imap.close.reset_mock()

    mock_imap.folder("Sent")
    mock_imap.imap.select.assert_called_with('"Sent"')
    assert mock_imap.selected_folder == "Sent"
    assert mock_imap.selected_folder_utf7 == b"Sent"

    mock_imap.folder("INBOX")
    mock_imap.imap.select.assert_called_with('"INBOX"')
    assert mock_imap.selected_folder == "INBOX"
    assert mock_imap.selected_folder_utf7 == b"INBOX"

    with pytest.raises(NonexistentFolderError):
        mock_imap.folder("NonexistentFolder")

    mock_imap.folder()
    assert mock_imap.selected_folder is None
    assert mock_imap.selected_folder_utf7 is None

    assert mock_imap.imap.select.call_count == 2


def test_folder_nonexistent(mock_imap):
    with pytest.raises(NonexistentFolderError):
        mock_imap.folder("Nonexistent")


def test_children(mock_imap):
    mock_imap.mail_folder_class.get_children.return_value = [
        "Work/Project1",
        "Work/Project2",
    ]
    mock_imap.selected_folder = "Work"
    assert mock_imap.children() == ["Work/Project1", "Work/Project2"]


def test_parent(mock_imap):
    mock_imap.mail_folder_class.get_parent_name.return_value = "Work"
    mock_imap.selected_folder = "Work/Project1"
    mock_imap.parent()
    assert mock_imap.selected_folder == "Work"


def test_append(mock_imap):
    message = MIMEText("Test message")
    message["Subject"] = "Test Subject"
    message["From"] = "sender@example.com"
    message["To"] = "recipient@example.com"

    mock_imap.append(message, flags=[EmailFlag.SEEN])

    mock_imap.imap.append.assert_called_once_with(
        '"INBOX"', "(\\SEEN)", "", message.as_string()
    )

    mock_imap.imap.append.reset_mock()
    mock_imap.append(message)
    mock_imap.imap.append.assert_called_once_with(
        '"INBOX"', "", "", message.as_string()
    )

    mock_imap.imap.append.reset_mock()
    mock_imap.append(message, flags=[EmailFlag.RECENT])
    mock_imap.imap.append.assert_called_once_with(
        '"INBOX"', "", "", message.as_string()
    )

    with pytest.raises(UnknownEmailMessageType):
        mock_imap.append("Not a MIMEBase object")


def test_emails_by_sequence(mock_imap):
    mock_imap.imap.fetch.return_value = ("OK", [b"1 (UID 100)"])
    mock_imap._fetch_emails_info = Mock(return_value=[Mock(spec=EmailMessage)])
    mock_imap.info = Mock(return_value={"total": 1})
    emails = mock_imap.emails(1, 1)
    assert len(emails) == 1
    mock_imap.imap.fetch.assert_called_once_with("1:1", "(UID)")


def test_emails_by_query(mock_imap):
    query = Q().sender("test@example.com").seen()
    mock_imap.imap.uid.return_value = ("OK", [b"100 101 102"])
    mock_imap._fetch_emails_info = Mock(return_value=[Mock(spec=EmailMessage)] * 3)
    emails = mock_imap.emails(query)
    assert len(emails) == 3
    mock_imap.imap.uid.assert_called_once_with(
        "SEARCH", "FROM", '"test@example.com"', "SEEN"
    )


def test_mark(mock_imap):
    mock_imap.mark(EmailFlag.SEEN, "100")
    mock_imap.imap.uid.assert_called_once_with("STORE", "100", "+FLAGS", "(\\SEEN)")


def test_make_folder(mock_imap):
    mock_imap.make_folder("New Folder")
    mock_imap.imap.create.assert_called_once_with('"INBOX/New Folder"')
    mock_imap._update_folder_info.assert_called_once()


def test_copy_message(mock_imap):
    mock_imap.imap.uid.return_value = ("OK", None)
    mock_imap.imap.untagged_responses = {"COPYUID": ["1 100 200"]}
    msg = Mock(spec=EmailMessage)
    result = mock_imap.copy_message("100", "Sent", msg)
    mock_imap.imap.uid.assert_called_once_with("COPY", "100", '"Sent"')
    assert result.uid == "200"
    assert result.folder == "Sent"


def test_move_message(mock_imap):
    mock_imap.copy_message = Mock()
    mock_imap.delete_message = Mock()
    msg = Mock(spec=EmailMessage)
    mock_imap.move_message("100", "Sent", msg)
    mock_imap.copy_message.assert_called_once_with("100", "Sent", msg)
    mock_imap.delete_message.assert_called_once_with("100", "INBOX")


def test_delete_message(mock_imap):
    mock_imap.delete_message("100", "INBOX")
    mock_imap.imap.uid.assert_called_once_with("STORE", "100", "+FLAGS", "(DELETED)")


def test_info(mock_imap):
    mock_imap.imap.status.return_value = (
        "OK",
        [b"INBOX (MESSAGES 120 RECENT 5 UIDNEXT 4321 UIDVALIDITY 1234567890 UNSEEN 5)"],
    )
    info = mock_imap.info()
    assert info == {
        "total": 120,
        "recent": 5,
        "unseen": 5,
        "uidnext": 4321,
        "uidvalidity": 1234567890,
    }


def test_rename(mock_imap):
    mock_imap.folder = Mock()
    mock_imap.rename("New Name")
    mock_imap.imap.rename.assert_called_once_with('"INBOX"', '"New Name"')
    assert mock_imap._update_folder_info.call_count == 2
    assert mock_imap.folder.call_count == 2


def test_delete(mock_imap):
    mock_imap.delete()
    mock_imap.imap.delete.assert_called_once_with('"INBOX"')
    mock_imap._update_folder_info.assert_called_once()


@pytest.mark.parametrize(
    "method",
    [
        "folders",
        "folder",
        "children",
        "parent",
        "append",
        "emails",
        "mark",
        "make_folder",
        "copy_message",
        "move_message",
        "delete_message",
        "info",
        "rename",
        "delete",
    ],
)
def test_logged_out_error(mock_imap, method):
    mock_imap.logged_in = False
    with pytest.raises(ImapyLoggedOut):
        getattr(mock_imap, method)()
