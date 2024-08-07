# -*- coding: utf-8 -*-
"""
    imapy.mail_folder
    ~~~~~~~~~~~~~~~~~

    This module contains MailFolder class used to encapsulate
    some of functionality for parsing and representing email
    folder(s) structure.

    :copyright: (c) 2015 by Vladimir Goncharov.
    :license: MIT, see LICENSE for more details.
"""

import re
from dataclasses import dataclass, field
from typing import Any, Dict, List, Tuple

from . import utils
from .exceptions import EmailFolderParsingError


@dataclass
class MailFolder:
    """Class for email folder operations"""

    folders: List[str] = field(default_factory=list)
    folders_tree: Dict[str, Any] = field(default_factory=dict)
    children: Dict[str, List[str]] = field(default_factory=dict)
    separator: str = field(init=False)
    raw_folders: List[Any] = field(init=False)
    folder_parts: re.Pattern = field(init=False)

    def __post_init__(self):
        self.folder_parts = re.compile(
            r"""
            # name attributes
            \(?(?P<attributes>.*?)?(?<!\\)\)\s?
            # separator
            \"(?P<separator>.*?)\"\s
            # inbox name with/without separator
            \"?(?P<name>.*?)\"?$
            """,
            re.VERBOSE,
        )

    def get_folders(self, *args: Tuple[Any, List[Any]]) -> List[str]:
        """Return list of found folders"""
        self.raw_folders = args[0][1]
        # get dictionary holding folders info
        self.folders_tree, self.children = self._get_folders_tree_and_children(
            self.raw_folders
        )
        return self.folders

    def get_children(self, folder_name: str) -> List[str]:
        """Returns list of subfolders for current folder"""
        return self.children.get(folder_name, [])

    def get_separator(self) -> str:
        """Return hierarchy separator"""
        return self.separator

    def _get_folders_tree_and_children(
        self, raw_folders: List[Any]
    ) -> Tuple[Dict[str, Any], Dict[str, List[str]]]:
        """Construct Folders tree and dictionary holding folder children"""
        obj_list: Dict[str, Any] = {}
        self.folders = []
        max_depth = 0

        for raw_folder in raw_folders:
            if not raw_folder:
                continue

            if isinstance(raw_folder, tuple):
                len_suffix = "{%d}" % len(raw_folder[1])
                raw_folder = raw_folder[0][: -len(len_suffix)] + raw_folder[1]

            raw_folder = utils.utf7_to_unicode(raw_folder)
            match = self.folder_parts.match(raw_folder)
            if not match:
                raise EmailFolderParsingError("Couldn't parse folder info.")

            attributes = [a.lstrip("\\") for a in match.group("attributes").split()]
            self.separator = utils.to_unescaped_str(match.group("separator"))
            full_name = match.group("name")
            name = full_name.split(self.separator)[-1]

            parent_name = ""
            if self.separator in full_name:
                parent_parts = full_name.split(self.separator)
                parent_name = self.separator.join(parent_parts[:-1])

            depth = full_name.count(self.separator)
            max_depth = max(max_depth, depth)

            self.folders.append(full_name)

            obj_list[full_name] = {
                "full_name": full_name,
                "name": name,
                "standard_attributes": attributes.copy(),
                "full_attributes": attributes,
                "children": {},
                "parent_name": parent_name,
                "depth": depth,
            }

        tree, children = self._create_tree_and_children(max_depth, obj_list)
        return tree, children

    def get_parent_name(self, folder_name: str) -> str:
        """Returns name of a parent folder or itself if it is already topmost folder."""
        if self.separator not in folder_name:
            return folder_name
        parent_parts = folder_name.split(self.separator)[:-1]
        return self.separator.join(parent_parts)

    def _create_tree_and_children(
        self, max_depth: int, obj_list: Dict[str, Any]
    ) -> Tuple[Dict[str, Any], Dict[str, List[str]]]:
        """Returns folders merged into tree-like dictionary and dictionary containing the children of each folder"""
        result: Dict[str, Any] = {}
        children: Dict[str, List[str]] = {}

        for current_depth in range(max_depth + 1):
            for folder_name, folder_info in obj_list.items():
                if folder_info["depth"] == current_depth:
                    parent_name = folder_info["parent_name"]
                    if parent_name:
                        path = result
                        for i, name in enumerate(folder_name.split(self.separator)):
                            local_name = self.separator.join(
                                folder_name.split(self.separator)[: i + 1]
                            )
                            if (
                                name != self.separator
                                and name not in path
                                and local_name in obj_list
                            ):
                                path[name] = obj_list[local_name]
                            if name in path:
                                path = path[name]["children"]
                        if parent_name in children:
                            children[parent_name].append(folder_name)
                            children[folder_name] = []
                    else:
                        result[folder_name] = folder_info
                        children[folder_name] = []

        return result, children

    def __repr__(self) -> str:
        return str(self.folders)
