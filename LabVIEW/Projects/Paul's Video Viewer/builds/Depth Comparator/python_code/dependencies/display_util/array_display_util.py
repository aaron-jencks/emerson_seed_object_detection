
def get_list_string(data: list, delim: str = '\t', fmt: str = '{}') -> str:
    """Converts a 1D data array into a [a0, a1, a2,..., an] formatted string."""
    result = "["
    first = True
    for i in data:
        if not first:
            result += delim + " "
        else:
            first = False

        result += fmt.format(i)

    result += "]"
    return result


def display_2d_table(data, delim: str = '\t', fmt: str = '{}'):
    result = ""
    first = True
    for i in range(data.shape[0]):
        if not first:
            result += "\n"
        else:
            first = False

        result += get_list_string(data[i, :], delim, fmt)
    print(result)
