import shutil
from colorama import Fore, Style

FALLBACK_TERMINAL_SIZE = (80, 20)
TERMINAL_COLUMNS = None


def get_console_columns():
    """Returns the number of columns that are in the console"""
    global TERMINAL_COLUMNS

    # Stops the function from executing needlessly multiple times.
    if TERMINAL_COLUMNS:
        return TERMINAL_COLUMNS
    else:
        TERMINAL_COLUMNS = shutil.get_terminal_size(FALLBACK_TERMINAL_SIZE).columns
        return TERMINAL_COLUMNS


def fill_tabs(string: str):
    """Replaces every occurence of \\t with four spaces"""

    return string.replace("\t", "    ")


def will_wrap(length: int)-> bool:
    """Determines if a string will wrap around to multiple lines in the
    console."""

    return get_console_columns() < length


def get_next_segment(string: str, num_columns: int):
    """Finds the next segment of this string that would fit on the screen
    rounded down to the nearest space"""

    fill_tabs(string)

    if len(string) > num_columns:
        diff = len(string) - num_columns
        if string[-diff].isspace():
            return string[:-diff]
        else:
            while not string[-diff].isspace():
                diff += 1
            return string[:-diff]
    else:
        return string


def print_hang(string: str):
    """Prints a string to the console, if it wraps, then a tab is inserted
    whenever it does to create a hanging indent."""

    if will_wrap(len(string)):
        num_columns = get_console_columns()
        while will_wrap(len(string)):
            seg = get_next_segment(string, num_columns)
            if string == seg:
                print(seg)
                string = ""
            else:
                print(seg)
                string = "\t" + string[len(seg):]
    else:
        print(string)


def horizontal_rule(char: str, num: int):
    """Creates a horizontal bar on the screen composed of the given character"""

    # Determines if the bar would wrap, and makes it so it doesn't
    if will_wrap(len(char) * num):
        num = get_console_columns() // len(char)

    print(char * num)


def get_constrained_input(criteria, prompt: str = "")-> bool:
    """Gets input from the user and checks it against the provided criteria,
    continues collecting until it's received a valid response

    criteria must be a one argument method that returns a boolean
        True when the provided argument matches
        False when it doesn't"""

    res = input(prompt)
    while not criteria(res):
        print(Fore.RED + "Invalid response, try again")
        print(Style.RESET_ALL)
        res = input(prompt)

    return res
