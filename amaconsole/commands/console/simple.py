#!/usr/bin/env python3
#
# Simple commands for ama console
#
# Status: REFACTORED - Dec 8 2021

import cmd2
from colorama import Style

from ama import VERSION
from ama.commands import CommandCategory as Category
from ama.utils.fineprint import print_status
from ama.utils import color
from ama.utils.misc import tips2table

@cmd2.with_default_category(Category.CONSOLE)
class SimpleCmds(cmd2.CommandSet):
    """
    Simple commands for ama console
    """

    def do_exit(self,  _: cmd2.Statement):
        """
        Exit console
        """
        return True

    def do_version(self, _: cmd2.Statement):
        """
        Print Ama-Framework's version
        """
        print_status(f"Ama version: {color(VERSION, style=Style.BRIGHT)}")

    def do_banner(self, _: cmd2.Statement):
        """
        Print fancy Ama-Framework's banner
        """

        print(self._cmd.banner_generator.random())

    def do_tips(self, _: cmd2.Statement):
        """
        Print some useful tips
        """

        tips2table(self._cmd.banner_generator.tips)
