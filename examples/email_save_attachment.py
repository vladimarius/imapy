# -*- encoding: utf-8 -*-
"""
Shows how to save email attachments with Imapy to a file
"""

import imapy
from imapy.query_builder import Q

connection = {
    "host": "imap.gmail.com",
    "username": "name@email.com",
    "password": "123",
    "ssl": True,
}

with imapy.connect(**connection) as em:
    """
    Suppose in our 'Inbox' folder we have email titled 'PDF test'
    containing some PDF file attached to it
    """
    # select the required email
    q = Q()
    emails = em.folder("Inbox").emails(q.subject("PDF test"))

    # get attachment info
    if len(emails):
        email = emails[0]
        for attachment in email.attachments:
            # save each attachment in current directory
            file_name = attachment.filename
            content_type = attachment.content_type
            data = attachment.data

            with open(file_name, "wb") as f:
                f.write(data)
