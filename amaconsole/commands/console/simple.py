#!/usr/bin/env python3
#
# Simple commands for ama console
#
# Status: REFACTORED - Dec 8 2021

import cmd2
from colorama import Style
from tabulate import tabulate
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
        Print Ama-Framework component versions
        """
        ama_versions = self._cmd._get_ama_component_versions()

        table = [[component, version] for component, version in ama_versions.items()]

        self._cmd.poutput(tabulate(table,
                                   headers=['Component', 'Version'],
                                   tablefmt=self._cmd.config['CONSOLE']['tablefmt']))

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

    def do_pdbtrace(self, _: cmd2.Statement):
        import pdb; pdb.set_trace()
