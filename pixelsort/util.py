import logging
import math
import time

import numpy as np
from PIL import Image

from pixelsort.super_pixel import SuperPixel


def id_generator() -> str:
    timestr = time.strftime("%Y%m%d-%H%M%S")
    return timestr


def crop_to(image_to_crop: Image.Image, reference_image: Image.Image) -> Image.Image:
    """
    Crops image to the size of a reference image. This function assumes that the relevant image is located in the center
    and you want to crop away equal sizes on both the left and right as well on both the top and bottom.
    :param image_to_crop
    :param reference_image
    :return: image cropped to the size of the reference image
    """
    reference_size = reference_image.size
    current_size = image_to_crop.size
    dx = current_size[0] - reference_size[0]
    dy = current_size[1] - reference_size[1]
    left = dx / 2
    upper = dy / 2
    right = dx / 2 + reference_size[0]
    lower = dy / 2 + reference_size[1]
    return image_to_crop.crop(box=(int(left), int(upper), int(right), int(lower)))


def calculate_scaled_size(size, super_pixel_size):
    return (
        math.ceil(size[0] / super_pixel_size),
        math.ceil(size[1] / super_pixel_size),
    )


# Super Pixel Utils
def extract_super_pixel(
    image: Image.Image,
    row: int,
    col: int,
    super_pixel_size: int,
) -> dict:
    # Calculate the coordinates for the super pixel region
    image_width, image_height = image.size
    left = col
    upper = row
    right = min(col + super_pixel_size, image_width)
    lower = min(row + super_pixel_size, image_height)

    # Crop the super pixel region from the input image
    super_pixel = SuperPixel(image.crop((left, upper, right, lower)))

    return super_pixel


def image_to_2d_super_pixel_array(
    image: Image.Image,
    super_pixel_size: int,
) -> np.ndarray:
    logging.debug("Generating Array...")
    image_width, image_height = image.size
    super_pixels = []
    for row in range(0, image_height, super_pixel_size):
        logging.debug(f"Generating Row {row/super_pixel_size}...")
        super_pixel_row = []
        for col in range(0, image_width, super_pixel_size):
            super_pixel = extract_super_pixel(image, row, col, super_pixel_size)
            super_pixel_row.append(super_pixel)
        super_pixels.append(super_pixel_row)
    logging.debug("Converting to Numpy Array...")
    arr = np.array(super_pixels)
    logging.debug("Transposing Numpy Array...")
    arr = np.transpose(arr)
    logging.debug("Done Generating Array...")
    return arr
