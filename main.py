# -*- coding: utf-8 -*-


"""Gitbot.
Python script to get as many stars and users on GitHub as you want."""


import traceback
import os
import random
import time
from uuid import uuid4

from mechanize import Browser


# List of popular mail providers to choose from
MAIL_PROVIDERS = ("@yahoo.com", "@gmail.com", "@outlook.com", "@riseup.net")
PASSWORD = "iambatman69"  # a "fake" password
USERNAMES_CREATED = []  # empty list to populate with usernames created
with open(os.path.join("assets", "names.txt")) as fyle:
    NAMES_LIST = tuple(fyle.readlines())  # tuple with strings, for usernames


try:
    input = raw_input  # Running on Python 2.x
except NameError:
    pass  # Running on Python >= 3.x
print(__doc__)

search_username_reponame = str(input("Enter username:repo-name with comma separated: "))


# Asks the user to verify that the reposiitory is part of an organization.
while True:
    organization = str(input("Is this an organization repository (y/n) ?"))
    if organization.lower() in ["yes", "y"]:
        organization = True
        break
    elif organization.lower() in ["no", "n"]:
        organization = False
        break
    else:
        print("Not a valid response. Try Again")
        continue

n = int(input("Enter number of stars&followers you want "))

for i in range(n):
    print(i)
    username = random.choice(NAMES_LIST).lower().strip() + uuid4().hex[:9]
    email = username + random.choice(MAIL_PROVIDERS)
    USERNAMES_CREATED.append(username)
    print(username + " --> " + email)

    br = Browser()
    br.set_handle_robots(False)   # ignore robots
    br.set_handle_refresh(False)  # can sometimes hang without this

    # open GitHub signup page and set form values

    br.open("https://github.com/join?source=header-home")
    br.form = list(br.forms())[1]
    login_control = br.form.find_control("user[login]")
    if login_control.type == "text":
        login_control.value = username
    email_control = br.form.find_control("user[email]")
    if email_control.type == "text":
        email_control.value = email
    password_control = br.form.find_control("user[password]")
    if password_control.type == "password":
        password_control.value = PASSWORD
    for control in br.form.controls:
        submit = control

    submit.readonly = False
    print("Created new user")
    br.submit()

    for i in search_username_reponame.split(","):
        searchusername = i.split(":")[0].strip()
        searchreponame = i.split(":")[1].strip()
        # Checks if the repo is an organization
        if not organization:
            # open link to your profile
            br.open("https://github.com/" + searchusername)
            br.form = list(br.forms())[4]

            for control in br.form.controls:
                follow = control

            follow.readonly = False
            print("Followed")
            br.submit()  # Follow the user


            # Time delay to prevent too many requests
            time.sleep(random.randint(1, 8))

        # open link to your repo
        br.open("https://github.com/" + searchusername + "/" + searchreponame)
        br.form = list(br.forms())[4]

        for control in br.form.controls:
            star = control
        star.readonly = False
        print("Starred")
        br.submit()  # Star the repo

    
    time.sleep(random.randint(1, 8))  # Time delay to prevent too many requests


with open(os.path.join("unbot", "usernamescreated.txt"), "w") as fyle:
    fyle.write("\n".join(USERNAMES_CREATED))  # write file with created users

#nambah seperlunya
#nambah seperlunya2
