Testing
-------
Imapy is currently being tested under Python 2.7, 3.2, 3.3, 3.4 using following imap servers or services:

- gmail.com
- yahoo.com
- Dovecot
- yandex.com
- outlook.com


Excluded from testing:

- Mail.com
- Gmx.com

(Both of the above don't support creating folders containing
non-ascii symbols, return *"NO unallowed folder"* response
when trying to create one)

- Inbox.com

(Registration is closed for my country)

Search implementation
---------------------
Imapy uses its own class to construct search queries. 
It allows to create simple, non-nested AND queries.
It means that all search conditions specified by user
has to be met in search results. It doesn't currently
support joining query conditions with OR and NOT statements.

Imapy doesn't yet **officially** support using non-ascii symbols
to search for emails. This is due to a behaviour of imaplib
(Python library used by Imapy) which lacks such support
and causes errors under specific conditions. For example
using non-ascii symbols to search Yahoo folder will raise an
error. Google, Dovecot and some others seem to work fine.

Another thing to notice is that you cannot use more than **1**
search condition containing non-ascii symbols due to limitations
in underlying imaplib library.

**Important** thing to know while searching for emails is that search retrieves all resulting emails. It may become a problem in situations where number of emails is too much or email(s) size is too big and might not fit in memory. Probably a better thing would be to use generator-based approach, however it haven't been a priority for a version 1 release. 

Notes on IMAP servers
---------------------

**Yahoo**

Yahoo mail imap implementation doesn't seem to 
support SEARCH command with following arguments
(returning error responses) :

- SENTBEFORE
- SENTSINCE 
- SENTON 
- ON
- KEYWORD
- UNKEYWORD

Search using non-ascii characters on Yahoo raises error
due to imaplib bug (see **"Search implementation"** above).

**Dovecot**

Disconnects after deleting folder when such folder is currently
selected. Send *"BYE Selected mailbox was deleted, have to disconnect."* response

Deletes parent folder without deleting child folder.
Imagine you have "Abc" as a parent email folder for "Def" with a
folder separator "/". Parent folder name is "Abc", child name is
"Abc/Def". If "Abc" is deleted, the server will not
delete child folder(s) and it will still have a folder named "Abc/Def"
having no parent folder.

**Outlook**

Outlook IMAP doesn't allow to rename currently selected
folder. Returns *"NO [CANNOT] Cannot rename selected folder."*


Email parsing
-------------
- Pythons' email.header.decode_header fails to correctly parse 'From' header 
when there is no space between email sender name/organization and email address
- Pythons' email.header.decode_header may return different results in Python2 and
Python 3
- Some headers may not be present in email: 'To' header may be omitted (Yandex appends it's first welcome email to Inbox without it) and 'Subject'
