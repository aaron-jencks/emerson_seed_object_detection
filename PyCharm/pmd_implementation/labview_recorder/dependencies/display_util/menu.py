from .string_display_util import *
from colorama import Fore


def get_constrained_input(prompt: str, constraint) -> str:
    """Prompts the user for input, continues to prompt the user for input until the lambda expression passed in for
        constraint returns True."""

    temp = input(Fore.GREEN + prompt + Fore.RESET)
    while not constraint(temp):
        print_warning("Invalid Response!")
        temp = input(Fore.GREEN + prompt + Fore.RESET)

    return temp


def yes_no_prompt(prompt: str = "") -> bool:
    """Prompts the user for a yes/no answer, automatically appends '(y/n) ' to your prompt.
    Returns True if the user answered yes, and False if they answered no."""

    choice = input(prompt + "(y/n) ")
    while choice != 'y' and choice != 'Y' and choice != 'n' and choice != 'N':
        print_warning("Invalid choice entered, please enter either 'y' or 'n'.")
        choice = input(prompt + "(y/n) ")

    return choice == 'y' or choice == 'Y'


def console_dash_menu(options: dict, list_format: str = "{}: {}", title: str = "", centered_title: bool = True,
                      dash: str = '#', tab_width: int = 4):
    """Creates a console style menu with the given options as choices to choose from
    Returns a key that was chosen from the options dict.
    Keys must be either a str or have a __str__() defined

    Arguments:

    options: a dict containing keys that are choices for users, and values that are descriptions for each key,
        the chosen key will be returned.

    list_format: uses similar syntax to str.format(), the default is \"{}: {}\" where the first {} is the key, and the
        second {} is the value.

    title: the title string displayed at the top of the menu.

    centered_title: True if the title string should be centered in the console.

    dash: character or string used as the duplicated dash sequence for the bars at the top and bottom of the menu.

    tab_width: width, in number of spaces, considered to be a single tab."""

    # Determines the longest string entry of the set of options
    entries = [list_format.format(k, options[k]) for k in options]
    max_length = max([len(x) for x in entries])
    if len(title) > max_length:
        max_length = len(title)

    # Creates the menu
    print_dashes(max_length, dash)
    print((centered_text(title, max_length) if centered_title else title) + "\n")
    print("Options: \n")
    for e in entries:
        print(hanging_indent(e, tab_width))

    print_dashes(max_length, dash)

    # Prompts the user for input and ensures validity
    valid = [str(k) for k in options.keys()]

    choice = get_constrained_input("Choice? ", lambda x: x in valid)

    # Finds the said choice and returns it
    index = valid.index(choice)
    return list(options.keys())[index]
