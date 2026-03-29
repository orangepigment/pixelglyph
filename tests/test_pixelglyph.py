import pytest

from pixelglyph.pixelglyph import _bounded_scale, _process_pixel, _to_char


def test_bounded_scale():
    # Default usage
    assert _bounded_scale(100, 0.3) == 30
    assert _bounded_scale(100, 1.2) == 120
    # Result cannopt exceed bound param
    assert _bounded_scale(100, 0.3, bound=20) == 20
    # Minimum scaled size is 1
    assert _bounded_scale(100, 0.002) == 1


def test_to_char():
    # Default char table tests
    assert (_to_char(0)) == " "
    assert (_to_char(255)) == "█"


def test_process_pixel(capsys):
    _process_pixel(255, x=10, y=33, invert=False)
    captured = capsys.readouterr()
    assert captured.out == "█ "

    with pytest.raises(ValueError) as true_color_error:
        _process_pixel((255, 255, 255), x=10, y=33, invert=False)
    assert "True color mode is not supported" in str(true_color_error)

    with pytest.raises(ValueError) as unexpected_pixel_error:
        _process_pixel(px=None, x=10, y=33, invert=False)
    assert "Unexpected pixel value: None at (10,33) coordinates" in str(
        unexpected_pixel_error
    )
