import os
import sys
import platform
import tempfile
import urllib.request as requests
import urllib.parse as urlparse

from html.parser import HTMLParser


# class CondaSiteParser(HTMLParser):
#     def __init__(self, root_url: str):
#         super().__init__()
#         self.root = root_url
#         self.linux_installer_root = self.root + "#linux"
#         self.windows_installer_root = self.root + "#windows"
#         self.mac_installer_root = self.root + "#macos"
#         self.is_linux = False
#         self.is_windows = False
#         self.is_macos = False
#         self.installer_urls = {}
#
#         self.found_section = False
#         self.current_link = ""
#
#     def get_windows(self):
#         """Gets the windows installer urls"""
#         self.is_windows = True
#         self.found_section = False
#         self.feed(open(requests.urlretrieve(self.windows_installer_root)[0]).read())
#
#         while self.is_windows:
#             pass
#
#         return self.installer_urls
#
#     def get_linux(self):
#         """Gets the windows installer urls"""
#         self.is_linux = True
#         self.found_section = False
#         self.feed(open(requests.urlretrieve(self.linux_installer_root)[0]).read())
#
#         while self.is_linux:
#             pass
#
#         return self.installer_urls
#
#     def handle_starttag(self, tag, attrs):
#         if tag == 'a':
#             for att, val in attrs:
#                 if att == 'href':
#                     self.current_link = val
#                     break
#         elif tag == 'div':
#             for att, val in attrs:
#                 if att == 'id':
#                     if (self.is_windows and val == 'windows') or\
#                        (self.is_linux and val == 'linux') or\
#                        (self.is_macos and val == 'macos'):
#                         self.current_link = ""
#                         self.found_section = True
#                         break
#
#     def handle_data(self, data):
#         if self.found_section and self.current_link != "":
#             self.installer_urls[data] = self.current_link


def find_installer_url(op_sys: str = "win32") -> str:
    """Finds the current installer url for the given operating system."""

    is_64bits = sys.maxsize > 2 ** 32
    print(platform.architecture())

    if op_sys == "win32":
        if is_64bits:
            return "https://repo.anaconda.com/archive/Anaconda3-2019.03-Windows-x86_64.exe"
        else:
            return "https://repo.anaconda.com/archive/Anaconda3-2019.03-Windows-x86.exe"
    elif op_sys == "Linux":
        pass


def download_installer():
    """Finds the anaconda installer online and downloads the installer.
    Returns the path to the installer location."""

    with tempfile.TemporaryDirectory() as download_dir:
        cpu_oper_system = sys.platform
        print("Downloading for {}".format(cpu_oper_system))

        url = find_installer_url(cpu_oper_system)
        output_file = os.path.join(download_dir, url.split('\\'))
        requests.urlretrieve(url, output_file)



if __name__ == "__main__":
    download_installer()
