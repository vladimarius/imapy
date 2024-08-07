# -*- coding: utf-8 -*-
"""
    imapy.imap
    ~~~~~~~~~~

    Core Imapy module which encapsulates most of its functionality.

    :copyright: (c) 2015 by Vladimir Goncharov.
    :license: MIT, see LICENSE for more details.
"""

import email
import imaplib
import re
import socket
from dataclasses import dataclass, field
from email.mime.base import MIMEBase
from typing import Any, Dict, List, Optional, Union

from . import utils
from .email_message import EmailFlag, EmailMessage
from .exceptions import (
    ConnectionRefused,
    ImapyLoggedOut,
    InvalidFolderName,
    InvalidHost,
    InvalidSearchQuery,
    NonexistentFolderError,
    TagNotSupported,
    UnknownEmailMessageType,
)
from .mail_folder import MailFolder
from .query_builder import Q


def is_logged(func):
    """Decorator used to check whether the user is logged in
    while sending commands to IMAP server
    """

    def wrapper(*args, **kwargs):
        if args[0].logged_in:
            return func(*args, **kwargs)
        else:
            raise ImapyLoggedOut("Trying to send commands after logging out.")

    return wrapper


def refresh_folders(func):
    """Decorator used to refresh folder tree during operations
    involving changing folder name(s) or structure
    """

    def wrapper(*args, **kwargs):
        f = func(*args, **kwargs)
        args[0]._update_folder_info()
        return f

    return wrapper


@dataclass
class IMAP:
    """Class used for interfacing between"""

    # Connection settings
    host: str
    username: str
    password: str
    ssl: bool = True
    auth_mechanism: Optional[str] = None
    auth_object: Any = None
    debug_level: int = 0
    port: int = 0

    capabilities: List[str] = field(default_factory=list)
    separator: Optional[str] = None
    folder_capabilities: Dict[str, List[str]] = field(default_factory=dict)

    # email flags
    standard_rw_flags: List[EmailFlag] = field(
        default_factory=lambda: [
            EmailFlag.SEEN,
            EmailFlag.ANSWERED,
            EmailFlag.FLAGGED,
            EmailFlag.DELETED,
            EmailFlag.DRAFT,
        ]
    )
    standard_r_flags: List[EmailFlag] = field(
        default_factory=lambda: [EmailFlag.RECENT]
    )
    standard_flags: List[EmailFlag] = field(init=False)

    # folders
    selected_folder: Optional[str] = None
    selected_folder_utf7: Optional[bytes] = None
    mail_folder_class: MailFolder = field(default_factory=MailFolder)

    # email parsing
    msg_class = EmailMessage

    operating_folder: Optional[str] = None
    logged_in: bool = False
    imap: Union[imaplib.IMAP4, imaplib.IMAP4_SSL] = field(init=False)

    # default ports
    IMAP4_SSL_PORT: int = 993
    IMAP4_PORT: int = 143

    def __post_init__(self):
        if not self.port:
            self.port = self.IMAP4_SSL_PORT if self.ssl else self.IMAP4_PORT

        if self.ssl:
            self.imap = imaplib.IMAP4_SSL(self.host, port=self.port)
        else:
            self.imap = imaplib.IMAP4(self.host, port=self.port)
        self.standard_flags = self.standard_rw_flags + self.standard_r_flags
        self.connect()

    def __enter__(self):
        return self

    def __exit__(self, type, value, traceback):
        self.logout()

    def __str__(self) -> str:
        return f'"{self.selected_folder}"'

    def __repr__(self) -> str:
        return f'"{self.selected_folder}"'

    def logout(self) -> None:
        """Log out"""
        # expunge selected folder if selected
        if self.selected_folder:
            self.imap.close()
        self.imap.logout()
        # cleanup vars
        self.selected_folder = self.selected_folder_utf7 = None
        self.logged_in = False

    def log_out(self) -> None:
        """Log out alias function"""
        self.logout()

    @is_logged
    def folders(self, search_string: Optional[str] = None) -> List[str]:
        """Return list of email all folders or folder names matching
        the search string
        """
        if search_string:
            # search folders folders
            regexp = ""
            parts = re.split(r"(?<!\\)\*", search_string)
            total = len(parts)
            for i, p in enumerate(parts):
                if p:
                    regexp += re.escape(p)
                    if (i + 1) < total:
                        regexp += ".*"
                else:
                    if (i + 1) < total:
                        regexp += ".*"
            folders = []
            for f in self.mail_folders:
                real_name = f.split(self.separator).pop()
                if re.match("^" + regexp + "$", real_name):
                    folders.append(f)
            return folders
        else:
            if hasattr(self, "mail_folders"):
                return self.mail_folders
            self._update_folder_info()
        return self.mail_folders

    @is_logged
    def folder(self, folder_name: str = "") -> "IMAP":
        """Sets folder for folder-related operations. If folder_name is omitted
        then operations will be carried on topmost folder level."""
        if folder_name:
            if folder_name not in self.mail_folders:
                raise NonexistentFolderError(
                    f"The folder you are trying to select ({folder_name}) doesn't exist. Hint: try getting list of available folders via `em.folders()`"
                )
            if self.selected_folder:
                self.imap.close()
            self.selected_folder = folder_name
            self.selected_folder_utf7 = utils.str_to_utf7(self.selected_folder)
            if self.selected_folder_utf7 is not None:
                self.imap.select('"' + self.selected_folder_utf7.decode() + '"')
            self._save_folder_capabilities(self.selected_folder)
        else:
            if self.selected_folder:
                self.imap.close()
            self.selected_folder = self.selected_folder_utf7 = None
        return self

    def _save_folder_capabilities(self, folder_name: str) -> None:
        """Saves folder capabilities in class variable if not present"""

        if folder_name not in self.folder_capabilities:
            _response, result = self.imap.capability()
            self.folder_capabilities[folder_name] = result[0].upper().split()

    def _update_folder_info(self) -> None:
        """Updates internal information about email folder structure"""
        raw_folders = self.imap.list()
        self.mail_folders = self.mail_folder_class.get_folders(raw_folders)
        self.separator = self.mail_folder_class.get_separator()

    @is_logged
    def children(self) -> List[str]:
        """Returns list of folder subfolders"""
        if not self.selected_folder:
            return []
        children = self.mail_folder_class.get_children(utils.u(self.selected_folder))
        return [c for c in children]

    @is_logged
    def parent(self) -> "IMAP":
        """Selects folder for folder operations which is a parent of a current
        folder.
        """
        if self.selected_folder:
            self.selected_folder = self.mail_folder_class.get_parent_name(
                self.selected_folder
            )
            if self.selected_folder:
                self.selected_folder_utf7 = utils.str_to_utf7(self.selected_folder)
        return self

    def connect(self) -> "IMAP":
        if not self.host:
            raise InvalidHost("Host is required for connection")

        try:
            self.imap.debug = self.debug_level

            if self.auth_mechanism:
                if self.auth_object is None:
                    raise ValueError(
                        "auth_object is required when using auth_mechanism"
                    )
                self.imap.authenticate(self.auth_mechanism, self.auth_object)
            else:
                if not self.username or not self.password:
                    raise ValueError(
                        "Both username and password are required for login"
                    )
                self.imap.login(self.username, self.password)

        except socket.error as e:
            raise ConnectionRefused(str(e))

        self.logged_in = True
        self.capabilities = list(self.imap.capabilities)
        self._update_folder_info()
        return self

    @is_logged
    def append(self, message: MIMEBase, **kwargs) -> "IMAP":
        """Append message to the end of mailbox folder."""
        # create flags string '(\Seen \Flagged)'
        flags: Optional[List[EmailFlag]] = kwargs.pop("flags", None)
        if flags:
            good_flags = list(set(flags) & set(self.standard_rw_flags))
            if good_flags:
                flags_str = "(\\" + " \\".join(f.name for f in good_flags) + ")"
            else:
                flags_str = ""
        else:
            flags_str = ""

        date_time: Optional[str] = kwargs.pop("date_time", None)

        # detect message type
        if isinstance(message, MIMEBase):
            msg = message.as_string()
        else:
            raise UnknownEmailMessageType(
                "Message should be a subclass of email.mime.base.MIMEBase"
            )

        self.imap.append(
            '"' + utils.b_to_str(self.selected_folder_utf7) + '"',
            flags_str,
            date_time or "",
            msg,
        )

        return self

    def email(self, sequence_number: int) -> Optional[EmailMessage]:
        """Helper function for self.emails(). Returns email by its
        sequence number
        """
        emails = self.emails(sequence_number, sequence_number)
        if emails:
            return emails[0]
        return None

    @is_logged
    def emails(self, *args, **kwargs) -> Union[List[EmailMessage], List[str]]:
        """Returns emails based on search criteria or sequence set"""
        ids_only: bool = kwargs.get("ids_only", False)
        if len(args) > 2:
            raise InvalidSearchQuery("emails() method accepts maximum 2 parameters.")
        elif len(args) == 2:
            if not isinstance(args[0], int) or not isinstance(args[1], int):
                raise InvalidSearchQuery(
                    "emails() method accepts 2 integers as parameters."
                )
            if args[1] < 0:
                raise InvalidSearchQuery(
                    "emails() method second parameter cannot be negative."
                )
            return self._get_emails_by_sequence(args[0], args[1], ids_only=ids_only)
        elif len(args) == 1:
            if isinstance(args[0], Q):
                query = args[0]
                if self.selected_folder:
                    query.capabilities = self.folder_capabilities.get(
                        self.selected_folder, []
                    )
                use_query = query.get_query()

                # call search
                if self.imap:
                    if query.non_ascii_params:
                        # search using charset
                        old_literal = self.imap.literal
                        self.imap.literal = utils.str_to_b(query.non_ascii_params[0])
                        _, data = self.imap.uid("SEARCH", *use_query)
                        self.imap.literal = old_literal
                    else:
                        _, data = self.imap.uid("SEARCH", *use_query)

                    if data and data[0]:
                        uids = utils.b_to_str(data[0]).split()
                        return self._fetch_emails_info(uids)
                return []
            elif isinstance(args[0], int):
                return self._get_emails_by_sequence(args[0], ids_only=ids_only)
            else:
                raise InvalidSearchQuery(
                    "Please construct query using query_"
                    "builder Q class or call emails() "
                    "method with integers as parameters."
                )
        else:
            # no parameters - fetch all emails in folder
            return self._get_emails_by_sequence(ids_only=ids_only)

    def _get_emails_by_sequence(
        self,
        from_id: Optional[int] = None,
        to_id: Optional[int] = None,
        ids_only: bool = False,
    ) -> Union[List[EmailMessage], List[str]]:
        """Returns emails fetched by their sequence numbers."""
        from_seq = from_id
        to_seq = to_id
        status = self.info()
        total = status["total"] or 0
        if not total:
            return []
        if from_id is not None and from_id < 0:
            from_seq = total + from_id + 1
            if to_id is not None:
                raise InvalidSearchQuery(
                    "Invalid use of parameters: accepting only 1 parameter "
                    "when sequence start is negative."
                )
        if from_id is None:
            from_seq = 1
        if to_id is None:
            to_seq = total

        if self.imap:
            _, data = self.imap.fetch(
                f"{max(from_seq or 1, 1)}:{max(to_seq or 1, 1)}", "(UID)"
            )

            if isinstance(data, list) and data:
                uids = []
                for inputs in data:
                    match = re.search(r"UID (\d+)", utils.b_to_str(inputs))
                    if match:
                        uids.append(match.group(1))
                if ids_only:
                    return [uid for uid in uids]
                else:
                    return self._fetch_emails_info(uids)
        return []

    @is_logged
    def _fetch_emails_info(self, email_uids: List[str]) -> List[EmailMessage]:
        """Fetches email info from server and returns as parsed email
        objects
        """
        emails = []
        # fetch email without changing 'Seen' state
        if self.imap and len(email_uids) > 0:
            uids = ",".join(email_uids)
            _result, data = self.imap.uid("FETCH", uids, "(FLAGS BODY.PEEK[])")
            if data:
                total = len(data)
                for i, inputs in enumerate(data):
                    if isinstance(inputs, tuple):
                        email_id, raw_email = inputs
                        # Check for email flags/uid added after email contents
                        if (i + 1) < total and isinstance(data[i + 1], bytes):
                            email_id += b" " + data[i + 1]
                        email_id_str = utils.b_to_str(email_id)
                        raw_email_str = utils.b_to_str(raw_email)
                        # get UID
                        uid_match = re.match(r".*UID (?P<uid>[0-9]+)", email_id_str)
                        uid = uid_match.group("uid") if uid_match else ""
                        # get FLAGS
                        flags = []
                        flags_match = re.match(
                            r".*FLAGS \((?P<flags>.*?)\)", email_id_str
                        )
                        # cleanup standard tags
                        if flags_match:
                            for f in flags_match.group("flags").split():
                                flag_name = f.upper().lstrip("\\")
                                if flag_name in EmailFlag.__members__:
                                    flags.append(EmailFlag[flag_name])
                                else:
                                    flags.append(f)
                        email_obj = email.message_from_string(raw_email_str)
                        email_parsed = self.msg_class(
                            folder=self.selected_folder or "",
                            uid=uid,
                            flags=flags,
                            email_obj=email_obj,
                            imap_obj=self,
                        )
                        emails.append(email_parsed)

        return emails

    @is_logged
    def mark(self, tags: Union[EmailFlag, List[EmailFlag]], uid: str) -> None:
        """Adds or removes standard IMAP flags to message identified by UID"""
        add_tags = []
        remove_tags = []
        if not isinstance(tags, list):
            tags = [tags]
        for t in tags:
            if isinstance(t, EmailFlag):
                tag_clean = t.name
                if tag_clean.startswith("UN"):
                    compare_tag = EmailFlag[tag_clean[2:]]
                    remove_tags.append(compare_tag)
                else:
                    compare_tag = t
                    add_tags.append(t)

                if compare_tag not in self.standard_rw_flags:
                    allowed_mark = self.standard_rw_flags
                    allowed_unmark = [
                        EmailFlag[f"UN{t.name}"]
                        for t in self.standard_rw_flags
                        if f"UN{t.name}" in EmailFlag.__members__
                    ]
                    allowed = ", ".join(str(i) for i in allowed_mark + allowed_unmark)
                    raise TagNotSupported(
                        f'Using "{t}" tag to mark email '
                        f"message is not supported. Please use one "
                        f"of the following: {allowed}"
                    )

        # add tags
        if add_tags and self.imap:
            tag_list = " ".join(f"\\{t.name}" for t in add_tags)
            self.imap.uid("STORE", uid, "+FLAGS", f"({tag_list})")
        # remove tags
        if remove_tags and self.imap:
            tag_list = " ".join(f"\\{t.name}" for t in remove_tags)
            self.imap.uid("STORE", uid, "-FLAGS", f"({tag_list})")
        self._restore_operating_folder()

    def _restore_operating_folder(self) -> None:
        """Selects operating folder"""
        if self.operating_folder:
            self.folder(self.operating_folder)
            self.operating_folder = None

    def make(self, folder_name: Union[str, List[str]]) -> "IMAP":
        """Alias for make_folder() function"""
        return self.make_folder(folder_name)

    @refresh_folders
    @is_logged
    def make_folder(self, folder_name: Union[str, List[str]]) -> "IMAP":
        """
        Creates mailbox subfolder with a given name under currently
        selected folder.
        """
        if isinstance(folder_name, str):
            names = [folder_name]
        else:
            names = folder_name

        for n in names:
            if self.separator and self.separator in n:
                raise InvalidFolderName(
                    f"Folder name cannot contain separator symbol: {self.separator}"
                )
            parent_path = ""
            if self.selected_folder:
                parent_path = self.selected_folder + (self.separator or "")
            name = utils.str_to_utf7('"' + utils.u(parent_path) + utils.u(n) + '"')
            if self.imap and name is not None:
                self.imap.create(name.decode())

        return self

    @is_logged
    def copy_message(
        self, uid: str, mailbox: str, msg_instance: EmailMessage
    ) -> EmailMessage:
        """Copy message with specified UID onto end of new_mailbox."""
        if self.imap:
            self.imap.uid(
                "COPY", uid, '"' + utils.str_to_utf7(utils.u(mailbox)).decode() + '"'
            )
            copy_uid_data = self.imap.untagged_responses.get("COPYUID", [])
            for i, val in reversed(list(enumerate(copy_uid_data[:]))):
                if isinstance(val, str):
                    _, original_uid, target_uid = val.split()
                    if int(uid) == int(original_uid):
                        del copy_uid_data[i]
                        msg_instance.uid = target_uid
                        msg_instance.folder = mailbox
                        self.operating_folder = self.selected_folder
                        self.folder(mailbox)
                        break

        return msg_instance

    @is_logged
    def move_message(
        self, uid: str, mailbox: str, msg_instance: EmailMessage
    ) -> EmailMessage:
        """Move message with specified UID onto end of new_mailbox."""
        msg_folder = self.selected_folder
        self.copy_message(uid, mailbox, msg_instance)
        self.delete_message(uid, msg_folder)
        return msg_instance

    @is_logged
    def delete_message(self, uid: str, folder: str) -> None:
        """Deletes message with specified UID and folder"""
        if folder != self.selected_folder:
            self.folder(folder)
        self.imap.uid("STORE", uid, "+FLAGS", f"({EmailFlag.DELETED.name})")
        self._restore_operating_folder()

    @is_logged
    def info(self) -> Dict[str, Optional[int]]:
        """Request named status conditions for mailbox."""
        info: Dict[str, Optional[int]] = {
            "total": None,
            "recent": None,
            "unseen": None,
            "uidnext": None,
            "uidvalidity": None,
        }
        if self.selected_folder_utf7 and self.imap:
            _status, result = self.imap.status(
                '"' + self.selected_folder_utf7.decode() + '"',
                "(MESSAGES RECENT UIDNEXT UIDVALIDITY UNSEEN)",
            )
            if result and isinstance(result[0], bytes):
                where = result[0].decode()
                messages = re.search(r"MESSAGES ([0-9]+)", where)
                if messages:
                    info["total"] = int(messages.group(1))
                recent = re.search(r"RECENT ([0-9]+)", where)
                if recent:
                    info["recent"] = int(recent.group(1))
                unseen = re.search(r"UNSEEN ([0-9]+)", where)
                if unseen:
                    info["unseen"] = int(unseen.group(1))
                uidnext = re.search(r"UIDNEXT ([0-9]+)", where)
                if uidnext:
                    info["uidnext"] = int(uidnext.group(1))
                uidvalidity = re.search(r"UIDVALIDITY ([0-9]+)", where)
                if uidvalidity:
                    info["uidvalidity"] = int(uidvalidity.group(1))

        return info

    @refresh_folders
    @is_logged
    def rename(self, folder_name: str) -> "IMAP":
        """Renames currently selected folder"""
        sep = self.separator
        folder_name = utils.u(folder_name)
        if (
            sep is not None
            and folder_name
            and (sep in (self.selected_folder or ""))
            and (sep not in folder_name)
        ):
            folder_path = (self.selected_folder or "").split(sep)[:-1]
            folder_name = sep.join(folder_path) + sep + folder_name

        folder_to_rename = self.selected_folder_utf7
        if folder_to_rename and self.imap:
            new_name = utils.str_to_utf7(folder_name)
            """
            Return to authenticated state. That's because some imap servers
            (like outlook.com) cannot rename currently selected folder & return
            "NO [CANNOT] Cannot rename selected folder." response
            """
            self.folder()
            self.imap.rename(
                '"' + folder_to_rename.decode() + '"', '"' + new_name.decode() + '"'
            )
            self._update_folder_info()
            self.folder(utils.b_to_str(new_name))

        return self

    @refresh_folders
    @is_logged
    def delete(self, folder_names: Optional[Union[str, List[str]]] = None) -> "IMAP":
        """Deletes list of specified folder names or currently selected
        folder and returns to authenticated state if currently selected
        folder is being deleted.
        """
        if folder_names:
            if isinstance(folder_names, str):
                folder_names = [folder_names]
            if self.selected_folder in folder_names:
                self.folder()
            for f_name in folder_names:
                if self.imap:
                    self.imap.delete(
                        '"' + utils.str_to_utf7(utils.u(f_name)).decode() + '"'
                    )
        else:
            current_folder = self.selected_folder_utf7
            if current_folder and self.imap:
                self.folder()
                self.imap.delete('"' + current_folder.decode() + '"')
        return self
