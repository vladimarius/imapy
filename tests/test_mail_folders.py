import pytest

from imapy.exceptions import EmailFolderParsingError
from imapy.mail_folder import MailFolder


@pytest.fixture
def mail_folder():
    return MailFolder()


def test_get_folders(mail_folder):
    raw_folders = [
        b'(\\HasNoChildren) "/" "INBOX"',
        b'(\\HasChildren) "/" "Work"',
        b'(\\HasNoChildren) "/" "Work/Projects"',
        b'(\\HasNoChildren) "/" "Work/Tasks"',
        b'(\\HasNoChildren) "/" "Personal"',
    ]
    folders = mail_folder.get_folders((None, raw_folders))

    assert folders == ["INBOX", "Work", "Work/Projects", "Work/Tasks", "Personal"]
    assert mail_folder.separator == "/"


def test_get_children(mail_folder):
    raw_folders = [
        b'(\\HasNoChildren) "/" "INBOX"',
        b'(\\HasChildren) "/" "Work"',
        b'(\\HasNoChildren) "/" "Work/Projects"',
        b'(\\HasNoChildren) "/" "Work/Tasks"',
        b'(\\HasNoChildren) "/" "Personal"',
    ]
    mail_folder.get_folders((None, raw_folders))

    assert mail_folder.get_children("Work") == ["Work/Projects", "Work/Tasks"]
    assert mail_folder.get_children("INBOX") == []
    assert mail_folder.get_children("Personal") == []


def test_get_separator(mail_folder):
    raw_folders = [b'(\\HasNoChildren) "/" "INBOX"']
    mail_folder.get_folders((None, raw_folders))

    assert mail_folder.get_separator() == "/"


def test_get_parent_name(mail_folder):
    raw_folders = [
        b'(\\HasNoChildren) "/" "INBOX"',
        b'(\\HasChildren) "/" "Work"',
        b'(\\HasNoChildren) "/" "Work/Projects"',
    ]
    mail_folder.get_folders((None, raw_folders))

    assert mail_folder.get_parent_name("Work/Projects") == "Work"
    assert mail_folder.get_parent_name("INBOX") == "INBOX"


def test_invalid_folder_info(mail_folder):
    raw_folders = [b"Invalid folder info"]

    with pytest.raises(EmailFolderParsingError):
        mail_folder.get_folders((None, raw_folders))


def test_unicode_folder_names(mail_folder):
    raw_folders = [
        b'(\\HasNoChildren) "/" "&2D3dJQ- ideas"',
        b'(\\HasNoChildren) "/" "&BB8EQAQ4BDIENQRC-"',
    ]
    folders = mail_folder.get_folders((None, raw_folders))
    assert folders == ["🔥 ideas", "Привет"]


def test_nested_folders(mail_folder):
    raw_folders = [
        b'(\\HasChildren) "/" "Parent"',
        b'(\\HasNoChildren) "/" "Parent/Child1"',
        b'(\\HasChildren) "/" "Parent/Child2"',
        b'(\\HasNoChildren) "/" "Parent/Child2/Grandchild"',
    ]
    folders = mail_folder.get_folders((None, raw_folders))

    assert folders == [
        "Parent",
        "Parent/Child1",
        "Parent/Child2",
        "Parent/Child2/Grandchild",
    ]
    assert mail_folder.get_children("Parent") == ["Parent/Child1", "Parent/Child2"]
    assert mail_folder.get_children("Parent/Child2") == ["Parent/Child2/Grandchild"]
