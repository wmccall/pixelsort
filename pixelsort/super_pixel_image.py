from PIL import Image

from pixelsort.super_pixel import SuperPixel


class SuperPixelImage:
    def __init__(self, image: Image.Image, super_pixel_size: int):
        self.super_pixel_size = super_pixel_size
        self.original_size = image.size
        self.scaled_image = (
            image.reduce(super_pixel_size) if super_pixel_size > 1 else image
        )
        self.size = self.scaled_image.size
        average_data = self.scaled_image.load()
        self.super_pixels = {
            (x, y): SuperPixel(image, x, y, super_pixel_size, average_data[x, y])
            for x in range(self.size[0])
            for y in range(self.size[1])
        }
