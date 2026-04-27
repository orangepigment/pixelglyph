# PixelGlyph

PixelGlyph is a command-line app for rendering iamges as ASCII-art.
It uses [Pillow](https://pillow.readthedocs.io/en/stable/index.html) for loading images and then output the image as a set ASCII characters depedning on pixel values.

## Installation

## Usage

Basic command syntax:

```shell
pixelglyph -i <path-to-image>
```

Help mesage:

```
usage: pixelglyph [-h] -i INPUT [-s SCALE] [-sb SIZE_BOUND]
                  [-cm {BASIC,EXTENDED,RGB}] [-c COLOR] [-n]

CLI app for rendering images as ascii art

options:
  -h, --help            show this help message and exit
  -cm, --color-mode {BASIC,EXTENDED,RGB}
                        Color mode. Determines color selection and color code
                        fomat.
  -c, --color COLOR     Color code. Use color names in BASIC mode (e.g. red or
                        bright-red), integer values [0;255] in EXTENDED mode
                        and tuple in RGB mode (e.g. 255,255,255).This option
                        is ignored in MULTICOLOR mode.
  -n, --negative        invert pixel values for selecting characters

Resize control:
  Options for changing image size

  -i, --input INPUT     path to the input image
  -s, --scale SCALE     Scaling coefficient
  -sb, --size-bound SIZE_BOUND
                        Upper bound for the larger image size in pixels.Value
                        will be scaled proportionally for the smaller side.
```

## Roadmap

- [ ] Add more granular user-friendly error handling
- [x] Write tests
- [ ] Write advanced tests
- [ ] Write documentation
- [x] Add CI pipeline for building and running tests
- [x] Add support for extended ANSI colors and RGB
- [ ] Add support for background coloring
- [ ] Add multicolor mode
- [ ] Add support for effects (e.g. blinking)
- [ ] Add support for loading images from URL
- [ ] Add a directory with examples
- [ ] Publish to PyPi
