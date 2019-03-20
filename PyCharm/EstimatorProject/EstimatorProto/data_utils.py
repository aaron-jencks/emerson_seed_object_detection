import tensorflow as tf
import random
import pathlib

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


def get_dataset(root_path: str):
    """Finds all image files located in the root
    directory and loads them into a tf.Dataset
    object."""

    print("Creating images")
    all_image_paths = list(root_path.glob('*/*'))
    all_image_paths = [str(path) for path in all_image_paths]
    random.shuffle(all_image_paths)

    print("Creating labels")
    label_names = sorted(item.name for item in root_path.glob('*/') if item.is_dir())
    label_to_index = dict((name, index) for index, name in enumerate(label_names))
    all_image_labels = [label_to_index[pathlib.Path(path).parent.name]
                        for path in all_image_paths]

    print("Creating combined dataset")
    ds = tf.data.Dataset.from_tensor_slices((all_image_paths, all_image_labels))
    image_label_ds = ds.map(load_and_preprocess_from_path_label)

    return image_label_ds, len(all_image_paths)


def get_input_fn(root_path, batch_size: int):
    """Returns a dataset that can be used by an
    estimator."""

    ds = None

    if isinstance(root_path, str):
        # Try to read the folder of images, if it's a string
        ds, cnt = get_dataset(root_path)
        ds = ds.shuffle(cnt).repeat().batch(batch_size)

    elif isinstance(root_path, dict):
        # Directly turn into a dataset if it's a dictionary

        # Preprocesses the images
        # for i, v in enumerate(root_path["data"]):
        #     root_path["data"][i] = preprocess_image(v)

        ds = tf.data.Dataset.from_tensor_slices((root_path["data"], root_path["labels"]))
        ds = ds.shuffle(len(root_path)).repeat().batch(batch_size)

    return ds
