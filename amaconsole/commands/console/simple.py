#!/usr/bin/env python3
#
# Simple commands for ama console
#
# Status: REFACTORED - Dec 8 2021

import cmd2
from colorama import Style

from amaconsole import AMACONSOLE_VERSION
from amaconsole.commands import CommandCategory as Category
from amaconsole.utils import color
#from ama.utils.misc import tips2table

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
        self.poutput(f"Ama version: {color(AMACONSOLE_VERSION, style=Style.BRIGHT)}")

    def do_banner(self, _: cmd2.Statement):
        """
        Print fancy Ama-Framework's banner
        """

        print(self._cmd.banner_generator.random())

    def do_tips(self, _: cmd2.Statement):
        """
        Print some useful tips
        """
        pass
        #tips2table(self._cmd.banner_generator.tips)
