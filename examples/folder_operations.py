# -*- encoding: utf-8 -*-
"""
Shows some folder operations with Imapy
"""

import imapy

em = imapy.connect(
    host="host",
    username="username",
    password="password",
    ssl=True,
)

# get all folder names
folders = em.folders()

# search folders by keyword
# names start with 'Inbo' (matches 'Inbox')
folders = em.folders("Inbo*")
# names end with 'ox' (matches 'Inbox')
folders = em.folders("*ox")
# names contain 'nb' (matches 'Inbox')
folders = em.folders("*nb*")
# names contain 'n', followed by 'o' somewere ahead (matches 'Inbox')
folders = em.folders("*n*o*")

# Create folder
em.folder().make_folder("Imapy")

# Create subfolders
# (note how you can pass several folder names in a list)
em.folder("Imapy").make_folder(["Imapy subfolder", "Kamikaze folder"])

# Get list of children names of a folder
children = em.folder("Imapy").children()
for c in children:
    print(f"{c} is a child of 'Imapy' folder")

# Rename subfolder
subfolder_name = "Imapy" + em.separator + "Imapy subfolder"
em.folder(subfolder_name).rename("My precious")

# Delete folder
delete_name = "Imapy" + em.separator + "Kamikaze folder"
em.folder(delete_name).delete()

# Select parent folder from child folder
new_subfolder_name = "Imapy" + em.separator + "My precious"
parent = em.folder(new_subfolder_name).parent()
parent.rename("Imapy renamed")

# logout
em.logout()
