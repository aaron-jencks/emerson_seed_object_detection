from colorama import Fore


def print_notification(string: str, begin: str = '', **kwargs):
    """Prints a notification to the console"""
    print(begin + Fore.CYAN + '[NOTIFICATION] ' + string + Fore.RESET, **kwargs)


def print_info(string: str, begin: str = '', **kwargs):
    """Prints information to the console"""
    print(begin + Fore.GREEN + '[INFO] ' + string + Fore.RESET, **kwargs)


def print_warning(string: str, begin: str = '', **kwargs):
    """Prints a notification to the console"""
    print(begin + Fore.YELLOW + '[WARNING] ' + string + Fore.RESET, **kwargs)


def print_error(string: str, begin: str = '', **kwargs):
    """Prints a notification to the console"""
    print(begin + Fore.RED + '[ERROR] ' + string + Fore.RESET, **kwargs)


def get_input(prompt: str, begin: str = ''):
    return input(begin + Fore.BLUE + '[HELLO?] ' + prompt + Fore.RESET)
