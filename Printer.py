import colorama
from colorama import Fore, Style

RED = 1
GREEN = 2
YELLOW = 3
CYAN = 4
MAGENTA = 5
BLUE = 6
GRAY = 7

dict = {
    RED: Fore.RED,
    GREEN: Fore.GREEN,
    YELLOW: Fore.YELLOW,
    CYAN: Fore.CYAN,
    MAGENTA: Fore.MAGENTA,
    BLUE: Fore.BLUE,
    GRAY: Fore.LIGHTBLACK_EX
}


colorama.init()


def colored(color, text, bright=False):
    result = dict.get(color)

    if bright:
        result += Style.BRIGHT

    result += text + Style.RESET_ALL

    return result


def divider(text):
    return colored(GRAY, text)


def error(text):
    return colored(RED, text, True)


def user_input(text):
    return colored(MAGENTA, text)