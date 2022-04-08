#!/usr/bin/env python3
#
# String that support coloration

from __future__ import annotations

from abc import ABC, abstractmethod
from typing import List
from colorama import Fore, Back, Style


class ColorHandler(ABC):
    def __init__(self, next_handler: ColorHandler = None):
        self.next_handler = next_handler

    @abstractmethod
    def apply(self, color_texture):
        pass

class ForeColorHandler(ColorHandler):
    def __init__(self, fore_color: Fore, next_handler: ForeColorHandler = None):
        self.fore_color = fore_color
        super().__init__(next_handler)

    def apply(self, msg: str, fore_color: Fore = None) -> str:
        fancy_msg: str = msg
        if fore_color and self.fore_color == fore_color:
            fancy_msg = f"{fore_color}{msg}{Fore.RESET}"
        else:
            if self.next_handler:
                fancy_msg = self.next_handler.apply(msg, fore_color)

        return fancy_msg

class BackColorHandler(ColorHandler):
    def __init__(self, back_color: Fore, next_handler: BackColorHandler = None):
        self.back_color = back_color
        super().__init__(next_handler)

    def apply(self, msg: str, back_color: Back = None) -> str:
        fancy_msg: str = msg
        if back_color and self.back_color == back_color:
            fancy_msg = f"{back_color}{msg}{Back.RESET}"
        else:
            if self.next_handler:
                fancy_msg = self.next_handler.apply(msg, back_color)

        return fancy_msg

class StyleColorHandler(ColorHandler):
    def __init__(self, style: Style, next_handler: StyleColorHandler = None):
        self.style = style
        super().__init__(next_handler)

    def apply(self, msg: str, style: Style = None) -> str:
        fancy_msg: str = msg
        if style and self.style == style:
            fancy_msg = f"{style}{msg}{Style.NORMAL}"
        else:
            if self.next_handler:
                fancy_msg = self.next_handler.apply(msg, style)
        return fancy_msg


class ForeColorChain:
    def __init__(self):
        black_fore_color = ForeColorHandler(Fore.BLACK)
        blue_fore_color = ForeColorHandler(Fore.BLUE, next_handler=black_fore_color)
        cyan_fore_color = ForeColorHandler(Fore.CYAN, next_handler=blue_fore_color)
        green_fore_color = ForeColorHandler(Fore.GREEN, next_handler=cyan_fore_color)
        red_fore_color = ForeColorHandler(Fore.RED, next_handler=green_fore_color)
        white_fore_color = ForeColorHandler(Fore.WHITE, next_handler=red_fore_color)
        yellow_fore_color = ForeColorHandler(Fore.YELLOW, next_handler=white_fore_color)


        self.init_handler = yellow_fore_color

    def apply(self, msg:str, fore_color: Fore = None) -> str:
        return self.init_handler.apply(msg, fore_color)


class BackColorChain:
    def __init__(self):
        black_back_color = BackColorHandler(Fore.BLACK)
        blue_back_color = BackColorHandler(Fore.BLUE, next_handler=black_back_color)
        cyan_back_color = BackColorHandler(Fore.CYAN, next_handler=blue_back_color)
        green_back_color = BackColorHandler(Fore.GREEN, next_handler=cyan_back_color)
        red_back_color = BackColorHandler(Fore.RED, next_handler=green_back_color)
        white_back_color = BackColorHandler(Fore.WHITE, next_handler=red_back_color)
        yellow_back_color = BackColorHandler(Fore.YELLOW, next_handler=white_back_color)


        self.init_handler = yellow_back_color

    def apply(self, msg:str, back_color: Fore = None) -> str:
        return self.init_handler.apply(msg, back_color)


class StyleColorChain:
    def __init__(self):
        normal_style = StyleColorHandler(Style.NORMAL)
        dim_style = StyleColorHandler(Style.DIM, next_handler=normal_style)
        bright_style = StyleColorHandler(Style.BRIGHT, next_handler=dim_style)

        self.init_handler = bright_style

    def apply(self, msg:str, style: Style = None) -> str:
        return self.init_handler.apply(msg, style)


def  color(msg: str, fore: Fore = None, back: Back = None, style: Style = None) -> str:
    fancy_msg: str = ForeColorChain().apply(msg, fore)
    fancy_msg = BackColorChain().apply(fancy_msg, back)
    fancy_msg = StyleColorChain().apply(fancy_msg, style)

    return fancy_msg
