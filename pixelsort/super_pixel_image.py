from PIL import Image

from pixelsort.util import image_to_2d_super_pixel_array


class SuperPixelImage:
    def __init__(self, image: Image.Image, super_pixel_size: int):
        self.super_pixels = image_to_2d_super_pixel_array(
            image=image,
            super_pixel_size=super_pixel_size,
        )
        self.super_pixel_size = super_pixel_size
        self.original_size = image.size
        self.size = (len(self.super_pixels), len(self.super_pixels[0]))
