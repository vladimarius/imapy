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
# (note that Gmail uses "INBOX" as Inbox folder name)
status = box.folder('Inbox').info()
total_messages = status['total']

# create folder named 'Awesome' in the root folder
# having subfolder named 'Even awesomer'
box.folder().make_folder('Awesome')
box.folder('Awesome').make_folder('Even awesomer')

# get 5 latest emails from Inbox and print some details
emails = box.folder('Inbox').emails(-5)

for email in emails:
    print ('Email from: {0}'.format(email['from']))
    print ('Email subject: {0}'.format(email['subject']))

# copy last 3 emails from 'Inbox' to 'Awesome/Even awesomer'
# folder, make them flagged and unseen
emails = box.folder('Inbox').emails(-3)
for em in emails:
    folder_name = 'Awesome' + box.separator + 'Even awesomer'
    em.copy(folder_name).mark(['Unseen', 'Flagged'])

# logout
box.logout()
