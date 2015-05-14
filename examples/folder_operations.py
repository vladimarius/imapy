# -*- encoding: utf-8 -*-
"""
Shows some folder operations with Imapy
"""

import imapy

box = imapy.connect(
    host='host',
    username='username',
    password='password',
    ssl=True,
)

# get all folder names
folders = box.folders()

# Create folder
box.folder().make_folder('Imapy')

# Create subfolders
# (note how you can pass several folder names in a list)
box.folder('Imapy').make_folder(['Imapy subfolder', 'Kamikaze folder'])

# Rename subfolder
subfolder_name = 'Imapy' + box.separator + 'Imapy subfolder'
box.folder(subfolder_name).rename('My precious')

# Delete
delete_name = 'Imapy' + box.separator + 'Kamikaze folder'
box.folder(delete_name).delete()

# logout
box.logout()
