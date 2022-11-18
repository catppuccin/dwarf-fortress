#!/usr/bin/env python3
"""
Generates a Dwarf Fortress (hereafter "DF") `colors.txt` file for each flavour
of Catppuccin.
"""

from pathlib import Path
from typing import TextIO

from catppuccin import Colour, Flavour

LIGHTEN_PERCENT = 1.2

# map DF colour names to Catppuccin colour names.
# prefix with light: to lighten the colour.
scheme = {
    "black": "base",
    "blue": "blue",
    "green": "green",
    "cyan": "teal",
    "red": "red",
    "magenta": "mauve",
    "brown": "rosewater",
    "lgray": "overlay2",
    "dgray": "surface2",
    "lblue": "sky",
    "lgreen": "light:green",
    "lcyan": "light:teal",
    "lred": "pink",
    "lmagenta": "lavender",
    "yellow": "yellow",
    "white": "text",
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
    r = colour.red * LIGHTEN_PERCENT
    g = colour.green * LIGHTEN_PERCENT
    b = colour.blue * LIGHTEN_PERCENT
    return Colour(*redistribute_rgb(r, g, b))


def write_colours(flavour: Flavour, *, fp: TextIO) -> None:
    for df, ctp in scheme.items():
        light = False
        if ctp.startswith("light:"):
            ctp = ctp[len("light:") :]
            light = True

        colour = getattr(flavour, ctp)
        if light:
            colour = lighten(colour)

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
