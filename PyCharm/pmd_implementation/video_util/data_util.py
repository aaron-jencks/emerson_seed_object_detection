from data_structures.lists import LinkedList
from matplotlib.path import Path as MPth
import numpy as np


def find_mins_maxes(arr: list) -> tuple:
    """Finds the minimum and maximum of the given list and returns them as (min, max)"""

    return min(arr), max(arr)


def find_mean(arr: list) -> float:
    """Finds the average of a given list"""

    return sum(arr) / len(arr) if len(arr) > 0 else 0


def get_mask(verts, current_image):
    ny, nx = np.shape(current_image)

    # Create vertex coordinates for each grid cell...
    # (<0,0> is at the top left of the grid in this system)
    x, y = np.meshgrid(np.arange(nx), np.arange(ny))
    x, y = x.flatten(), y.flatten()
    points = np.vstack((x, y)).T

    roi_path = MPth(verts)
    grid = roi_path.contains_points(points).reshape((ny, nx))

    return grid


def apply_mask(mask, image) -> tuple:
    """Applies the boolean mask returned by get_mask() to a 2D image, returns a tuple of 3 lists

    mask: the boolean mask to use.

    image: the image to apply the mask to.

    Returns: Returns 3 lists composed of x_coord, y_coord, img.
        x_coord: contains the x coordinates of the corresponding img value
        y_coord: contains the y coordinates of the corresponding img value
        img: contains the remaining image after the crop is applied"""

    width, height = np.shape(image)

    x_coord = LinkedList()
    y_coord = LinkedList()
    selection = LinkedList()

    for col in range(width):
        for row in range(height):
            if mask[col][row] and image[col][row]:
                x_coord.append(col)
                y_coord.append(row)
                selection.append(image[col][row])

    return x_coord, y_coord, selection
