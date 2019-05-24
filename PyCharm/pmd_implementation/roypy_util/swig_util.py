import os


def setup_interface(directory: str) -> str:
    result = "%module roypy\n%{\n"
    files = []
    for r, w, f in os.walk(directory, followlinks=True):
        for file in f:
            if file.endswith('.hpp'):
                files.append(file)

    for f in files:
        result += '#include "{}"\n'.format(f)

    result += "%}\n\n"

    for f in files:
        result += '%include "{}"\n'.format(f)

    return result


if __name__ == "__main__":
    file = setup_interface(input("Where would you like to search for headers? "))
    print(file)
    with open(input("Where would you like to store this? "), 'w+') as f:
        f.write(file)
    print("Write complete!")
