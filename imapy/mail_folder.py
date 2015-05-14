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
from . import utils
from .exceptions import (EmailFolderParsingError)


class MailFolder():
    """Class for email folder operations"""

    def __init__(self):
        """Initialize vars"""
        # list holding folder names
        self.folders = []
        self.folders_tree = {}
        self.children = {}
        # prepare regexp
        # (\\HasNoChildren) "/" "Bulk Mail"
        # (\HasNoChildren \Drafts) "." Drafts
        self.folder_parts = re.compile(
            r'''
            # name attributes
            \(?(?P<attributes>.*?)?(?<!\\)\)\s?
            # separator
            \"(?P<separator>.*?)\"\s
            # inbox name with/without separator
            \"?(?P<name>.*?)\"?$
            ''', re.VERBOSE)

    def get_folders(self, *args):
        """Return list of found folders"""
        self.raw_folders = args[0][1]
        # get dictionary holding folders info
        self.folders_tree, self.children = self._get_folders_tree_and_children(
            self.raw_folders)
        return self.folders

    def get_children(self, folder_name):
        """Returns list of subfolders for current folder"""
        if folder_name in self.children:
            return self.children[folder_name]
        return []

    def get_separator(self):
        """Return hierarchy separator """
        return self.separator

    def _get_folders_tree_and_children(self, raw_folders):
        """Construct Folders tree and dictionary holding folder children"""
        obj_list = {}
        self.folders = []
        """setup maximum depth for a folder
           (used later while merging objects into one)
        """
        max_depth = 0
        for raw_folder in raw_folders:
            # get name attributes, hierarchy delimiter, name
            # decode folder name
            raw_folder = utils.utf7_to_unicode(raw_folder)
            match = self.folder_parts.match(raw_folder)
            if not match:
                raise EmailFolderParsingError("Couldn't parse folder info.")

            # create objects
            """
            Example of format we use:
            "[Gmail]":
                # name without path
                'name':'[Gmail]',
                # name with path
                'full_name':'[Gmail]',
                # only attributes defined in RFC3501
                # '\' is skipped from the start of attributes
                'standard_attributes': ['HasChildren', 'Noselect'],
                # custom attributes (all the attributes we've found)
                'full_attributes':['HasChildren', 'Noselect']
                'children':{}, # empty dict or dict with objects like this
                'parent_name':False,
                'depth':0, # how deep the folder is (zero is the root)
            """
            # box attributes
            attributes = match.group('attributes').split()
            attributes = [a.lstrip('\\') for a in attributes]
            # separator
            self.separator = utils.to_str(match.group('separator'))
            # full name (unique identifier for mailbox)
            full_name = match.group('name')
            # full name with no path part
            name = full_name.split(self.separator).pop()
            # parent's name
            parent_name = False
            if full_name.count(self.separator):
                parent_parts = full_name.split(self.separator)
                parent_name = self.separator.join(
                    [i for i in parent_parts[:-1]]
                )
            # depth
            depth = full_name.count(self.separator)
            if depth > max_depth:
                max_depth = depth

            # add folder name to list of folders
            self.folders.append(utils.to_str(full_name))

            # add to object dictionary
            obj_list[full_name] = {
                'full_name': full_name,
                'name': name,
                # TODO -- add only standard values
                'standard_attributes': [attr for attr in attributes],
                'full_attributes': attributes,
                # this later is updated while merging objects later
                'children': {},
                'parent_name': parent_name,
                'depth': depth
            }

        # Merge objects into one and create children dict
        tree, children = self._create_tree_and_children(
            max_depth, obj_list)

        return tree, children

    def get_parent_name(self, folder_name):
        """Returns name of a parent folder or itself if it is already topmost
        folder.
        """
        if self.separator not in folder_name:
            return folder_name
        parent_parts = folder_name.split(self.separator)[:-1]
        return self.separator.join([str(i) for i in parent_parts])

    def _create_tree_and_children(self, max_depth, obj_list):
        """Returns 2 things:
        1) Folders merged into tree-like dictionary
        2) Dictionary containing the children of each folder
        """
        current_depth = 0
        result = {}
        children = {}
        while current_depth <= max_depth:
            for folder_name in obj_list:
                # add only folders from current depth
                if obj_list[folder_name]['depth'] == current_depth:
                    # does it has a parent ?
                    parent_name = obj_list[folder_name]['parent_name']
                    if parent_name:
                        # create subtree in result
                        name = ''
                        path = result
                        for i, name in enumerate(
                                folder_name.split(self.separator)):
                            local_name_parts = folder_name.split(
                                self.separator)[:i + 1]
                            local_name = self.separator.join(
                                [s for s in local_name_parts])
                            if name != self.separator:
                                if name not in path:
                                    """ Additional check for Dovecot which can have subfolder
                                    without a parent folder
                                    """
                                    if local_name in obj_list:
                                        path[name] = obj_list[local_name]
                            # nonexistent parent check (Dovecot)
                            if name in path:
                                path = path[name]['children']
                        # nonexistent parent check (Dovecot)
                        if parent_name in children:
                            # add to children
                            children[parent_name].append(folder_name)
                            children[folder_name] = []
                    else:
                        # just add
                        result[folder_name] = obj_list[folder_name]
                        # add to children
                        children[folder_name] = []
            current_depth += 1

        return result, children

    def __repr__(self):
        return str(self.folders)
