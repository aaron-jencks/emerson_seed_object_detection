import traceback


class File:
    def __init__(self, path: str):
        self.path = path
        self.is_opened = False
        self.fp = None

    def __enter__(self):
        self.open()

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.close()
        traceback.print_exception(exc_type, exc_val, exc_tb)

    def open(self):
        if not self.is_opened:
            self.fp = open(self.path, 'r+')
            self.is_opened = True

    def close(self):
        if self.is_opened:
            self.is_opened = False
            self.fp.close()
