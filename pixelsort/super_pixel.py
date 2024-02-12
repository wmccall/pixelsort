from PIL import Image


class SuperPixel:
    def __init__(self, pixels: Image):
        self.pixels = pixels
        self.average_pixel = pixels.resize((1, 1)).load()[0, 0]
