import pytest

from pixelglyph.coloring import (
    ColorMode,
    _get_color_ansi_escape_code,
    _get_extended_color_ansi_escape_code,
    _get_rgb_ansi_escape_code,
    get_color_escape_code,
)


def test_get_color_escape_code():
    # BASIC as default
    assert get_color_escape_code("red") == "\x1b[31m"
    with pytest.raises(ValueError):
        get_color_escape_code("no-such-color")
    # BASIC
    assert get_color_escape_code("bright-red", ColorMode.BASIC) == "\x1b[91m"
    with pytest.raises(ValueError):
        get_color_escape_code("no-such-color", ColorMode.BASIC)
    # EXTENDED
    assert get_color_escape_code("141", ColorMode.EXTENDED) == "\x1b[38;5;141m"
    with pytest.raises(ValueError):
        get_color_escape_code("red", ColorMode.EXTENDED)
    # RGB
    assert (
        get_color_escape_code("255,255,255", ColorMode.RGB) == "\x1b[38;2;255;255;255m"
    )
    with pytest.raises(ValueError):
        get_color_escape_code("red", ColorMode.RGB)


def test_get_color_ansi_escape_code():
    assert _get_color_ansi_escape_code("red") == "\x1b[31m"
    assert _get_color_ansi_escape_code("bright-red") == "\x1b[91m"
    with pytest.raises(ValueError):
        _get_color_ansi_escape_code("no-such-color")


def test_get_extended_color_ansi_escape_code():
    assert _get_extended_color_ansi_escape_code("215") == "\x1b[38;5;215m"
    with pytest.raises(ValueError):
        _get_extended_color_ansi_escape_code("1000")
    with pytest.raises(ValueError):
        _get_extended_color_ansi_escape_code("red")


def test_get_rgb_ansi_escape_code():
    assert _get_rgb_ansi_escape_code((0, 100, 255)) == "\x1b[38;2;0;100;255m"
    with pytest.raises(ValueError):
        _get_rgb_ansi_escape_code("0,1000,255")
    with pytest.raises(ValueError):
        _get_rgb_ansi_escape_code("10,128")
    with pytest.raises(ValueError):
        _get_rgb_ansi_escape_code("not-a-number")
