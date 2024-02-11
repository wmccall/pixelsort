import argparse
import logging

from pixelsort.constants import DEFAULTS
from pixelsort.interval import choices as interval_choices
from pixelsort.sorting import choices as sorting_choices


def parse_args():
    parser = argparse.ArgumentParser(description="Pixel mangle an image.")
    parser.add_argument("image", help="Input image file path.")
    parser.add_argument(
        "-o", "--output", help="Output image file path, DEFAULTS to the time created."
    )
    parser.add_argument(
        "-i",
        "--int_function",
        choices=interval_choices.keys(),
        default=DEFAULTS["interval_function"],
        help="Function to determine sorting intervals",
    )
    parser.add_argument(
        "-t",
        "--threshold",
        type=float,
        default=DEFAULTS["lower_threshold"],
        help="Pixels darker than this are not sorted, between 0 and 1",
    )
    parser.add_argument(
        "-u",
        "--upper_threshold",
        type=float,
        default=DEFAULTS["upper_threshold"],
        help="Pixels brighter than this are not sorted, between 0 and 1",
    )
    parser.add_argument(
        "-c",
        "--char_length",
        type=int,
        default=DEFAULTS["char_length"],
        help="Characteristic length of random intervals",
    )
    parser.add_argument(
        "-a",
        "--angle",
        type=float,
        default=DEFAULTS["angle"],
        help="Rotate the image by an angle (in degrees) before sorting",
    )
    parser.add_argument(
        "-p",
        "--super_pixel_size",
        type=int,
        default=DEFAULTS["super_pixel_size"],
        help="Size of super pixel",
    )
    parser.add_argument(
        "-r",
        "--randomness",
        type=float,
        default=DEFAULTS["randomness"],
        help="What percentage of intervals are NOT sorted",
    )
    parser.add_argument("-f", "--int_file", help="Image used for defining intervals.")
    parser.add_argument(
        "-s",
        "--sorting_function",
        choices=sorting_choices.keys(),
        default=DEFAULTS["sorting_function"],
        help="Function to sort pixels by.",
    )
    parser.add_argument(
        "-m", "--mask", help="Image used for masking parts of the image"
    )
    parser.add_argument(
        "-l",
        "--log_level",
        default="WARNING",
        help="Print more or less info",
        choices=["DEBUG", "INFO", "WARNING", "ERROR", "CRITICAL"],
    )

    _args = parser.parse_args()

    logging.basicConfig(
        format="%(name)s: %(levelname)s - %(message)s",
        level=logging.getLevelName(_args.log_level),
    )

    return {
        "image_input_path": _args.image,
        "image_output_path": _args.output,
        "interval_function": _args.int_function,
        "interval_file_path": _args.int_file,
        "lower_threshold": _args.threshold,
        "upper_threshold": _args.upper_threshold,
        "char_length": _args.char_length,
        "angle": _args.angle,
        "super_pixel_size": _args.super_pixel_size,
        "randomness": _args.randomness,
        "sorting_function": _args.sorting_function,
        "mask_path": _args.mask,
    }
