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

# Get list of children names of a folder
children = box.folder('Imapy').children()
for c in children:
    print("{0} is a child of 'Imapy' folder".format(c))

# Rename subfolder
subfolder_name = 'Imapy' + box.separator + 'Imapy subfolder'
box.folder(subfolder_name).rename('My precious')

# Delete folder
delete_name = 'Imapy' + box.separator + 'Kamikaze folder'
box.folder(delete_name).delete()

# Select parent folder from child folder
new_subfolder_name = 'Imapy' + box.separator + 'My precious'
parent = box.folder(new_subfolder_name).parent()
parent.rename('Imapy renamed')

# logout
box.logout()
