import logging
from PIL import Image
import numpy as np


class SuperPixel:
    def __init__(self, pixels: Image):
        self.pixels = pixels
        self.average_pixel = pixels.resize((1, 1)).load()[0,0]


def _extract_super_pixel(
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


def _image_to_2d_super_pixel_array(
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
            super_pixel = _extract_super_pixel(
                image, row, col, super_pixel_size
            )
            super_pixel_row.append(super_pixel)
        super_pixels.append(super_pixel_row)
    logging.debug("Converting to Numpy Array...")
    arr = np.array(super_pixels)
    logging.debug("Transposing Numpy Array...")
    arr = np.transpose(arr)
    logging.debug("Done Generating Array...")
    return arr


class SuperPixelImage:
    def __init__(self, image: Image.Image, super_pixel_size: int):
        self.super_pixels = _image_to_2d_super_pixel_array(
            image=image,
            super_pixel_size=super_pixel_size,
        )
        self.super_pixel_size = super_pixel_size
        self.original_size = image.size
        self.size = (len(self.super_pixels), len(self.super_pixels[0]))

    def to_standard_image(self) -> Image.Image:
        new_image = Image.new("RGB", self.original_size)

        # Paste each super_pixel into the new image at its corresponding position in the grid
        y_offset = 0
        for row in self.super_pixels:
            x_offset = 0
            for super_pixel in row:
                pixels = super_pixel.pixels
                new_image.paste(pixels, (x_offset, y_offset))
                x_offset += (
                    pixels.width
                )  # Using super_pixel width since it could be an edge super pixel
            y_offset += self.super_pixel_size
        return new_image

    def to_scaled_image(self) -> Image.Image:
        new_image = Image.new("RGB", self.size)

        # Paste each average_pixel into the new image at its corresponding position in the grid
        for y_offset, row in enumerate(self.super_pixels):
            x_offset = 0
            for x_offset, super_pixel in enumerate(row):
                pixels = super_pixel.average_pixel
                new_image.paste(pixels, (x_offset, y_offset))
        return new_image
