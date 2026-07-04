from PIL import Image


class SuperPixel:
    def __init__(
        self,
        source_image: Image.Image,
        x: int,
        y: int,
        size: int,
        average_pixel: tuple,
    ):
        self._source_image = source_image
        self._x = x
        self._y = y
        self._size = size
        self.average_pixel = average_pixel

    @property
    def pixels(self) -> Image.Image:
        left = self._x * self._size
        upper = self._y * self._size
        right = min(left + self._size, self._source_image.size[0])
        lower = min(upper + self._size, self._source_image.size[1])
        return self._source_image.crop((left, upper, right, lower))
