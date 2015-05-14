# -*- encoding: utf-8 -*-
"""
Shows how to append email to folder
"""

import imapy
from email.mime.text import MIMEText


def get_text_email(sender, recepient, subject, text):
    """returns email object"""
    msg = MIMEText(text, "plain", "utf-8")
    msg['Subject'] = subject
    msg['From'] = sender
    msg['To'] = recepient

    return msg

box = imapy.connect(
    host='host',
    username='username',
    password='password',
    ssl=True,
)


# create 'Imapy' folder
box.folder().make_folder('Imapy')

# prepare email
text_email = get_text_email(
    'imapy@sample.com',
    'you@sample.com',
    'Howdy!',
    'Hi there, dear Imapy user :)')

# append email to folder
box.folder('Imapy').append(text_email, flags=['flagged'])

# logout
box.logout()
