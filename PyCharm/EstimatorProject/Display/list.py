from .util import *


def print_list(choices_dict: dict,
               prompt: str = "",
               ordered: bool = True,
               choice_display_format: str = "{}: {}",
               display_char: str = '#'):
    """Creates a text-line user interface for prompting the user for input
    Currently only works for choice selection prompts"""

    num_columns = get_console_columns()

    horizontal_rule(display_char, num_columns)

    if len(prompt) is not 0:
        print_hang(prompt)
    print()

    if choice_display_format.count('{}') != 2:
        raise Exception("There must be exactly two '{}' instances for menu gui to operate correctly")
    else:
        for c in choices_dict:
            if ordered:
                print_hang(choice_display_format.format(c, choices_dict[c]))
            else:
                print_hang(choice_display_format.format('*', choices_dict[c]))

    print()
    horizontal_rule(display_char, num_columns)


def enumerate_and_print_list(items: list,
                             prompt: str = "",
                             ordered: bool = True,
                             choice_display_format: str = "{}: {}",
                             display_char: str = '#'):
    """Prints a list out to the console and enumerates it, does not allow for nested items"""

    choices_dict = {}
    for i, v in enumerate(items):
        choices_dict[i] = v

    print_list(choices_dict, prompt, ordered, choice_display_format, display_char)
