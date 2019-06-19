from backup_util.storage_util import list_dir_w_exclusions
from display_util.string_display_util import print_info, print_notification
import zipfile
from zipfile import ZipFile
from tqdm import tqdm
import os
import datetime


backup_dir = "D:/backup/backup"


def get_backup_name() -> str:
    return datetime.date.today().strftime("%a-%d-%Y_%H:%M:%S")


def get_archive_name(prefix: str = 'backup', suffix: str = '') -> str:
    if not os.path.exists(os.path.join(backup_dir, prefix + ('_' + suffix if suffix != '' else '') + '.zip')):
        return prefix + ('_' + suffix if suffix != '' else '') + '.zip'
    else:
        prefix += '_'
        i = 1
        while os.path.exists(os.path.join(backup_dir, prefix + str(i) + suffix + '.zip')):
            i += 1

        return prefix + str(i) + suffix + '.zip'


def zip_dir(directory: str, output_dir: str, exclusions=None) -> str:
    """Creates a new archive of the given directory using the current date and time as a name"""

    # To ensure that the output path actually exists
    if exclusions is None:
        exclusions = []
    os.makedirs(output_dir, exist_ok=True)

    if os.path.exists(directory) and os.path.isdir(directory):
        arch_name = get_archive_name(suffix=os.path.basename(directory))
        print_info("Making archive file for {}".format(arch_name))
        archive = os.path.join(output_dir, arch_name)
        with ZipFile(archive, 'x', zipfile.ZIP_DEFLATED) as arch:

            # Add files here
            # Create a file that marks where the original files came from
            print_info("Adding restoration directory file")
            parent = os.path.abspath(os.curdir)
            os.chdir(output_dir)
            restoration_file = os.path.relpath(str(os.path.basename(arch_name).split('.')[0]) + '.txt')
            with open(restoration_file, 'x') as f:
                f.write(directory)
            arch.write(restoration_file)
            os.remove(restoration_file)

            # Helps us get relative paths instead of absolute ones
            os.chdir(directory)
            print_notification("Scanning files")
            files = list_dir_w_exclusions(directory, exclusions if exclusions is not None else [])
            print_notification("Archiving files")
            for file in files:
                print_info("Backing up {}".format(file))
                arch.write(file)
            os.chdir(parent)

        return archive


def zip_dir_delete_orig(directory: str, output_dir: str, exclusions=None) -> str:
    """Creates a new archive of the given directory using the current date and time as a name,
    deletes the original contents as it's copied over"""

    # To ensure that the output path actually exists
    if exclusions is None:
        exclusions = []
    os.makedirs(output_dir, exist_ok=True)

    if os.path.exists(directory) and os.path.isdir(directory):
        arch_name = get_archive_name()
        print_info("Making archive file for {}".format(arch_name))
        archive = os.path.join(output_dir, arch_name)
        parent = os.path.abspath(os.curdir)
        os.chdir(directory)
        with ZipFile(archive, 'x', zipfile.ZIP_DEFLATED) as arch:
            print_notification("Scanning files")
            files = list_dir_w_exclusions(directory, exclusions if exclusions is not None else [])
            print_notification("Archiving files")
            for file in files:
                print_info("Backing up {}".format(file))
                arch.write(file)
                os.remove(file)
        os.chdir(parent)

        return archive


def restore_dir(archive: str, replace_existing: bool = True, clear_output_dir: bool = False):
    """Restores a zip archive to its original location"""
    pass
