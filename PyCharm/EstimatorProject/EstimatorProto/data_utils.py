import tensorflow as tf
import os

AUTOTUNE = tf.data.experimental.AUTOTUNE


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


def image_extraction_fn(data_record):
    """Parses a tf.Example from the tfrecord data"""

    features = {
        'image/height': tf.FixedLenFeature([], tf.int64),
        'image/width': tf.FixedLenFeature([], tf.int64),
        'image/filename': tf.FixedLenFeature([], tf.string),
        'image/source_id': tf.FixedLenFeature([], tf.string),
        'image/encoded': tf.FixedLenFeature([], tf.string),
        'image/format': tf.FixedLenFeature([], tf.string),
        'image/object/bbox/xmin': tf.VarLenFeature(tf.float32),
        'image/object/bbox/xmax': tf.VarLenFeature(tf.float32),
        'image/object/bbox/ymin': tf.VarLenFeature(tf.float32),
        'image/object/bbox/ymax': tf.VarLenFeature(tf.float32),
        'image/object/class/text': tf.VarLenFeature(tf.string),
        'image/object/class/label': tf.VarLenFeature(tf.int64),
    }

    sample = tf.parse_single_example(data_record, features)

    image_tf = sample["image/encoded"]
    labels = sample["image/object/class/label"]
    xmins = sample["image/object/bbox/xmin"]
    xmaxs = sample["image/object/bbox/xmax"]
    ymins = sample["image/object/bbox/ymin"]
    ymaxs = sample["image/object/bbox/ymax"]

    raw_img = tf.cond(tf.image.is_jpeg(image_tf),
                      lambda: tf.image.decode_jpeg(image_tf),
                      lambda: tf.image.decode_png(image_tf))
    img = tf.image.resize(raw_img, (600, 400))
    # shape = tf.stack([sample["image/height"], sample["image/width"]])

    return [img, labels.values[0]]  # (labels, xmins, xmaxs, ymins, ymaxs)


def get_dataset(root_path: str, record_prefix: str):
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
    ds = ds.map(image_extraction_fn)

    return ds


def get_input_fn(root_path, batch_size: int):
    """Returns a dataset that can be used by an
    estimator."""

    ds = None

    if isinstance(root_path, str):
        # Try to read the folder of images, if it's a string
        record_prefix = os.path.basename(root_path)
        ds = get_dataset(os.path.dirname(root_path), record_prefix)
        ds = ds.shuffle(1000).repeat().batch(batch_size)

    elif isinstance(root_path, dict):
        # Directly turn into a dataset if it's a dictionary

        # Preprocesses the images
        # for i, v in enumerate(root_path["data"]):
        #     root_path["data"][i] = preprocess_image(v)

        ds = tf.data.Dataset.from_tensor_slices((root_path["data"], root_path["labels"]))
        ds = ds.shuffle(len(root_path)).repeat().batch(batch_size)

    return ds
