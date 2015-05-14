# -*- encoding: utf-8 -*-
"""
Shows some basic operations with Imapy
"""

import imapy

box = imapy.connect(
    host='host',
    username='username',
    password='password',
    ssl=True,
)

# get all folder names
folders = box.folders()

""" 'folders' now contains a list of all folder names.
    Email folders can be hierarchical (have parent and
    children). A folder name of a child folder consists
    of a parent name + separator symbol + name of a child.
"""

# get information about Inbox folder
status = box.folder('Inbox').info()
total_messages = status['total']

# get 5 latest emails and print some details
emails = box.folder('Inbox').emails(-5)

for email in emails:
    print ('Email from: {0}'.format(email['from']))
    print ('Email subject: {0}'.format(email['subject']))

# logout
box.logout()