from enum import StrEnum
from functools import singledispatch


class ColorMode(StrEnum):
    BASIC = "BASIC"
    EXTENDED = "EXTENDED"
    RGB = "RGB"


_ANSI_FG_COLORS = {
    "black": "\x1b[30m",
    "red": "\x1b[31m",
    "green": "\x1b[32m",
    "yellow": "\x1b[33m",
    "blue": "\x1b[34m",
    "magenta": "\x1b[35m",
    "cyan": "\x1b[36m",
    "white": "\x1b[37m",
    "bright-black": "\x1b[90m",
    "bright-red": "\x1b[91m",
    "bright-green": "\x1b[92m",
    "bright-yellow": "\x1b[93m",
    "bright-blue": "\x1b[94m",
    "bright-magenta": "\x1b[95m",
    "bright-cyan": "\x1b[96m",
    "bright-white": "\x1b[97m",
}

DISABLE_STYLING_CODE = "\x1b[0m"

# TODO: add custom exceptions hierarchy
_INVALID_BASIC_COLOR = ValueError("Basic color code must be a string")
_INVALID_EXTENDED_COLOR = ValueError(
    "Extended color code must be an int in [0;255] range"
)
_INVALID_RGB_COLOR = ValueError(
    "RGB color code must be a tuple of three ints in [0;255] range. Eg, 255,255,255"
)


def get_color_escape_code(color: str, mode: ColorMode = ColorMode.BASIC) -> str:
    match mode:
        case ColorMode.BASIC:
            return _get_color_ansi_escape_code(color)
        case ColorMode.EXTENDED:
            return _get_extended_color_ansi_escape_code(color)
        case ColorMode.RGB:
            return _get_rgb_ansi_escape_code(color)


# TODO: add setting/functions for fg/bg
def _get_color_ansi_escape_code(color: str) -> str:
    code = _ANSI_FG_COLORS.get(color)
    if code is None:
        raise _INVALID_BASIC_COLOR
    return code


@singledispatch
def _get_extended_color_ansi_escape_code(color_code: int) -> str:
    if 0 <= color_code <= 255:
        return f"\x1b[38;5;{color_code}m"
    else:
        raise _INVALID_EXTENDED_COLOR


@_get_extended_color_ansi_escape_code.register
def _(color: str) -> str:
    if color.isdecimal():
        color_code = int(color)
        return _get_extended_color_ansi_escape_code(color_code)
    else:
        raise ValueError("BOOM")


@singledispatch
def _get_rgb_ansi_escape_code(rgb: tuple[int, int, int]) -> str:
    if 0 <= rgb[0] <= 255 and 0 <= rgb[1] <= 255 and 0 <= rgb[2] <= 255:
        return f"\x1b[38;2;{rgb[0]};{rgb[1]};{rgb[2]}m"
    else:
        raise _INVALID_RGB_COLOR


@_get_rgb_ansi_escape_code.register
def _(rgb: str) -> str:
    color_components = rgb.split(",")
    match color_components:
        case (r_str, g_str, b_str) if (
            r_str.isdecimal and g_str.isdecimal and b_str.isdecimal
        ):
            red = int(r_str)
            green = int(g_str)
            blue = int(b_str)

            return _get_rgb_ansi_escape_code((red, green, blue))
        case _:
            raise _INVALID_RGB_COLOR
