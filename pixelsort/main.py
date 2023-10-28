import logging
import typing

from PIL import Image

# python implementation of the PixelAccess class returned by im.load(), has the same functions so is fine for type hints
from PIL import PyAccess

from pixelsort.constants import DEFAULTS
from pixelsort.interval import choices as interval_choices
from pixelsort.sorter import sort_image
from pixelsort.sorting import choices as sorting_choices
from pixelsort.util import crop_to, downscale_image
from pixelsort.super_pixel_image import (
    SuperPixelImage,
    SuperPixel,
    calculate_scaled_size,
)


def pixelsort(
    image: Image.Image,
    mask_image: typing.Optional[Image.Image] = None,
    interval_image: typing.Optional[Image.Image] = None,
    randomness: float = DEFAULTS["randomness"],
    char_length: float = DEFAULTS["char_length"],
    sorting_function: typing.Literal[
        "lightness", "hue", "saturation", "intensity", "minimum"
    ] = DEFAULTS["sorting_function"],
    interval_function: typing.Literal[
        "random", "threshold", "edges", "waves", "file", "file-edges", "none"
    ] = DEFAULTS["interval_function"],
    lower_threshold: float = DEFAULTS["lower_threshold"],
    upper_threshold: float = DEFAULTS["upper_threshold"],
    angle: float = DEFAULTS["angle"],
    super_pixel_size: int = DEFAULTS["super_pixel_size"],
) -> Image.Image:
    """
    pixelsorts an image
    :param image: image to pixelsort
    :param mask_image: Image used for masking parts of the image.
    :param interval_image: Image used to define intervals. Must be black and white.
    :param randomness: What percentage of intervals *not* to sort. 0 by default.
    :param char_length:	Characteristic length for the random width generator. Used in mode `random` and `waves`.
    :param sorting_function: Sorting function to use for sorting the pixels.
    :param interval_function: Controls how the intervals used for sorting are defined.
    :param lower_threshold: How dark must a pixel be to be considered as a 'border' for sorting? Takes values from 0-1.
        Used in edges and threshold modes.
    :param upper_threshold: How bright must a pixel be to be considered as a 'border' for sorting? Takes values from
        0-1. Used in threshold mode.
    :param angle: Angle at which you're pixel sorting in degrees.
    :param super_pixel_size:
    :return: pixelsorted image
    """
    original = image
    image = image.convert("RGBA").rotate(angle, expand=True)

    logging.debug("Converting to SuperPixelImage...")
    super_pixel_image = SuperPixelImage(image=image, super_pixel_size=super_pixel_size)

    logging.debug("Loading Mask...")
    mask_image = (
        mask_image
        if mask_image
        else Image.new(
            "1", calculate_scaled_size(original.size, super_pixel_size), color=255
        )
    )
    mask_image = mask_image.convert("1").rotate(angle, expand=True, fillcolor=0)
    mask_data = mask_image.load()

    logging.debug("Loading Interval Image...")
    if interval_image:
        threshold = 200
        fn = lambda x: 255 if x > threshold else 0
        interval_image = interval_image.resize(
            calculate_scaled_size(original.size, super_pixel_size)
        )
        interval_image = interval_image.convert("L").point(fn, mode="1")
        interval_image = interval_image.rotate(angle, expand=True)

    logging.debug("Determining intervals...")
    intervals = interval_choices[interval_function](
        super_pixel_image,
        lower_threshold=lower_threshold,
        upper_threshold=upper_threshold,
        char_length=char_length,
        interval_image=interval_image,
    )
    logging.debug("Sorting pixels...")
    sorted_pixels = sort_image(
        super_pixel_image.size,
        super_pixel_image,
        mask_data,
        intervals,
        randomness,
        sorting_choices[sorting_function],
    )

    output_img = _place_pixels(sorted_pixels, mask_data, super_pixel_image)
    if angle != 0:
        output_img = output_img.rotate(-angle, expand=True)
        output_img = crop_to(output_img, original)

    final_image = original.convert("RGBA")
    # Create a binary mask where 0 (fully transparent) is treated as 0 (transparent), and any other value is treated as 255 (opaque)
    final_mask = output_img.getchannel("A").point(lambda p: p > 0, mode="1")

    # Squash pixel sorted image onto original to ensure no unexpected transparencies
    final_image.paste(output_img, (0, 0), final_mask)

    return final_image


def _place_pixels(
    pixels: list[list[SuperPixel]],
    mask: PyAccess.PyAccess,
    super_pixel_image: SuperPixelImage,
):
    super_pixel_size = super_pixel_image.super_pixel_size
    output_img = Image.new("RGBA", super_pixel_image.original_size)
    size = super_pixel_image.size
    for y in range(size[1]):
        count = 0
        for x in range(size[0]):
            if not mask[x, y]:
                output_img.paste(
                    super_pixel_image.super_pixels[x, y].pixels,
                    (x * super_pixel_size, y * super_pixel_size),
                )
            else:
                output_img.paste(
                    pixels[y][count].pixels,
                    (x * super_pixel_size, y * super_pixel_size),
                )
                count += 1
    return output_img
