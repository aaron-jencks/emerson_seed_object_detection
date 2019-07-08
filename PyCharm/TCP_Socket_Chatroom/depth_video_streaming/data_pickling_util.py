
class DataPreparator:
    """A class used to wrap functions necessary for preparing data for transmission along the TCP sockets

    The TCP server will call the 'convert()' method that must return a bytes object of the correct format for
    transmission"""

    def __init__(self, data=None, encoding: str = 'utf-8'):
        self.data = data
        self.encoding = encoding

    def convert(self, data=None) -> bytes:
        """Converts the data into a usable object for tcp server"""
        if self.data is None and data is None:
            raise AssertionError("Data to transfer cannot be None")
        return ''.encode(self.encoding)
