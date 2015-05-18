Imapy: Imap for Humans
======================


Imapy is an MIT Licensed IMAP library, written in Python.
It makes processing emails in your email box easy.

Most existing Python modules for dealing with IMAP are extremely
low-level. They require the programmer to know the intricacies of IMAP
protocol and differences in IMAP server behaviour so that even
simple tasks require writing hundred lines of code.

Imapy changes that.


.. code-block:: python

    >>> box = imapy.connect(
                  host='imap.gmail.com',
                  username='imapy@gmail.com',
                  password='secret',
                  ssl=True)

**Get all folder names:**

    >>> names = box.folders()

**Get last 5 emails in 'Inbox' folder:**

    >>> emails = box.folder('Inbox').emails(-5)

**Get unseen emails with Awesome in subject:**

    >>> q = Q()
    >>> emails = box.folder('Inbox').emails(
    >>>     q.subject('Awesome').unseen()
    >>> )

**Move messages sent by your boss to "Important" folder and mark them 'Flagged' and 'Unseen':**

    >>> q = Q()
    >>> emails = box.folder('Inbox').emails(
    >>>     q.sender('boss@email.com').unseen()
    >>> )
    >>> for email in emails:
    >>>     email.move('Important').mark(['Flagged', 'Unseen'])
    >>> 

**Print some email details:**

    >>> for email in emails:
    >>>    print(email['from'], email['subject'])

**Process all emails in 'Inbox' folder:**

    >>> status = box.folder('Inbox').info()
    >>> total = status['total']
    >>> for t in range(1, total + 1):
    >>>     email = box.folder('Inbox').email(t)
    >>>     print(email['subject'])

**Logout**

    >>> box.logout()

You can see more examples `here <https://github.com/vladimarius/imapy/tree/master/examples>`_



Installation
------------

To install Imapy, simply:

.. code-block:: bash

    $ pip install imapy


Miscellaneous
-------------
`Notes <https://github.com/vladimarius/imapy/blob/master/NOTES.rst>`_  & `TODO <https://github.com/vladimarius/imapy/blob/master/TODO.rst>`_