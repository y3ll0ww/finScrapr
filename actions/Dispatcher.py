import time
import traceback

from Printer import *
from actions import AuthorizationActions, CompaniesActions, CompanyDetailsActions, DatabaseActions
from browser import Browser

LOGIN = colored(YELLOW, "WEB: ", True) + colored(YELLOW, "Loggin in")
COLLECT_COMPANIES = colored(YELLOW, "WEB: ", True) + colored(YELLOW, "list all companies")
COLLECT_FUNDAMENTALS = colored(YELLOW, "WEB: ", True) + colored(YELLOW, "statements for all companies")
DATABASE_CREATION = colored(YELLOW, "DATABASE: ", True) + colored(YELLOW, "create database")
DATABASE_INSERTION = colored(YELLOW, "DATABASE: ", True) + colored(YELLOW, "insert into database")
QUIT = colored(YELLOW, "Close application")


class Dispatcher:
    def __init__(self):
        pass

    dict = {
        1: LOGIN,
        2: COLLECT_COMPANIES,
        3: COLLECT_FUNDAMENTALS,
        4: DATABASE_CREATION,
        5: DATABASE_INSERTION,
        0: QUIT
    }

    welcome = colored(RED, "WELCOME", True) + colored(RED, " to the ") + colored(RED, "FINVIZ SCRAPER", True)
    actions = divider("\n-----\n") + colored(CYAN, "POSSIBLE ACTIONS:\n\n", True) + \
              "#1 " + dict.get(1) + "\n" \
              "#2 " + dict.get(2) + "\n" \
              "#3 " + dict.get(3) + "\n\n" \
              "#4 " + dict.get(4) + "\n" \
              "#5 " + dict.get(5) + "\n\n" \
              "#0 " + dict.get(0) + "\n"

    def start(self):
        print(self.welcome)

        Browser.start()

        active = True
        while active:
            print(self.actions)
            action = input(user_input("Action: ") + "#")
            try:
                a = int(action)
                if a > 0:
                    self.__dispatcher(self.dict.get(a))
                else:
                    print("Closing the program...")
                    active = False
            except:
                print(error("Err: Not a suitable action; type the number of the action."))
                traceback.print_exc()
                pass

        Browser.quit()
        print("Application terminated.")

    def __dispatcher(self, action):
        print(divider("\n===========================================\n"))
        print(colored(CYAN, time.ctime(time.time())) + "\nAction dispatched: \"" + action + "\"")
        print(colored(GREEN, "ACTION STARTED\n", True))
        start_time = time.time()

        if action == LOGIN:                   AuthorizationActions.login()
        elif action == COLLECT_COMPANIES:     CompaniesActions.collect()
        elif action == COLLECT_FUNDAMENTALS:  CompanyDetailsActions.collect()
        elif action == DATABASE_CREATION:     DatabaseActions.create()
        elif action == DATABASE_INSERTION:    DatabaseActions.insert()
        else:
            print(colored(RED, "Err: No valid action given; make sure it is within range of possible actions."))

        elapsed_time = time.time() - start_time
        print(divider("\n===========================================\n"))
        print(colored(RED, "ACTION ENDED\n", True))
        print(colored(CYAN, time.ctime(time.time())))
        print("Action completed: \"" + action + "\"")
        print(self.__elapsed_time(elapsed_time))

    def __elapsed_time(self, elapsed_time):
        days = 0
        if elapsed_time >= 86400:
            days = colored(MAGENTA, str(int(elapsed_time / 86400)))
        elapsed = colored(MAGENTA, time.strftime("%H:%M:%S", time.gmtime(elapsed_time)))
        if days == 0:
            return f"Time elapsed: {elapsed}"
        else:
            return f"Time elapsed: {days}:{elapsed}"
