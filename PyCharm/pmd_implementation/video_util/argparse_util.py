import argparse
from roypy_sample_utils import add_camera_opener_options


def get_parser_options(proj_desc: str):
    """Returns an argument parser than can be used to parse command-line arguments"""

    parser = argparse.ArgumentParser(description=proj_desc, usage=__doc__)
    add_camera_opener_options(parser)
    parser.add_argument("--external_trig", '-e', action="store_true")

    return parser
