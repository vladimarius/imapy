# -*- encoding: utf-8 -*-
"""
Shows how to append email to folder
"""

from email.mime.text import MIMEText

import imapy


def get_text_email(sender, recepient, subject, text):
    """returns email object"""
    msg = MIMEText(text, "plain", "utf-8")
    msg['Subject'] = subject
    msg['From'] = sender
    msg['To'] = recepient

    return msg

em = imapy.connect(
    host='host',
    username='username',
    password='password',
    ssl=True,
)


# create 'Imapy' folder
em.folder().make_folder('Imapy')

# prepare email
text_email = get_text_email(
    'imapy@sample.com',
    'you@sample.com',
    'Howdy!',
    'Hi there, dear Imapy user :)')

# append email to folder
em.folder('Imapy').append(text_email, flags=['flagged'])

# logout
em.logout()
