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
