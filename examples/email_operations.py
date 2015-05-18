# -*- encoding: utf-8 -*-
"""
Shows how to deal with email messages in Imapy
"""

import imapy
import re


def get_ipv4(headers):
    """Returns ip address (v4) from message 'Received' header.
       (ip detection is oversimplified)
    """
    received = headers['Received'].pop()
    match = re.search('(?P<ip>\d+\.\d+\.\d+\.\d+)', received)
    if match:
        return match.group('ip')
    return 'ip not found'


box = imapy.connect(
    host='host',
    username='username',
    password='password',
    ssl=True,
)

# first create some folders in the root email directory
box.folder().make_folder(['Imapy1', 'Imapy2'])

if 'Inbox' in box.folders():
    """
        Copying emails
    """
    # select first 3 emails in 'Inbox' (the oldest ones)
    emails = box.folder('Inbox').emails(1, 3)
    for em in emails:
        # copy each email to 'Imapy1', flagging it and making unseen
        em.copy('Imapy1').mark(['flagged', 'unseen'])

    """
        Moving emails
    """
    # move 1 email from 'Imapy1' to 'Imapy2'
    box.folder('Imapy1').email(1).move('Imapy2')

    """
        Marking emails
    """
    box.folder('Imapy2').email(1).mark(['unflagged'])

    """
        Message headers
    """
    # get list of email headers for an email
    email_data = box.folder('Imapy2').email(1)
    headers = email_data['headers']

    # get ip of sender
    print('Ip of a sender: {0}'.format(get_ipv4(headers)))

    # show message id
    # (note that you may get headers in case-insensitive manner
    # so headers['Message-id'] and headers['MESSAGE-id'] refer
    # to the same object)
    print('Message id: {0}'.format(headers['Message-Id'][0]))
