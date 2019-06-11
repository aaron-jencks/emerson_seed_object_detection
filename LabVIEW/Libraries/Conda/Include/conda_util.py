import os.path as pth


install_root = "C:\\programs"


def detect_existing_install() -> bool:
  """Detects if there is a prior existing installation on the hardrive."""
  
  return False


def install_conda():
  """Downloads and opens the anaconda install prompt, but only if it's not already installed."""
  
  
