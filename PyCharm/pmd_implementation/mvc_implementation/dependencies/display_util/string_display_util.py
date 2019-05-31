import shutil
from colorama import Fore
from enum import Enum
import os


def clear():
    """Clears the terminal screen as per
    https://stackoverflow.com/questions/517970/how-to-clear-the-interpreter-console"""
    if os.name in ('nt','dos'):
        os.system("cls")
    elif os.name in ('linux','osx','posix'):
        os.system("clear")
    else:
        print("\n"*120)


def centered_text(text: str, length: int = -1) -> str:
    """Returns a string that contains enough spaces to center the text in the context of the length given

    Defaults to centering the text in the width of the entire console

    text is stripped of leading and trailing whitespace before starting

    If length - len(text) is odd, then the extra space is appended to the end of the string

    If len(text) >= length, then text is returned

    If length is wider than the terminal width, then it is squeezed to fit

    Note: This does add spaces to the end of the string, not just the beginning, this allows for an accurate size in
    conjunction with other functions in this library"""

    t = text.strip()

    # If length is longer than the console width, then squeeze it to fit
    num_col = shutil.get_terminal_size((80, 20)).columns
    if length > num_col:
        length = num_col

    if len(t) >= length:
        return t

    space_tot = length - len(t)
    space_num = space_tot // 2

    space = " "*space_num

    if space_tot % 2 == 0:
        return space + t + space
    else:
        # Places the extra space at the end of the string
        return space + t + space + " "


def dashed_line(num: int, dash: str = '#') -> str:
    """Returns a string composed of num dashes"""

    temp = ""
    for i in range(num):
        temp += dash

    return temp


def print_dashes(num: int, dash: str = '#'):
    """Prints out a single line of dashes with num chars
    If the num is larger than the console width, then a single console width is printed out instead"""

    # Gets the terminal width
    num_col = shutil.get_terminal_size((80, 20)).columns

    print(dashed_line(num if num <= num_col else num_col, dash))


def hanging_indent(string: str, tab_width: int = 4) -> str:
    """Creates a hanging indent """

    # Gets the terminal width
    num_col = shutil.get_terminal_size((80, 20)).columns

    if len(string) <= num_col:
        # Returns a clone of the string, not the original
        return string[:]

    # Creates a tab string
    tab = " "*tab_width

    result = string[:num_col]
    remaining = string[num_col:]
    while True:
        if len(remaining) > num_col - tab_width:
            result += tab + remaining[:num_col - tab_width]
            remaining = remaining[num_col - tab_width:]
        else:
            result += tab + remaining
            break

    return result


class ListTypes(Enum):
    NUMERIC_ORDERED = 0
    ALPHA_ORDERED = 1
    UNORDERED = 2


def print_list(arr: list, format: str = "{}: {}", type: ListTypes = ListTypes.NUMERIC_ORDERED, **kwargs):
    """Prints a list to the screen in a neat fashion.

    format is a string used to determine layout of the element, default is '{}: {}' where the first is the index,
        and the second is the element."""

    if type == ListTypes.NUMERIC_ORDERED:
        for i, e in enumerate(arr):
            print(format.format(i, e), **kwargs)
    elif type == ListTypes.ALPHA_ORDERED:
        for i, e in enumerate(arr):
            print(format.format(chr(ord('a') + i), e), **kwargs)
    else:
        for e in arr:
            print(format.format('•', e), **kwargs)


def print_info(string: str, begin: str = '', **kwargs):
    """Prints an info prompt to the console
    info prompts have '[INFO]' as a prefix and are printed in Yellow."""
    print(begin + Fore.YELLOW + "[INFO] " + string + Fore.RESET, **kwargs)


def print_warning(string: str, begin: str = '', **kwargs):
    """Prints an warning prompt to the console
    warning prompts have '[WARNING]' as a prefix and are printed in Red."""
    print(begin + Fore.RED + "[WARNING] " + string + Fore.RESET, **kwargs)


def print_notification(string: str, begin: str = '', **kwargs):
    """Prints an notification prompt to the console
    notification prompts have '[NOTIFICATION]' as a prefix and are printed in Green."""
    print(begin + Fore.GREEN + "[NOTIFICATION] " + string + Fore.RESET, **kwargs)
