# -*- encoding: utf-8 -*-
"""
Shows some email search functionality.
"""

import imapy
from imapy.query_builder import Q

em = imapy.connect(
    host='host',
    username='username',
    password='password',
    ssl=True,
)

""" Search for unseen emails from Inbox sent
    from "example.com" with "important" in subject
"""
q = Q()
emails = em.folder('Inbox').emails(
    q.unseen().sender("example.com").subject("important")
)

""" Search for flagged emails from Inbox sent
    since February 15, 2014
"""
q = Q()
emails = em.folder('Inbox').emails(
    q.flagged().since('15-Feb-2014')
)

""" Search for emails having size less than
    4 Kilobytes
"""
q = Q()
emails = em.folder('Inbox').emails(
    q.smaller('4 KB')
    # Calls below are also OK:
    # q.smaller('4 Kilobytes')
    # q.smaller(4000) # <-- size in bytes

    # Also fine, but most likely you wouldn't want to do that:
    # q.larger('99 Mb')
    # q.larger('3 gigabytes')
)

""" Search for emails in Inbox subfolder named "Secret"
    containing text 'Chewbacca' in body sent after
    September 5th, 2070 which were left unanswered
"""
q = Q()
folder_name = 'Inbox' + em.separator + 'Secret'
emails = em.folder(folder_name).emails(
    q.text('Chewbacca').since('5-Sep-2070').unanswered()
)

# logout
em.logout()
