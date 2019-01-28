# -*- coding: utf-8 -*-
import email
import os
from imapy import utils
from imapy.email_message import EmailMessage


def test_parsing_sample_emails():
    # check parsing sample emails (msg1, msg2 ...)
    msg_dir = "test_emails"
    fnames = os.listdir(msg_dir)
    for fn in fnames:
        if '.msg' in fn:
            f = open(msg_dir + os.sep + fn, 'rb')
            raw_email = f.read()
            email_obj = email.message_from_string(utils.b_to_str(raw_email))
            email_parsed = EmailMessage(
                folder='no_folder', uid=999, flags=[],
                email_obj=email_obj, imap_obj=None)
            msg_num = int(fn.split('.')[0])

            if msg_num == 1:
                assert email_parsed['from_WHOM'] == 'Dropbox'
                assert email_parsed['from'] ==\
                    'Dropbox <no-reply@dropboxmail.com>'
                assert email_parsed['from_email'] == 'no-reply@dropboxmail.com'
                assert email_parsed['cc'] == []
                assert email_parsed['subject'] ==\
                    'Update: Changes to better serve our users around the' +\
                    ' world'
                assert email_parsed['date'] == 'Sat, 2 May 2015 13:46:01 +0000'
                assert 'outside of North America' in\
                    email_parsed['text'][0]['text_normalized']
                assert len(email_parsed['html']) > 0

            elif msg_num == 2:
                assert email_parsed['from_WHOM'] == \
                    'Надежда ДранинаfS (via Twitter)'
                assert 'Надежда ДранинаfS' in email_parsed['from'] and\
                    '<notify@twitter.com>' in email_parsed['from']

                assert email_parsed['from_email'] == 'notify@twitter.com'
                assert email_parsed['cc'] == []
                assert email_parsed['subject'] ==\
                    'Надежда ДранинаfS (@dranina73) is now following' + \
                    ' you on Twitter!'
                assert email_parsed['date'] ==\
                    'Wed, 22 Apr 2015 05:00:36 +0000'
                assert 'You have a new follower on' in\
                    email_parsed['text'][0]['text_normalized']
                assert len(email_parsed['html']) > 0

            elif msg_num == 3:
                assert email_parsed['from_WHOM'] == \
                    '"USPS"'
                assert email_parsed['from'] ==\
                    '"USPS" <no-reply@usps.com>'
                assert email_parsed['from_email'] == 'no-reply@usps.com'
                assert email_parsed['cc'] == []
                assert email_parsed['subject'] ==\
                    'Shipment status change for package # 23696393'
                assert email_parsed['date'] ==\
                    'Thu, 30 Apr 2015 09:32:16 -0700'
                assert 'The package could not be delivered' in\
                    email_parsed['text'][0]['text_normalized']
                assert len(email_parsed['html']) == 0

            elif msg_num == 4:
                assert email_parsed['from_WHOM'] == \
                    'François Schiettecatte'
                assert 'François Schiettecatte' in email_parsed['from'] and\
                    '<fschiettecatte@gmail.com>' in email_parsed['from']
                assert email_parsed['from_email'] == 'fschiettecatte@gmail.com'
                assert email_parsed['cc'] == []
                assert email_parsed['subject'] ==\
                    'Re: Require code explaination'
                assert email_parsed['date'] ==\
                    'Wed, 29 Apr 2015 09:46:37 -0400'
                assert 'Django does not implement X-Accel-Redirect' in\
                    email_parsed['text'][0]['text_normalized']
                assert len(email_parsed['html']) == 0

            elif msg_num == 5:
                assert email_parsed['from_WHOM'] == \
                    'Orange API contact'
                assert email_parsed['from'] ==\
                    'Orange API contact <notilus-inbox@contact-everyone.fr>'
                assert email_parsed['from_email'] == \
                    'notilus-inbox@contact-everyone.fr'
                assert email_parsed['cc'] == []
                subj5 = "Orange API : Annule et Remplace, l'Opération de " +\
                    "maintenance Orange API aura lieu le jeudi 26 juillet" +\
                    " au lieu de mercredi 25 juillet"
                assert email_parsed['subject'] == subj5
                assert email_parsed['date'] ==\
                    'Tue, 24 Jul 2012 16:49:56 +0200 (CEST)'
                assert 'des travaux sur son infrastructure' in\
                    email_parsed['html'][0]

            elif msg_num == 6:
                assert email_parsed['from_WHOM'] == \
                    '老张'
                assert '老张' in email_parsed['from']
                assert '<abcdef11@163.com>' in email_parsed['from']
                assert email_parsed['from_email'] == \
                    'abcdef11@163.com'
                assert email_parsed['cc'] == []
                assert email_parsed['subject'] ==\
                    "how to put files in different dirs"
                assert email_parsed['date'] ==\
                    'Wed, 4 Feb 2015 21:48:47 +0800 (CST)'
                assert 'it seems only one entry in stattic-dirs' in\
                    email_parsed['html'][0]

            elif msg_num == 7:
                assert email_parsed['from_WHOM'] == \
                    'Бугрым Андрей'
                assert 'Бугрым Андрей' in email_parsed['from']
                assert '<random555@yandex.ru>' in email_parsed['from']
                assert email_parsed['from_email'] == \
                    'random555@yandex.ru'
                assert email_parsed['cc'] == []
                assert email_parsed['subject'] == "Re: С НОВЫМ 2014 ГОДОМ!!!"
                assert email_parsed['date'] ==\
                    'Sat, 11 Jan 2012 02:16:33 +0400'
                assert 'http://www.sample.us/index/abcd' in\
                    email_parsed['text'][0]['text']

            elif msg_num == 8:
                assert email_parsed['from_WHOM'] == \
                    'Илья Красильщик'
                assert 'Илья Красильщик' in\
                    email_parsed['from']
                assert '<publisher@meduza.io>' in email_parsed['from']
                assert email_parsed['from_email'] == \
                    'publisher@meduza.io'
                assert email_parsed['cc'] == []
                assert email_parsed['subject'] == "Meduza: 20 дней вместе"
                assert email_parsed['date'] ==\
                    'Fri, 01 Nov 2011 16:21:09 +0000 (UTC)'

            elif msg_num == 9:
                assert email_parsed['from_WHOM'] == 'Vladimir'
                assert 'Vladimir <xxxxxxxx@gmail.com>' in\
                    email_parsed['from']
                assert 'Vladimir <xxxxxxxx@gmail.com>' in email_parsed['from']
                assert email_parsed['from_email'] == \
                    'xxxxxxxx@gmail.com'
                assert email_parsed['cc'] == []
                assert email_parsed['subject'] == 'PDF test'
                assert email_parsed['date'] ==\
                    'Tue, 16 Nov 2015 17:20:30 +0200'
                assert len(email_parsed['attachments']) > 0
                assert 'data' in email_parsed['attachments'][0]
                assert email_parsed['attachments'][0]['filename'] ==\
                    'checkerboard.pdf'
                assert email_parsed['attachments'][0]['content_type'] ==\
                    'application/pdf'
