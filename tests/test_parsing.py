import email
from pathlib import Path

from imapy import utils
from imapy.email_message import EmailMessage

MESSAGES_FOLDER = Path("test_emails")


def test_parsing_sample_emails():
    # check parsing sample emails (msg1, msg2 ...)
    fnames = MESSAGES_FOLDER.iterdir()
    for fn in fnames:
        if fn.suffix == ".msg":
            with fn.open("rb") as f:
                raw_email = f.read()
            email_obj = email.message_from_string(utils.b_to_str(raw_email))
            email_parsed = EmailMessage(
                folder="no_folder",
                uid=999,
                flags=[],
                email_obj=email_obj,
                imap_obj=None,
            )
            msg_num = int(fn.stem)

            if msg_num == 1:
                assert str(email_parsed.sender) == "Dropbox <no-reply@dropboxmail.com>"
                assert email_parsed.sender.name == "Dropbox"
                assert email_parsed.sender.email == "no-reply@dropboxmail.com"
                assert email_parsed.cc == []
                assert (
                    email_parsed.subject
                    == "Update: Changes to better serve our users around the world"
                )
                assert email_parsed.date == "Sat, 2 May 2015 13:46:01 +0000"
                assert (
                    "outside of North America"
                    in email_parsed.text[0]["text_normalized"]
                )
                assert len(email_parsed.html) > 0

            elif msg_num == 2:
                assert (
                    str(email_parsed.sender)
                    == "Надежда ДранинаfS (via Twitter) <notify@twitter.com>"
                )
                assert email_parsed.sender.name == "Надежда ДранинаfS (via Twitter)"
                assert email_parsed.sender.email == "notify@twitter.com"
                assert email_parsed.cc == []
                assert (
                    email_parsed.subject
                    == "Надежда ДранинаfS (@dranina73) is now following you on Twitter!"
                )
                assert email_parsed.date == "Wed, 22 Apr 2015 05:00:36 +0000"
                assert (
                    "You have a new follower on"
                    in email_parsed.text[0]["text_normalized"]
                )
                assert len(email_parsed.html) > 0

            elif msg_num == 3:
                assert str(email_parsed.sender) == '"USPS" <no-reply@usps.com>'
                assert email_parsed.sender.name == '"USPS"'
                assert email_parsed.sender.email == "no-reply@usps.com"
                assert email_parsed.cc == []
                assert (
                    email_parsed.subject
                    == "Shipment status change for package # 23696393"
                )
                assert email_parsed.date == "Thu, 30 Apr 2015 09:32:16 -0700"
                assert (
                    "The package could not be delivered"
                    in email_parsed.text[0]["text_normalized"]
                )
                assert len(email_parsed.html) == 0

            elif msg_num == 4:
                assert (
                    str(email_parsed.sender)
                    == "François Schiettecatte <fschiettecatte@gmail.com>"
                )
                assert email_parsed.sender.name == "François Schiettecatte"
                assert email_parsed.sender.email == "fschiettecatte@gmail.com"
                assert email_parsed.cc == []
                assert email_parsed.subject == "Re: Require code explaination"
                assert email_parsed.date == "Wed, 29 Apr 2015 09:46:37 -0400"
                assert (
                    "Django does not implement X-Accel-Redirect"
                    in email_parsed.text[0]["text_normalized"]
                )
                assert len(email_parsed.html) == 0

            elif msg_num == 5:
                assert (
                    str(email_parsed.sender)
                    == "Orange API contact <notilus-inbox@contact-everyone.fr>"
                )
                assert email_parsed.sender.name == "Orange API contact"
                assert email_parsed.sender.email == "notilus-inbox@contact-everyone.fr"
                assert email_parsed.cc == []
                assert (
                    email_parsed.subject
                    == "Orange API : Annule et Remplace, l'Opération de maintenance Orange API aura lieu le jeudi 26 juillet au lieu de mercredi 25 juillet"
                )
                assert email_parsed.date == "Tue, 24 Jul 2012 16:49:56 +0200 (CEST)"
                assert "des travaux sur son infrastructure" in email_parsed.html[0]

            elif msg_num == 6:
                assert str(email_parsed.sender) == "老张 <abcdef11@163.com>"
                assert email_parsed.sender.name == "老张"
                assert email_parsed.sender.email == "abcdef11@163.com"
                assert email_parsed.cc == []
                assert email_parsed.subject == "how to put files in different dirs"
                assert email_parsed.date == "Wed, 4 Feb 2015 21:48:47 +0800 (CST)"

            elif msg_num == 7:
                assert str(email_parsed.sender) == "Бугрым Андрей <random555@yandex.ru>"
                assert email_parsed.sender.name == "Бугрым Андрей"
                assert email_parsed.sender.email == "random555@yandex.ru"
                assert email_parsed.cc == []
                assert email_parsed.subject == "Re: С НОВЫМ 2014 ГОДОМ!!!"
                assert email_parsed.date == "Sat, 11 Jan 2012 02:16:33 +0400"

            elif msg_num == 8:
                assert (
                    str(email_parsed.sender) == "Илья Красильщик <publisher@meduza.io>"
                )
                assert email_parsed.sender.name == "Илья Красильщик"
                assert email_parsed.sender.email == "publisher@meduza.io"

                assert email_parsed.cc == []
                assert email_parsed.subject == "Meduza: 20 дней вместе"
                assert email_parsed.date == "Fri, 01 Nov 2011 16:21:09 +0000 (UTC)"

            elif msg_num == 9:
                assert str(email_parsed.sender) == "Vladimir <xxxxxxxx@gmail.com>"
                assert email_parsed.sender.name == "Vladimir"
                assert email_parsed.sender.email == "xxxxxxxx@gmail.com"

                assert email_parsed.cc == []
                assert email_parsed.subject == "PDF test"
                assert email_parsed.date == "Tue, 16 Nov 2015 17:20:30 +0200"

                assert len(email_parsed.attachments) > 0
                assert hasattr(email_parsed.attachments[0], "data")
                assert email_parsed.attachments[0].filename == "checkerboard.pdf"
                assert email_parsed.attachments[0].content_type == "application/pdf"
