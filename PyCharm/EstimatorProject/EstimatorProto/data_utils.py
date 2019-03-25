import tensorflow as tf
import os

from tqdm import tqdm

AUTOTUNE = tf.data.experimental.AUTOTUNE


def find_min_dim(image_files):
    """Searches a directory for all of its images, then returns
    a tuple containing the minimum width and height found"""

    from PIL import Image

    min_dim = {"width": None, "height": None}

    print("Finding min and maxes")
    for f in tqdm(image_files):
        img = Image.open(f)
        width, height = img.size

        # Checks width
        if not min_dim["width"] or width < min_dim["width"]:
            min_dim["width"] = width

        # Checks height
        if not min_dim["height"] or width < min_dim["height"]:
            min_dim["height"] = width

    return min_dim["width"], min_dim["height"]


def preprocess_image(image):
    """Takes an image, decodes it into a 2D array of
    ints ranging from 0-255, then converts it to float
    from 0-1"""

    image = tf.image.decode_jpeg(image, channels=3)
    image = tf.image.resize_images(image, [192, 192])
    image /= 255.0  # normalize to [0,1] range

    return image


def load_and_preprocess_image(path:str):
    """Loads an image from a given path and encodes it
    using the preprocess_image() method"""

    image = tf.read_file(path)
    return preprocess_image(image)


def load_and_preprocess_from_path_label(path: str, label: str):
    """Loads an image from the given path and pairs it with
    its label."""

    return load_and_preprocess_image(path), label


def image_extraction_fn(data_record, min_dim):
    """Parses a tf.Example from the tfrecord data"""

    features = {
        'image/encoded': tf.FixedLenFeature([], tf.string),
        'image/object/class/label': tf.FixedLenFeature([], tf.int64),
    }

    sample = tf.parse_single_example(data_record, features)

    image_tf = sample["image/encoded"]
    labels = sample["image/object/class/label"]

    raw_img = tf.cond(tf.image.is_jpeg(image_tf),
                      lambda: tf.image.decode_jpeg(image_tf, 1),
                      lambda: tf.image.decode_png(image_tf, 1))
    img = tf.image.resize(raw_img, min_dim)
    img = tf.image.convert_image_dtype(img, tf.float32)

    label = tf.one_hot(labels, 3, 1, 0)

    return [img, labels]  # labels.values]


def get_dataset(root_path: str, record_prefix: str, min_dim):
    """Finds all image files located in the root
    directory and loads them into a tf.Dataset
    object."""
    import fnmatch

    print("Creating dataset")
    files_in_dir = os.listdir(root_path)
    pattern = "{}*".format(record_prefix)
    all_records = [os.path.join(root_path, path)
                   for path in fnmatch.filter(files_in_dir, pattern)]

    ds = tf.data.TFRecordDataset(all_records)
    ds = ds.map(lambda x: image_extraction_fn(x, min_dim))

    return ds


def get_input_fn(root_path, batch_size: int, min_dim):
    """Returns a dataset that can be used by an
    estimator."""

    ds = None

    # Try to read the folder of images, if it's a string
    record_prefix = os.path.basename(root_path)
    ds = get_dataset(os.path.dirname(root_path), record_prefix, min_dim)
    ds = ds.shuffle(1000).repeat().batch(batch_size)

    return ds


def setup_temp_model_dir(name: str = None):
    """Sets up a temporary directory that you can use to store your model files.
    The new directory will be stored at: <temporary_directory>/Emerson_Toolkit/<name>
    'name' will default to model_n if one is not supplied.

    Returns a series of directories that are created in the order below
    temp_ctx, temp_dir, data_dir, image_dir, annotation_dir, model_dir

    temp_ctx is the context manager for the temporary directory, see the documentation
        https://docs.python.org/3/library/tempfile.html#tempfile.TemporaryDirectory
        It's name will point to <temporary_directory>/Emerson_Toolkit/.
        When you are done with this object, call temp_ctx.cleanup() to delete all of the files.

    temp_dir will point to <temp_ctx>/<name>

    data_dir is <temp_dir>/data

    image_dir is <data_dir>/images, there is a folder in this one called 'raw', but that folder
        is not explicitly returned.

    annotation_dir is <data_dir>/annotations

    model_dir is <temp_dir>/model
    """

    import tempfile
    import pathlib

    temp_dir = tempfile.TemporaryDirectory(prefix="Emerson_Toolkit_")

    temp_root = temp_dir.name
    pathlib.Path(temp_root).mkdir(parents=True, exist_ok=True)

    if not name:
        temp_root = tempfile.mkdtemp(prefix="model", dir=temp_root)
    else:
        temp_root = os.path.join(temp_root, name)

    data_dir = os.path.join(temp_root, "data/")

    # Creates the file hierarchy in the temporary directory
    print("Creating temporary workspace {}".format(temp_root))
    image_dir = os.path.join(data_dir, "images/")
    annotation_dir = os.path.join(data_dir, "annotations/")
    pathlib.Path(image_dir).mkdir(parents=True, exist_ok=True)
    pathlib.Path(os.path.join(image_dir, "raw/")).mkdir(parents=True, exist_ok=True)
    pathlib.Path(annotation_dir).mkdir(parents=True, exist_ok=True)
    pathlib.Path(os.path.join(data_dir, "data/")).mkdir(parents=True, exist_ok=True)

    model_dir = os.path.join(temp_root, "model/")
    pathlib.Path(model_dir).mkdir(parents=True, exist_ok=True)

    return temp_dir, temp_root, data_dir, image_dir, annotation_dir, model_dir
