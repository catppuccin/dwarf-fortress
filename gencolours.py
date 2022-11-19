#!/usr/bin/env python3
"""
Generates a Dwarf Fortress (hereafter "DF") `colors.txt` file for each flavour
of Catppuccin.
"""

from enum import Enum, auto
from pathlib import Path
from typing import TextIO

from catppuccin import Colour, Flavour

# how much to darken/lighten colours
COLOUR_MOD_PERCENT = 1.4


class ColourOp(Enum):
    LIGHTEN = auto()
    DARKEN = auto()


# map DF colour names to Catppuccin colour names.
scheme = {
    "black": {"colour": "base"},
    "blue": {"colour": "blue"},
    "green": {"colour": "green"},
    "cyan": {"colour": "teal"},
    "red": {"colour": "red"},
    "magenta": {"colour": "mauve"},
    "brown": {"colour": "rosewater", "op": ColourOp.DARKEN},
    "lgray": {"colour": "overlay2"},
    "dgray": {"colour": "surface2"},
    "lblue": {"colour": "sky"},
    "lgreen": {"colour": "green", "op": ColourOp.LIGHTEN},
    "lcyan": {"colour": "teal", "op": ColourOp.LIGHTEN},
    "lred": {"colour": "pink"},
    "lmagenta": {"colour": "lavender"},
    "yellow": {"colour": "yellow"},
    "white": {"colour": "text"},
}


def redistribute_rgb(r, g, b):
    """
    all credit to: https://stackoverflow.com/a/141943
    """
    threshold = 255.999
    m = max(r, g, b)
    if m <= threshold:
        return int(r), int(g), int(b)
    total = r + g + b
    if total >= 3 * threshold:
        return int(threshold), int(threshold), int(threshold)
    x = (3 * threshold - total) / (3 * m - total)
    gray = threshold - x * m
    return int(gray + x * r), int(gray + x * g), int(gray + x * b)


def lighten(colour: Colour) -> Colour:
    r = colour.red * COLOUR_MOD_PERCENT
    g = colour.green * COLOUR_MOD_PERCENT
    b = colour.blue * COLOUR_MOD_PERCENT
    return Colour(*redistribute_rgb(r, g, b))


def darken(colour: Colour) -> Colour:
    r = colour.red / COLOUR_MOD_PERCENT
    g = colour.green / COLOUR_MOD_PERCENT
    b = colour.blue / COLOUR_MOD_PERCENT
    return Colour(*redistribute_rgb(r, g, b))


def write_colours(flavour: Flavour, *, fp: TextIO) -> None:
    for df, ctp in scheme.items():
        colour = getattr(flavour, ctp["colour"])

        match ctp.get("op"):
            case ColourOp.LIGHTEN:
                colour = lighten(colour)
            case ColourOp.DARKEN:
                colour = darken(colour)

        df = df.upper()
        print(f"[{df}_R:{colour.red}]", file=fp)
        print(f"[{df}_G:{colour.green}]", file=fp)
        print(f"[{df}_B:{colour.blue}]", file=fp)


for flavour in "latte", "frappe", "macchiato", "mocha":
    output_dir = Path(flavour)
    output_dir.mkdir(parents=True, exist_ok=True)
    colors_txt = output_dir / "colors.txt"

    flavour = getattr(Flavour, flavour)()  # >:)
    with colors_txt.open("w") as fp:
        write_colours(flavour, fp=fp)
