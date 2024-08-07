# -*- coding: utf-8 -*-
"""
    imapy.email_message
    ~~~~~~~~~~~~~~~~~~~

    This module contains EmailMessage class used for parsing email messages
    and passing calls which modify email state to imapy.IMAP() class.

    :copyright: (c) 2015 by Vladimir Goncharov.
    :license: MIT, see LICENSE for more details.
"""
import email
import re
from dataclasses import dataclass
from email.header import decode_header
from enum import Enum, auto
from typing import Any, Dict, List, Optional, Union

from . import utils
from .exceptions import EmailParsingError
from .structures import CaseInsensitiveDict


class EmailParser:
    class EmailContact:
        def __init__(self, name: str, email: str) -> None:
            self.name: str = name
            self.email: str = email

        def __str__(self) -> str:
            return f"{self.name} <{self.email}>"

        def __repr__(self) -> str:
            return f"{self.name} <{self.email}>"

    def parse_email_info(self, info: str) -> "EmailParser.EmailContact":
        match: Optional[re.Match[str]] = re.match(r"(.*?)\s*<(.+)>", info)
        if match:
            name, email = match.groups()
            return self.EmailContact(name.strip(), email.strip())
        else:
            if "@" in info:
                return self.EmailContact("", info.strip())
            raise ValueError("Invalid email format. Expected 'Name <email@domain.com>'")

    def parse_multiple_emails(self, info: str) -> List["EmailParser.EmailContact"]:
        emails = re.split(
            r",\s*(?=\S)", info
        )  # Split by comma followed by any non-whitespace character
        contacts = []
        for em in emails:
            match = re.match(r"(?P<name>.*?)\s*<(?P<email>.+)>", em)
            if match:
                name, em = match.groups()
            else:
                name, em = "", em
            contacts.append(self.EmailContact(name.strip(), em.strip()))
        return contacts


class EmailSender(EmailParser):
    def __init__(self, sender_info: str) -> None:
        self._sender: EmailParser.EmailContact = self.parse_email_info(sender_info)

    @property
    def email(self) -> str:
        return self._sender.email

    @property
    def name(self) -> str:
        return self._sender.name

    def __str__(self) -> str:
        return str(self._sender)

    def __repr__(self) -> str:
        return str(self._sender)


class EmailRecipients(EmailParser):
    def __init__(self, receiver_info: str) -> None:
        self._recipients: List[EmailParser.EmailContact] = self.parse_multiple_emails(
            receiver_info
        )

    def __getitem__(self, index: int) -> EmailParser.EmailContact:
        return self._recipients[index]

    def __len__(self) -> int:
        return len(self._recipients)

    def __iter__(self):
        return iter(self._recipients)

    def __str__(self) -> str:
        return ", ".join(str(receiver) for receiver in self._recipients)

    def __repr__(self) -> str:
        return ", ".join(str(receiver) for receiver in self._recipients)


class EmailFlag(Enum):
    SEEN = auto()
    ANSWERED = auto()
    FLAGGED = auto()
    DELETED = auto()
    DRAFT = auto()
    RECENT = auto()
    UNSEEN = auto()
    UNFLAGGED = auto()


@dataclass
class EmailAttachment:
    """Class for storing email attachaments"""

    filename: str
    data: str
    content_type: str

    def __repr__(self) -> str:
        return f"<{self.filename} ({self.content_type})>"


class EmailMessage:
    """Class for parsing email messages"""

    def __init__(
        self,
        folder: str,
        uid: str,
        flags: List[EmailFlag],
        email_obj: email.message.Message,
        imap_obj: Any,
    ):
        self._folder: str = folder
        self._uid: str = uid
        self._flags: List[EmailFlag] = flags
        self._email_obj: email.message.Message = email_obj
        self._imap_obj: Any = imap_obj
        self.sender: EmailSender
        self.recipients: EmailRecipients
        self._subject: str = ""
        self._cc: List[Dict[str, str]] = []
        self._text: List[Dict[str, Union[str, List[str]]]] = []
        self._html: List[str] = []
        self._headers: CaseInsensitiveDict = CaseInsensitiveDict()
        self._attachments: List[EmailAttachment] = []
        self._date: Optional[str] = None

        self.parse()

    def __repr__(self) -> str:
        return f"{self.sender.email}: {self._subject} ({self._date})"

    @property
    def folder(self) -> str:
        return self._folder

    @folder.setter
    def folder(self, value: str):
        self._folder = value

    @property
    def uid(self) -> str:
        return self._uid

    @uid.setter
    def uid(self, value: str):
        self._uid = value

    @property
    def flags(self) -> List[EmailFlag]:
        return self._flags

    @property
    def subject(self) -> str:
        return self._subject

    @property
    def cc(self) -> List[Dict[str, str]]:
        return self._cc

    @property
    def text(self) -> List[Dict[str, Union[str, List[str]]]]:
        return self._text

    @property
    def html(self) -> List[str]:
        return self._html

    @property
    def headers(self) -> CaseInsensitiveDict:
        return self._headers

    @property
    def attachments(self) -> List[EmailAttachment]:
        return self._attachments

    @property
    def date(self) -> Optional[str]:
        return self._date

    def clean_value(self, value: Any, encoding: Optional[str]) -> str:
        if isinstance(value, bytes):
            if encoding and encoding != "utf-8":
                return value.decode(encoding)
            return utils.b_to_str(value)
        return str(value)

    def _normalize_string(self, text: str) -> str:
        conversion = {"\r\n\t": " ", r"\s+": " "}
        for find, replace in conversion.items():
            text = re.sub(find, replace, text, flags=re.UNICODE)
        return text

    def _get_links(self, text: str) -> List[str]:
        links = set([])
        matches = re.findall(r"(https?://\S+?)(?=\s|$)", text, re.I | re.M)
        if matches:
            for m in matches:
                links.add(m)
        return list(links)

    def mark(self, flags: Union[EmailFlag, List[EmailFlag]]) -> Any:
        if not isinstance(flags, list):
            flags = [flags]
        for flag in flags:
            if flag.name.startswith("UN"):
                if EmailFlag[flag.name[2:]] in self._flags:
                    self._flags.remove(EmailFlag[flag.name[2:]])
            else:
                if flag not in self._flags:
                    self._flags.append(flag)
        return self._imap_obj.mark(flags, self.uid)

    def delete(self) -> Any:
        return self._imap_obj.delete_message(self.uid, self.folder)

    def copy(self, new_mailbox: str) -> Any:
        return self._imap_obj.copy_message(self.uid, new_mailbox, self)

    def move(self, new_mailbox: str) -> Any:
        return self._imap_obj.move_message(self.uid, new_mailbox, self)

    def parse(self) -> None:
        if not self._email_obj.is_multipart():
            text = utils.b_to_str(self._email_obj.get_payload(decode=True)).rstrip()
            self._text.append(
                {
                    "text": text,
                    "text_normalized": self._normalize_string(text),
                    "links": self._get_links(text),
                }
            )
        else:
            for part in self._email_obj.walk():
                if part.get_content_maintype() == "multipart":
                    continue
                content_type = part.get_content_type()
                if content_type == "text/plain":
                    text = utils.b_to_str(part.get_payload(decode=True)).rstrip()
                    self._text.append(
                        {
                            "text": text,
                            "text_normalized": self._normalize_string(text),
                            "links": self._get_links(text),
                        }
                    )
                elif content_type == "text/html":
                    html = utils.b_to_str(part.get_payload(decode=True)).rstrip()
                    self._html.append(html)
                else:
                    try:
                        data = part.get_payload(decode=True)
                    except AssertionError:
                        data = None

                    attachment_fname = decode_header(part.get_filename() or "")
                    filename = self.clean_value(
                        attachment_fname[0][0], attachment_fname[0][1]
                    )

                    self._attachments.append(
                        EmailAttachment(
                            filename=filename, data=data, content_type=content_type
                        )
                    )

        if "subject" in self._email_obj:
            msg_subject = decode_header(self._email_obj["subject"])
            if msg_subject:
                subject_part, encoding = msg_subject[0]
                self._subject = self.clean_value(subject_part, encoding)
            else:
                self._subject = ""

        from_header_cleaned = re.sub(r"[\n\r\t]+", " ", self._email_obj["from"] or "")
        msg_from = decode_header(from_header_cleaned)
        msg_txt = ""
        for part, encoding in msg_from:  # type: ignore
            msg_txt += self.clean_value(part, encoding)

        self.sender = EmailSender(msg_txt)

        if "to" in self._email_obj:
            self.recipients = EmailRecipients(self._email_obj["to"])

        msg_cc = decode_header(str(self._email_obj["cc"]))
        cc_clean = self.clean_value(msg_cc[0][0], msg_cc[0][1])
        if cc_clean and cc_clean.lower() != "none":
            recipients = cc_clean.split(",")
            for recipient in recipients:
                if "<" in recipient and ">" in recipient:
                    matches = re.findall(
                        r"((?P<to>.*)?(?P<to_email>\<.*\>))", recipient, re.U
                    )
                    if matches:
                        for match in matches:
                            self._cc.append(
                                {
                                    "cc": match[0],
                                    "cc_to": match[1].strip(" \n\r\t"),
                                    "cc_email": match[2].strip("<>"),
                                }
                            )
                    else:
                        raise EmailParsingError(
                            f"Error parsing CC message header. "
                            f"Header value: {cc_clean}"
                        )
                else:
                    self._cc.append(
                        {
                            "cc": recipient,
                            "cc_to": recipient,
                            "cc_email": recipient,
                        }
                    )

        self._date = self._email_obj["Date"]

        for header, val in self._email_obj.items():
            if header in self._headers:
                self._headers[header].append(val)
            else:
                self._headers[header] = [val]
