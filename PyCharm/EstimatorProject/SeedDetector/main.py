from argparse import ArgumentParser
from EstimatorProto.tfrecords_utils.Determine_training_set import *
from EstimatorProto.tfrecords_utils.create_tf_records import *
from Display.menu import get_menu_response
from Display.util import get_constrained_input
import os
import pathlib

from EstimatorProto.data_utils import find_min_dim


def convert_tfr(root_path: str):
    """Converts the xml annotations and the images
    created with split_dataset into TFRecords."""

    print("Generating tfrecords")

    (train, test) = find_xml_files(root_path)

    train_df = xml_to_csv(train)
    test_df = xml_to_csv(test)

    gen_tfrecord(train_df, os.path.join(root_path, "data/train.record"), root_path)
    gen_tfrecord(test_df, os.path.join(root_path, "data/test.record"), root_path)

    print("Generated TFRecords")


def split_dataset(root_path: str):
    """Splits the dataset using the tools from the
    Determine_training_set.py file, returns the minimum dimensions
    of the images found"""

    print("Finding the image directories and converting them.")

    (train, test) = read_train_val(root_path)

    train_dir = os.path.join(root_path, "images/train/")
    test_dir = os.path.join(root_path, "images/test/")

    # Creates the train folder if it doesn't exist yet.
    pathlib.Path(train_dir).mkdir(parents=True, exist_ok=True)

    # Creates the test folder if it doesn't exist yet.
    pathlib.Path(test_dir).mkdir(parents=True, exist_ok=True)

    # Copies the files into their respective directories
    copy_files(train, train_dir)
    copy_files(test, test_dir)

    return find_min_dim(train + test)


if __name__ == "__main__":

    os.environ['PYTHONPATH'] += ":/home/aaron/Documents/workspace/github_repos/tensorflow/models/research \
        :/home/aaron/Documents/workspace/github_repos/tensorflow/models/research/slim"

    parser = ArgumentParser("The master SeedDetector trainer and tester")
    parser.add_argument("-d", "--data_dir",
                        help="The directory where the images/annotations reside",
                        type=str, default="./data")
    parser.add_argument("-m", "--model_dir", type=str, default="./models")
    args = parser.parse_args()

    hasConverted = False
    hasSplit = False
    hasTrained = False
    data_dir = args.data_dir
    model_dir = args.model_dir

    while True:
        res = int(get_menu_response(
            {0: "Options",
             1: "Split dataset", 2: "Convert to TFRecords", 3: "Train model", 4: "Do all of them please",
             5: "Quit"},
            "Welcome to the Seed Detector model trainer, what would you like to do?"
        ))

        if res is 0:
            res = int(get_menu_response(
                {0: "Change data directory", 1: "Change model directory",
                 2: "Back"},
                "Welcome to the Seed Detector model trainer options menu, what would you like to do?"
            ))

            if res is 0:
                data_dir = get_constrained_input(lambda x: os.path.isdir(x),
                                                 "Please enter a new value for the data directory: ")
                continue
            elif res is 1:
                model_dir = get_constrained_input(lambda x: os.path.isdir(x),
                                                  "Please enter a new value for the model directory: ")
                continue
            elif res is 2:
                continue
        elif res is 1 or res is 4:
            if not hasSplit:
                split_dataset(data_dir)
                hasSplit = True
            else:
                print("You've already done that")
        elif res is 2 or res is 4:
            if not hasConverted:
                convert_tfr(data_dir)
                hasConverted = True
            else:
                print("You've already done that")
        elif res is 3 or res is 4:
            if not hasTrained:
                pass
            else:
                print("You've already done that")
        elif res is 5:
            break
        else:
            print("Coming soon")

