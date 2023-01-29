from Printer import *
from browser import Browser
from refs import urls
from refs.pages import LoginPage

before = colored(CYAN, "NOTES:", True) + \
         "\nType 'skip' at email to skip login.\nIf no '@' is found it will automatically add '@gmail.com'\n"
after = "logged in."

def login():
    print(before)

    login = colored(RED, "\nUnsuccessfully", True)

    email = input(user_input("Email: "))
    if email != "skip":
        password = input(user_input("Password: "))

        Browser.go_to(urls.login)

        if '@' not in email:
            email += "@gmail.com"

        LoginPage.email().send_keys(email)
        LoginPage.password().send_keys(password)
        LoginPage.login().click()
    else:
        login = "\nNot"

    if email != "skip":
        try:
            if LoginPage.valid().is_displayed():
                login = colored(GREEN, "\nSuccesfully", True)
        except:
            pass

    print(login, after)

