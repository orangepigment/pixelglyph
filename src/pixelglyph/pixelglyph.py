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
    scale: float,  # TODO: add default scale?
    width_bound: int | None = None,
    height_bound: int | None = None,
    invert: bool = False,
    color: str | None = None,
    color_mode: ColorMode = ColorMode.BASIC,
):
    # TODO: add upper limit?
    if scale <= 0:
        raise ValueError("scale must be greater than 0")

    if width_bound or 1 <= 0:
        raise ValueError("width bound must be greater than 0")

    if height_bound or 1 <= 0:
        raise ValueError("height bound must be greater than 0")

    # TODO: check file exists
    # TODO: split file reading and image processing into separate functions
    with Image.open(image_filename) as image:
        image = image.convert("L")  # L stands for grayscale

        scaled_width = _bounded_scale(image.width, scale, width_bound)
        scaled_height = _bounded_scale(image.height, scale, height_bound)

        resized = image.resize((scaled_width, scaled_height))

        coloring_enabled = color is not None and sys.stdout.isatty
        if coloring_enabled:
            color_code = get_color_escape_code(color, color_mode)
            print(color_code, end="")

        for y in range(resized.height):
            for x in range(resized.width):
                px = resized.getpixel((x, y))
                _process_pixel(px, x, y, invert)
            print()  # Newline
        if coloring_enabled:
            print(DISABLE_STYLING_CODE)  # Reset output styling
