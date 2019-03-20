
if __name__ == "__main__":
    from argparse import ArgumentParser
    import os

    parser = ArgumentParser("The master SeedDetector trainer and tester")
    parser.add_argument("training_dir",
                        help="The directory where the training images/annotations reside",
                        type=str, default="./training")
    parser.add_argument("testing_dir",
                        help="The directory where the testing images/annotations reside",
                        type=str, default="./testing")
    parser.add_argument("image_folder",
                        help="Image folder name for the testing/training directories",
                        type=str, default="images")
    parser.add_argument("annotation_folder",
                        help="Annotation folder name for the testing/training directories",
                        type=str, default="annotations")
    parser.add_argument("-m", "--model_dir", type=str, default="./models")

