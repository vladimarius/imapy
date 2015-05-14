# -*- encoding: utf-8 -*-
"""
Shows some email search functionality.
"""

import imapy
from imapy.query_builder import Q

box = imapy.connect(
    host='host',
    username='username',
    password='password',
    ssl=True,
)

""" Search for unseen emails from Inbox sent
    from "example.com" with "important" in subject
"""
q = Q()
emails = box.folder('Inbox').emails(
    q.unseen().sender("example.com").subject("important")
)

""" Search for flagged emails from Inbox sent
    since February 15, 2014
"""
q = Q()
emails = box.folder('Inbox').emails(
    q.flagged().since('15-Feb-2014')
)

""" Search for emails in Inbox subfolder named "Secret"
    containing text 'Chewbacca' in body sent after
    September 5th, 2070 which were left unanswered
"""
q = Q()
folder_name = 'Inbox' + box.separator + 'Secret'
emails = box.folder(folder_name).emails(
    q.text('Chewbacca').since('5-Sep-2070').unanswered()
)

# logout
box.logout()
