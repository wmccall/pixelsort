import functools
import typing

from pixelsort.super_pixel_image import SuperPixel


@functools.cache
def lightness(super_pixel: SuperPixel) -> float:
    """Sort by the lightness of a pixel according to a HLS representation."""
    # taken from rgb_to_hls
    pixel = super_pixel.average_pixel
    r, g, b = pixel[:3]
    maxc = max(r, g, b)
    minc = min(r, g, b)
    return (minc + maxc) / 2.0


@functools.cache
def hue(super_pixel: SuperPixel) -> float:
    """Sort by the hue of a pixel according to a HLS representation."""
    # taken from rgb_to_hls
    pixel = super_pixel.average_pixel
    r, g, b = pixel[:3]
    maxc = max(r, g, b)
    minc = min(r, g, b)
    # XXX Can optimize (maxc+minc) and (maxc-minc)
    if minc == maxc:
        return 0.0
    mcminusmc = maxc - minc
    rc = (maxc - r) / mcminusmc
    gc = (maxc - g) / mcminusmc
    bc = (maxc - b) / mcminusmc
    if r == maxc:
        h = bc - gc
    elif g == maxc:
        h = 2.0 + rc - bc
    else:
        h = 4.0 + gc - rc
    h = (h / 6.0) % 1.0
    return h


@functools.cache
def saturation(super_pixel: SuperPixel) -> float:
    """Sort by the saturation of a pixel according to a HLS representation."""
    # taken from rgb_to_hls
    pixel = super_pixel.average_pixel
    r, g, b = pixel[:3]
    maxc = max(r, g, b)
    minc = min(r, g, b)
    l = (minc + maxc) / 2.0
    if minc == maxc:
        return 0.0
    if l <= 0.5:
        s = (maxc - minc) / (maxc + minc)
    else:
        s = (maxc - minc) / (2.0 - maxc - minc)
    return s


def intensity(super_pixel: SuperPixel) -> int:
    """Sort by the intensity of a pixel, i.e. the sum of all the RGB values."""
    pixel = super_pixel.average_pixel
    return pixel[0] + pixel[1] + pixel[2]


def minimum(super_pixel: SuperPixel) -> int:
    """Sort on the minimum RGB value of a pixel (either the R, G or B)."""
    pixel = super_pixel.average_pixel
    return min(pixel[0], pixel[1], pixel[2])


choices = {
    "lightness": lightness,
    "hue": hue,
    "intensity": intensity,
    "minimum": minimum,
    "saturation": saturation,
}
