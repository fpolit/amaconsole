#!/usr/bin/env python3

from unittest import TestCase
from colorama import Fore, Back, Style

from amaconsole.utils import color


class TestUtilsColor(TestCase):
    def setUp(self):
        self.msg = 'hello'

    def test_color_only_fore(self):
        fancy_msg = f"{Fore.RED}{self.msg}{Fore.RESET}"

        self.assertEqual(color(self.msg, fore=Fore.RED), fancy_msg)

    def test_color_only_back(self):
        fancy_msg = f"{Back.RED}{self.msg}{Back.RESET}"

        self.assertEqual(color(self.msg, back=Back.RED), fancy_msg)

    def test_color_only_style(self):
        fancy_msg = f"{Style.BRIGHT}{self.msg}{Style.NORMAL}"

        self.assertEqual(color(self.msg, style=Style.BRIGHT), fancy_msg)

    def test_color_mix(self):
        fancy_msg = f"{Fore.RED}{self.msg}{Fore.RESET}"
        fancy_msg = f"{Back.RED}{fancy_msg}{Back.RESET}"
        fancy_msg = f"{Style.BRIGHT}{fancy_msg}{Style.NORMAL}"

        self.assertEqual(
            fancy_msg,
            color(self.msg,
                  fore=Fore.RED,
                  back=Back.RED,
                  style=Style.BRIGHT)
        )
