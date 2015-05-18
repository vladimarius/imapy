# -*- encoding: utf-8 -*-
"""
Shows how to check for specific email, reply to it (inserting original
message text) and mark processed message as read.
"""

import imapy
from imapy.query_builder import Q
import smtplib
from email.mime.text import MIMEText


def get_text_email(sender, recepient, subject, text):
    """Returns email object"""
    msg = MIMEText(text, "plain", "utf-8")
    msg['Subject'] = subject
    msg['From'] = sender
    msg['To'] = recepient

    return msg


box = imapy.connect(
    host='host',
    username='username',
    password='password',
    ssl='ssl',  # True or False
)

'''
    Suppose we need to process automatically new emails in
    'Inbox' folder which contain 'help me' in subject
'''
# find those emails
q = Q()
emails = box.folder('INBOX').emails(
    q.subject('help me').unseen()
)

# connect to SMTP server
user = 'test@gmail.com'
password = 'password'
s = smtplib.SMTP("smtp.gmail.com", 587)
s.ehlo()
s.starttls()
s.ehlo
s.login(user, password)

# reply to each email
for em in emails:
    # get all email headers (simply for demonstration)
    headers = em['headers']
    from_name = em['from_whom'] or 'Sir/Madam'
    from_email = em['from_email']
    from_subject = em['subject']

    """ All text contents and attachments are stored in email['text'] list
    while html contents/attachments in email['html'].

    Information about text is stored as a dictionary having 3 values:
        'text' - unmodified text
        'text_normalized' - text with spaces/tabs/newlines stripped
        'links' - list of links found in text
    """

    original_message = em['text'][0]['text']
    email_text = """
Dear {from_name},

Your request has been received and processed.

Best regards,
Imapy support


--------------------------
In reply to your message:
--------------------------
{original_message}
--------------------------
    """.format(from_name=from_name,
               original_message=original_message)

    # Send the message via SMTP server (Gmail 'test@gmail.com')
    msg = get_text_email(user, from_email, 'Re: ' + from_subject, email_text)

    # send email
    s.sendmail(user, [from_email], msg.as_string())

    # mark message as read
    em.mark('seen')

s.quit()
