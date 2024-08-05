# -*- coding: utf-8 -*-

""" Tests for imapy """

import pytest
import imaplib
import time
import os
import imapy
import email
from imapy import (imap, mail_folder, exceptions as e)
from imapy.query_builder import Q
from imapy.packages import (six)
from imapy.email_message import EmailMessage
try:
    from settings import (host, username, password, ssl)
except:
    pytestmark = pytest.mark.skip('settings not available')
from email.mime.text import MIMEText
from imapy import utils


def is_ascii(self, txt):
    """Returns True if string consists of ASCII characters only,
    False otherwise
    """
    try:
        txt.encode('utf-8').decode('ASCII')
    except UnicodeDecodeError:
        return False
    return True


def get_text_email(efrom, eto, esubject, etext, ebcc=None, ecc=None):
    """returns email object"""
    msg = MIMEText(etext, "plain", "utf-8")
    msg['Subject'] = esubject
    msg['From'] = efrom
    msg['To'] = eto
    if ebcc:
        msg['Bcc'] = ebcc
    if ecc:
        msg['Cc'] = ecc

    return msg


def setup_function(module):
    """ Delete all testing folders and empties Trash"""
    box = imapy.connect(
        host=host,
        username=username,
        password=password,
        ssl=ssl)

    folders = box.folders()
    sep = box.separator
    bad_folders = ['imapy-del1', 'imapy-del2', 'imapy-search test',
                   'Imapy-delete', 'Imapy-delete123', 'Imapy тест 123',
                   'Imapy тест 123' + sep + 'Subfolder 456 тест']
    trash_folders = ['Deleted', 'Удаленные', 'Trash',
                     '[Gmail]' + sep + 'Trash']

    for f in folders:
        # delete folders inside trash folder: '[Gmail]/Trash/123'
        for tf in trash_folders:
            if tf in f and tf != f:
                box.folder().delete(f)
        # delete bad folders
        if f in bad_folders:
            box.folder().delete(f)

    # delete messages inside trash folder
    trash_folders = [t.rstrip(sep) for t in trash_folders]
    server_trash_folders = list(set(trash_folders) & set(box.folders()))
    for f in server_trash_folders:
        emails = box.folder(f).emails(-100)
        if emails:
            for em in emails:
                em.delete()


def test_mail_folder_class():
    m = mail_folder.MailFolder()
    if six.PY2:
        raw_folders = ['(\\HasNoChildren) "/" "INBOX"',
                       '(\\HasNoChildren) "/" "Junk"',
                       '(\\HasNoChildren) "/" "Personal"',
                       '(\\HasNoChildren) "/" "Receipts"',
                       '(\\HasNoChildren) "/" "Trash"',
                       '(\\HasNoChildren) "/" "Travel"',
                       '(\\HasNoChildren) "/" "Work"',
                       '(\\HasChildren \\Noselect) "/" "[Gmail]"',
                       '(\\HasNoChildren \\All) "/" "[Gmail]/All Mail"',
                       '(\\HasNoChildren \\Drafts) "/" "[Gmail]/Drafts"',
                       '(\\HasNoChildren \\Important) "/" "[Gmail]/Important"',
                       '(\\Sent \\HasNoChildren) "/" "[Gmail]/Sent Mail"',
                       '(\\HasNoChildren \\Junk) "/" "[Gmail]/Spam"',
                       '(\\HasNoChildren \\Flagged) "/" "[Gmail]/Starred"',
                       '(\\HasChildren \\Trash) "/" "[Gmail]/Trash"',
                       '(\\HasNoChildren) "/" "[Gmail]/Trash/3"',
                       '(\\HasChildren) "/" "&BB4EPwQ1BEAEMARGBDgETw- &BCs-"',
                       '(\\HasNoChildren) "/" "&BB4EPwQ1BEAEMARGBDgETw- &BCs-'
                       '/&BB4EPwQ1BEAEMARGBDgETw- &BCM-"']
        bad_folders = ['(\\HasNoChildren) "Receipts"']
    if six.PY3:
        raw_folders = [b'(\\HasNoChildren) "/" "INBOX"',
                       b'(\\HasNoChildren) "/" "Junk"',
                       b'(\\HasNoChildren) "/" "Personal"',
                       b'(\\HasNoChildren) "/" "Receipts"',
                       b'(\\HasNoChildren) "/" "Trash"',
                       b'(\\HasNoChildren) "/" "Travel"',
                       b'(\\HasNoChildren) "/" "Work"',
                       b'(\\HasChildren \\Noselect) "/" "[Gmail]"',
                       b'(\\HasNoChildren \\All) "/" "[Gmail]/All Mail"',
                       b'(\\HasNoChildren \\Drafts) "/" "[Gmail]/Drafts"',
                       b'(\\HasNoChildren \\Important) "/" '
                       b'"[Gmail]/Important"',
                       b'(\\Sent \\HasNoChildren) "/" "[Gmail]/Sent Mail"',
                       b'(\\HasNoChildren \\Junk) "/" "[Gmail]/Spam"',
                       b'(\\HasNoChildren \\Flagged) "/" "[Gmail]/Starred"',
                       b'(\\HasChildren \\Trash) "/" "[Gmail]/Trash"',
                       b'(\\HasNoChildren) "/" "[Gmail]/Trash/3"',
                       b'(\\HasChildren) "/" "&BB4EPwQ1BEAEMARGBDgETw- &BCs-"',
                       b'(\\HasNoChildren) "/" "&BB4EPwQ1BEAEMARGBDgETw- '
                       b'&BCs-/&BB4EPwQ1BEAEMARGBDgETw- &BCM-"']
        bad_folders = [b'(\\HasNoChildren) "Receipts"']

    folders_tree, children = m._get_folders_tree_and_children(raw_folders)
    assert type(folders_tree) is dict
    assert len(folders_tree) == 9

    with pytest.raises(e.EmailFolderParsingError):
        m._get_folders_tree_and_children(bad_folders)


def test_wrong_login_credentials():
    with pytest.raises(e.ConnectionRefused):
        imapy.connect(
            host='nonexistent',
            username='username',
            password='password',
            ssl=True)
    with pytest.raises(imaplib.IMAP4_SSL.error):
        imapy.connect(
            host=host,
            username='username',
            password='password',
            ssl=True)


def test_logout():
    with imapy.connect(
            host=host, username=username, password=password, ssl=ssl) as box:
        assert(box.logged_in is True)
    assert(box.logged_in is False)

    box = imapy.connect(
        host=host,
        username=username,
        password=password,
        ssl=ssl)
    assert(box.logged_in is True)
    box.logout()
    assert(box.logged_in is False)


def test_search_params():
    box = imapy.connect(
        host=host,
        username=username,
        password=password,
        ssl=ssl)

    from1 = 'sender@domain.com'
    to1 = 'recipient@destination.com'
    subject1 = 'Samplissimo subject. Всякое разное'
    contents1 = 'Lorem ipsum dorem sit amet.' +\
        'Съешь ещё этих мягких французских булок, да выпей же чаю. ' +\
        'http://www.cnn.com https://wikipedia.org http://del.icio.us'
    bcc1 = 'another@email.com'
    ecc1 = 'carboncopy@email.com'

    text_email1 = get_text_email(from1, to1, subject1, contents1, bcc1, ecc1)

    # append email to folder
    folder_name = 'imapy-search test'
    box.folder().make_folder(folder_name)
    box.folder(folder_name).append(
        text_email1,
        flags=['answered', 'draft', 'flagged', 'seen'])

    q = Q()
    with pytest.raises(e.SearchSyntaxNotSupported):
        emails = box.folder(folder_name).emails(
            q.subject('Съешь').sender('ещё')
        )

    q = Q()
    with pytest.raises(e.WrongDateFormat):
        emails = box.folder(folder_name).emails(
            q.since('2014-Jan-1')
        )

    q = Q()
    today = time.strftime('%d-%b-%Y')
    query = q.sender(from1).bcc(bcc1).answered().before('1-Jan-2050').\
        body('ipsum').cc(ecc1).draft().flagged().larger(1).seen().\
        sent_before('1-Jan-2050').sent_since('1-Jan-2014').\
        since('1-Jan-2014').smaller(10000000).text('ipsum').\
        recipient(to1).undeleted().sent_on(today).on(today)

    emails = box.folder(folder_name).emails(
        query
    )
    ''' we don't test the amount of results because
        different imap servers handle search differently
        and may not return any results
    '''
    assert isinstance(emails, list)

    q = Q()
    # the queries below are pointless and used only for testing
    query = q.sender('abc').unseen().unflagged().undraft().unanswered().\
        uid('123')
    emails = box.folder(folder_name).emails(
        query
    )
    assert isinstance(emails, list)

    q = Q()
    query = q.recent()
    emails = box.folder(folder_name).emails(
        query
    )
    assert isinstance(emails, list)

    q = Q()
    query = q.sender('abcsdfsd').old()
    emails = box.folder(folder_name).emails(
        query
    )
    assert isinstance(emails, list)

    q = Q()
    query = q.sender('abcsdfsd').new()
    emails = box.folder(folder_name).emails(
        query
    )
    assert isinstance(emails, list)

    q = Q()
    query = q.sender('abcsdfsd').\
        header('some-header', 'some value').deleted()
    emails = box.folder(folder_name).emails(
        query
    )
    assert isinstance(emails, list)

    box.logout()


def test_operations():

    box = imapy.connect(
        host=host,
        username=username,
        password=password,
        ssl=ssl)

    assert isinstance(box, imap.IMAP)
    assert box.lib in (
        imaplib.IMAP4_SSL,
        imaplib.IMAP4,
        imaplib.IMAP4_stream)

    # folders()
    folders = box.folders()
    assert len(folders) > 0
    for f in folders:
        assert len(f) > 0
    folders2 = box.folders()
    assert folders2 == folders

    # no children
    assert box.children() == []

    # folder()
    assert box.selected_folder is None
    box.folder(folders[0])
    assert box.selected_folder is not None

    # children()
    assert type(box.children()) is list
    with pytest.raises(e.NonexistentFolderError):
        box.folder('NonexistentFolder')

    '''

    Create, rename, delete folder

    '''
    # create list of folders
    folders_list = ['imapy-del1', 'imapy-del2']
    box.folder().make_folder(folders_list)
    for f in folders_list:
        assert f in box.folders()

    box.folder().delete(folders_list)
    for f in folders_list:
        assert f not in box.folders()

    # create folder
    delete_name = 'Imapy-delete'
    box.folder().make_folder(delete_name)
    assert delete_name in box.folders()
    with pytest.raises(e.InvalidFolderName):
        box.make_folder('BadFolder' + box.separator + 'Name')

    # rename
    new_name = delete_name + '123'
    box.folder(delete_name).rename(new_name)
    assert new_name in box.folders()
    # delete
    box.folder().delete(new_name)
    assert (new_name) not in box.folders()

    '''

    Create subfolders, append messages, check messages,
    folder info, email search, mark messages with tags,
    delete messages, select parent folder

    '''
    # create folder (ascii + unicode)
    test_folder = 'Imapy тест 123'
    box.folder().make_folder(test_folder)
    assert test_folder in box.mail_folders

    # create subfolder (ascii + unicode)
    test_subfolder = 'Subfolder 456 тест'
    box.folder(test_folder).make_folder(test_subfolder)
    test_folder_full_name = test_folder + box.separator + test_subfolder
    assert test_folder_full_name in box.mail_folders

    from1 = 'imapy-test@example.com'
    to1 = 'to@destination.com'
    subject1 = 'Email subject заголовок -*-'
    test_subject1 = 'subject'
    contents1 = 'Email contents содержание'

    text_email1 = get_text_email(from1, to1, subject1, contents1)

    # check status1 before append
    status1 = box.folder(test_folder).info()
    assert status1['total'] == 0

    # append email to folder
    non_standard_flags = ['really-non-standard-flag', 'weird-flag']
    box.folder(test_folder).append(
        text_email1, flags=non_standard_flags)

    with pytest.raises(e.UnknownEmailMessageType):
        box.folder(test_folder).append({'dummy': 'dict'})

    # check status1 after append
    status1 = box.folder(test_folder).info()
    assert status1['total'] == 1

    # check appended email flags
    emails = box.folder(test_folder).emails(-1)
    for f in non_standard_flags:
        assert f not in emails[0]['flags']

    from2 = 'imapy-test2@example.com'
    to2 = 'to2@destination.com'
    subject2 = 'Email subject 2заголовок2 -*-'
    test_subject2 = 'subject'
    contents2 = 'Email contents содержание2'

    text_email2 = get_text_email(from2, to2, subject2, contents2)

    children = box.folder(test_folder).children()
    subfolder_name = children[0]

    # check parent selection
    parent_folder_obj = box.folder(test_folder).__dict__
    selected_parent_folder_obj = box.folder(subfolder_name).parent().__dict__
    assert parent_folder_obj == selected_parent_folder_obj

    # check parent selection when parent is already on topmost level
    parent_folder_obj = box.folder(test_folder).__dict__
    selected_parent_folder_obj =\
        box.folder(subfolder_name).parent().parent().__dict__
    assert parent_folder_obj == selected_parent_folder_obj

    # check status2 before append
    status2 = box.folder(subfolder_name).info()
    assert status2['total'] == 0

    # append email to subfolder
    box.folder(subfolder_name).append(text_email2, flags=['flagged'])

    # check status2 after append
    status2 = box.folder(subfolder_name).info()
    assert status2['total'] == 1

    # search non-existent emails
    q = Q()
    query = q.subject('nonEXISTENTemailSEARCHstring')
    emails = box.folder(test_folder).emails(
        query
    )
    assert emails == []

    # search all emails in folder
    emails = box.folder(test_folder).emails()
    assert len(emails) > 0

    # search email 1
    q = Q()
    query = q.subject(test_subject1)
    emails = box.folder(test_folder).emails(
        query
    )
    assert len(emails) > 0
    # add flag to email
    email1 = emails[0]
    email1.mark(['seen', 'unflagged'])

    with pytest.raises(e.TagNotSupported):
        email1.mark(['unsupported_tag', 'really_nonstandard'])

    # check email attributes
    assert 'seen' in email1['flags']
    assert 'flagged' not in email1['flags']
    assert email1['from'] == from1
    assert email1['to'] == to1
    assert email1['subject'] == subject1
    assert email1['text'][0]['text'] == contents1

    # get email flags from server to recheck
    emails_flags = box.folder(test_folder).emails(
        query
    )
    email_flags = emails_flags[0]
    assert 'seen' in email_flags['flags']
    assert 'flagged' not in email_flags['flags']

    # search for email 2
    q = Q()
    query = q.subject(test_subject2)
    emails = box.folder(subfolder_name).emails(
        query
    )
    assert len(emails) > 0

    # check email attributes
    email2 = emails[0]
    assert email2['from'] == from2
    assert email2['to'] == to2
    assert email2['subject'] == subject2
    assert email2['text'][0]['text'] == contents2

    # delete email1 from folder
    email1.delete()
    # check status1 after delete
    status1 = box.folder(test_folder).info()
    assert status1['total'] == 0

    # delete email2 from subfolder
    email2.delete()
    # check status2 after delete
    status2 = box.folder(subfolder_name).info()
    assert status2['total'] == 0

    """

    Copy email

    """
    # append email
    from3 = 'imapy-test-copy@example.com'
    to3 = 'to@destination.com'
    subject3 = 'Copy email testing, заголовок -*-'
    contents3 = 'Testing email copying. Проверка копирования email'

    text_email3 = get_text_email(from3, to3, subject3, contents3)
    box.folder(test_folder).append(text_email3)

    status3 = box.folder(test_folder).info()
    assert status3['total'] == 1

    # copy email
    emails = box.folder(test_folder).emails(-1)
    emails[0].copy(subfolder_name)
    status4 = box.folder(subfolder_name).info()
    assert status4['total'] == 1

    """

    Move email

    """
    from4 = 'imapy-test-move@example.com'
    to4 = 'to@destination.com'
    subject4 = 'Move email testing'
    contents4 = 'Testing email moving'

    text_email4 = get_text_email(from4, to4, subject4, contents4)
    subfolder_before_move_status = box.folder(subfolder_name).info()
    box.folder(test_folder).append(text_email4)

    emails = box.folder(test_folder).emails(-1)
    assert len(emails) > 0

    emails[0].move(subfolder_name)
    subfolder_after_move_status = box.folder(subfolder_name).info()
    assert subfolder_before_move_status['total'] != \
        subfolder_after_move_status['total']

    """

    Emails selecting

    """
    with pytest.raises(e.InvalidSearchQuery):
            box.folder(test_folder).emails(1, 2, 3)

    with pytest.raises(e.InvalidSearchQuery):
            box.folder(test_folder).emails('something', 'weird')

    with pytest.raises(e.InvalidSearchQuery):
            box.folder(test_folder).emails('weird')

    with pytest.raises(e.InvalidSearchQuery):
            box.folder(test_folder).emails(1, -10)

    with pytest.raises(e.InvalidSearchQuery):
            box.folder(test_folder).emails(-1, 10)

    # test folders searching with regexp
    # setup fake box.mail_folders variable and separator
    box.mail_folders = [
        # level 1
        'Inbox',
        'Some long name',
        'Входящие',
        'Длинное название ящика',
        # level 2
        'Inbox/Important stuff',
        'Входящие/Важные сообщения',
    ]
    box.separator = '/'

    assert 'Inbox' in box.folders('Inbox')
    assert 'Inbox' in box.folders('*nbox')
    assert 'Inbox' in box.folders('Inbo*')
    assert 'Inbox' in box.folders('*nbo*')
    assert 'Inbox' in box.folders('*n*o*')
    assert 'Some long name' in box.folders('Some*long*')
    assert 'Some long name' in box.folders('*o*n*e')
    assert 'Some long name' in box.folders('*long*')
    assert 'Длинное название ящика' in box.folders('*инн*')
    assert 'Длинное название ящика' in box.folders('Длинное*')
    assert 'Длинное название ящика' in box.folders('*ящика')
    assert 'Inbox/Important stuff' in box.folders('Important*')
    assert 'Inbox/Important stuff' in box.folders('*ant*')
    assert 'Inbox/Important stuff' in box.folders('* stuff')
    assert 'Входящие/Важные сообщения' in box.folders('Важные*')
    assert 'Входящие/Важные сообщения' in box.folders('*сообщ*')
    assert 'Входящие/Важные сообщения' in box.folders('* сообщения')

    # log out
    box.log_out()
    with pytest.raises(e.ImapyLoggedOut):
            box.folders()
