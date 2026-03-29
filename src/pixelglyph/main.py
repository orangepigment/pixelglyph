import argparse
import sys

from pixelglyph.coloring import ColorMode
from pixelglyph.pixelglyph import print_ascii_image


def app():
    # TODO: support providing custom char class tables.
    # TODO: add several predefined tables with differen number of characters
    # TODO: add support for weighted char tables
    # TODO: add mutually exlusive option groups where needed
    parser = argparse.ArgumentParser(
        prog="pixelglyph", description="CLI app for rendering images as ascii art"
    )
    parser.add_argument("-i", "--input", required=True, help="path to the input image")
    parser.add_argument(
        "-s", "--scale", type=float, default=0.1, help="Scaling coefficient"
    )
    parser.add_argument(
        "-hb", "--height-bound", type=int, help="Upper bound for image height in pixels"
    )
    parser.add_argument(
        "-wb", "--width-bound", type=int, help="Upper bound for image width in pixels"
    )

    # TODO: support names, codes, extended codes, RGB codes
    parser.add_argument(
        "-cm",
        "--color-mode",
        type=ColorMode,
        choices=[color.value for color in ColorMode],
        default=ColorMode.BASIC,
        help="Color mode. Determines color selection and color code fomat.",
    )

    parser.add_argument(
        "-c",
        "--color",
        help="Color code. Use color names in BASIC mode (e.g. red or bright-red),\
        integer values [0;255] in EXTENDED mode\
        and tuple in RGB mode (e.g. 255,255,255)",
    )

    parser.add_argument(
        "-n",
        "--negative",
        action="store_true",
        help="invert pixel values for selecting characters",
    )

    args = parser.parse_args()

    try:
        print_ascii_image(
            image_filename=args.input,
            scale=args.scale,
            width_bound=args.width_bound,
            height_bound=args.height_bound,
            color=args.color,
            color_mode=args.color_mode,
            invert=args.negative,
        )
    except Exception as e:
        print(e)
        sys.exit(1)


if __name__ == "__main__":
    app()
