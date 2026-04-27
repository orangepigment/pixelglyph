#!/usr/bin/env python3

import sys
from math import ceil, floor

from PIL import Image

from pixelglyph.coloring import (
    DISABLE_STYLING_CODE,
    ColorMode,
    get_color_escape_code,
)

# TODO: extract char map handling into a separate file
# Add support for custom chr maps
_DEFAULT_CHARS = [
    " ",  # Black
    ".",
    "░",
    "▒",
    "▓",
    "█",  # White
]


# TODO: validate pixel bounds?
def _to_char(pixel: int, chars: list[str] = _DEFAULT_CHARS) -> str:
    # Gray pixels are in range 0 to 255
    class_power = ceil(255 / len(chars))
    pixel_class: int = floor(pixel / class_power)
    return chars[pixel_class]


def _bounded_scale(size: int, scale: float, bound: int | None = None) -> int:
    scaled: int = round(size * scale)
    return max(min(scaled, bound or scaled), 1)


def _process_pixel(px: float | tuple[int, ...] | None, x: int, y: int, invert: bool):
    match px:
        case int():
            px = (255 - px) if invert else px
            # TODO: write to an explicit pipe
            print(_to_char(px), end=" ")
        case (_, _, _):
            raise ValueError("True color mode is not supported")
        case _:
            raise ValueError(f"Unexpected pixel value: {px} at ({x},{y}) coordinates")


def print_ascii_image(
    image_filename: str,
    scale: float,
    size_bound: int,
    invert: bool = False,
    color: str | None = None,
    color_mode: ColorMode = ColorMode.BASIC,
):
    # TODO: add upper limit?
    if scale <= 0:
        raise ValueError("scale must be greater than 0")

    if size_bound <= 0:
        print(f"size_bound: {size_bound}")
        raise ValueError("size bound must be greater than 0")

    # TODO: check file exists
    # TODO: split file reading and image processing into separate functions
    with Image.open(image_filename) as image:
        # Set conversion depending on colormode
        # L stands for grayscale
        image = image.convert("L")

        # TODO: extract to a function and add test for bounds evaluating
        if image.height > image.width:
            height_bound = size_bound or image.height
            width_bound = ceil(height_bound * (image.width / image.height))
        else:
            width_bound = size_bound or image.height
            height_bound = ceil(width_bound * (image.height / image.width))

        scaled_width = _bounded_scale(image.width, scale, width_bound)
        scaled_height = _bounded_scale(image.height, scale, height_bound)

        resized = image.resize((scaled_width, scaled_height))

        match color:
            # For MultiColor we set colro for each pixel
            case str() if sys.stdout.isatty:
                color_code = get_color_escape_code(color, color_mode)
                print(color_code, end="")
                coloring_enabled = True
            case _:
                coloring_enabled = False

        for y in range(resized.height):
            for x in range(resized.width):
                px = resized.getpixel((x, y))
                _process_pixel(px, x, y, invert)
            print()  # Newline
        if coloring_enabled:
            print(DISABLE_STYLING_CODE)  # Reset output styling
