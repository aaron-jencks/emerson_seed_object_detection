from .list import print_list


def get_menu_response(choices_dict: dict,
                      prompt: str = "",
                      choice_display_format: str = "{}: {}",
                      display_prompt: str = 'Your choice: ',
                      display_char: str = '#'):
    """Creates a text-line user interface for prompting the user for input
    Currently only works for choice selection prompts, then asks the
    user to select a choice"""

    from colorama import Fore, Style

    # Ensures that the choices are strings, and not a different datatype
    choices = []
    for k in choices_dict.keys():
        choices.append(str(k))

    print_list(choices_dict, prompt, True, choice_display_format, display_char)
    print()

    # Asks the user to make their decision
    c = input(display_prompt)
    while c not in choices:
        print(Fore.RED + "Invalid response, try again")
        print(Style.RESET_ALL)

        print_list(choices_dict, prompt, True, choice_display_format, display_char)
        print()

        # Asks the user to make their decision
        c = input(display_prompt)

    return c
