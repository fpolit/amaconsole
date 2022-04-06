#!/usr/bin/env python3
#
# String that support coloration

from typing import List
from colorama import Fore, Back, Style

# from amaconsole.exceptions.utils import (
#     InvalidBackColorError,
#     InvalidForeColorError,
#     InvalidStyleError
# )

VALID_FORE_COLORS = [
    Fore.BLACK,
    Fore.RED,
    Fore.GREEN,
    Fore.YELLOW,
    Fore.MAGENTA,
    Fore.CYAN,
    Fore.WHITE,
    Fore.BLUE
]

VALID_BACK_COLORS = [
    Back.BLACK,
    Back.RED,
    Back.GREEN,
    Back.YELLOW,
    Back.MAGENTA,
    Back.CYAN,
    Back.WHITE
]

VALID_STYLES = [
    Style.DIM,
    Style.NORMAL,
    Style.BRIGHT
]

def array_color(array: List[str],
                fore=None, back=None, style=None) -> List[str]:
    colored_array: List[str] = \
        [color(text, fore=fore, back=back, style=style)
         for text in array]

    return colored_array

def color(string: str, fore=None, back=None, style=None):
    fancy_string = string

    # validate fore , back and style parameters
    if fore and fore not in VALID_FORE_COLORS:
        #raise InvalidForeColorError(fore)
        pass

    if back and back not in VALID_BACK_COLORS:
        #raise InvalidBackColorError(back)
        pass

    if style and style not in VALID_STYLES:
        #raise InvalidStyleError(style)
        pass


    if fore in VALID_FORE_COLORS:
        fancy_string = f"{fore}{fancy_string}{Fore.RESET}"

    if back  in VALID_BACK_COLORS:
        fancy_string = f"{back}{fancy_string}{Back.RESET}"

    if style  in VALID_STYLES:
        fancy_string = f"{style}{fancy_string}{Style.NORMAL}"

    return fancy_string
