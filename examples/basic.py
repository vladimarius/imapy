# -*- encoding: utf-8 -*-
"""
Shows some basic operations with Imapy
"""

import imapy

em = imapy.connect(
    host="host",
    username="username",
    password="password",
    # you may also specify custom port:
    # port=993
    ssl=True,
)

# get all folder names
folders = em.folders()

""" 'folders' now contains a list of all folder names.
    Email folders can be hierarchical (have parent and
    children). A folder name of a child folder consists
    of a parent name + separator symbol + name of a child.
"""

# get information about Inbox folder
# (note that Gmail uses "INBOX" as Inbox folder name)
status = em.folder("Inbox").info()
total_messages = status["total"]

# create folder named 'Awesome' in the root folder
# having subfolder named 'Even awesomer'
em.folder().make_folder("Awesome")
em.folder("Awesome").make_folder("Even awesomer")

# get 5 latest emails from Inbox and print some details
emails = em.folder("Inbox").emails(-5)

for email in emails:
    print(f"Email from: {email.sender.name}, {email.sender.email}")
    print(f"Email subject: {email.subject}")

# copy last 3 emails from 'Inbox' to 'Awesome/Even awesomer'
# folder, make them flagged and unseen
emails = em.folder("Inbox").emails(-3)
for em in emails:
    folder_name = "Awesome" + em.separator + "Even awesomer"
    em.copy(folder_name).mark(["Unseen", "Flagged"])

# logout
em.logout()
