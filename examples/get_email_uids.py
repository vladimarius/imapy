# -*- encoding: utf-8 -*-
"""
Get email UIDs of selected folder
"""

import imapy

em = imapy.connect(
    host="host",
    username="username",
    password="password",
    ssl=True,
)

uids = em.folder("INBOX").emails(ids_only=True)
print(uids)

# logout
em.logout()
