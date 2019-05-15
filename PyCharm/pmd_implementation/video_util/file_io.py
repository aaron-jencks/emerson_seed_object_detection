import os.path as pth
import tempfile


def get_fake_file_buffer(filename: str = None) -> tuple:
    """Creates a linux fifo socket and binds it to the filename supplied. Returns the socket object"""

    tempfile.tempdir = '/dev/shm'
    path = pth.join(tempfile.mkdtemp(), filename if filename is not None else 'SOCK.rrf')

    return path
