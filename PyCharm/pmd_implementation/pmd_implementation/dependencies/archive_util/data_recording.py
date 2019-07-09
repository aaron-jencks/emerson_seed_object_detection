from enum import Enum


class DataRecordingType(Enum):
    OVERWRITE = 0
    APPEND = 1


class TabDelimText:
    """Provides functions to write tab-delimitted text files"""
    def __init__(self, path: str, method: DataRecordingType = DataRecordingType.APPEND):
        self.fp = open(path, 'a' if method == DataRecordingType.APPEND else 'w')

    def __del__(self):
        self.dispose()

    def dispose(self):
        self.fp.close()

    @staticmethod
    def __create_tab_delim_line(data: list, formatter: str) -> str:
        """Creates a tab-delimitted line of data"""
        result = ""
        first = True
        for d in data:
            if first:
                first = False
            else:
                result += '\t'

            result += formatter.format(d)

        result += '\n'

        return result

    def add_data(self, data: list, format_string: str = '{}'):
        self.fp.write(self.__create_tab_delim_line(data, format_string))

    def add_headers(self, headers: list):
        self.add_data(headers)
