#!/usr/bin/env python3
#
# Commands to manipulate extensions

import cmd2
import argparse
from cmd2 import with_argparser
from tabulate import tabulate
from colorama import Style

from amaconsole.commands import CommandCategory as Category
from amaconsole.extensions import load_extensions
from amaconsole.utils.misc import commands_count
from amaconsole.utils import color

@cmd2.with_default_category(Category.CONSOLE)
class ExtensionsCommands(cmd2.CommandSet):
    """
    Commands to manipulate extensions
    """

    parser = cmd2.Cmd2ArgumentParser()
    parser.add_subparsers(title='action')

    @with_argparser(parser)
    def do_extensions(self, ns: argparse.Namespace):
        handler = ns.cmd2_handler.get()
        if handler:
            handler(ns)
        else: # List loaded extentions
            #import pdb; pdb.set_trace()
            table = [[name, commands_count(ext), ext.cmd2_default_help_category] for name, ext in self._cmd.extensions.items()]

            self._cmd.poutput(color('Custom Extensions:', style=Style.BRIGHT))
            self._cmd.poutput(tabulate(table,
                                       headers=['Name', 'Commands', 'Category'],
                                       tablefmt=self._cmd.config['CONSOLE']['tablefmt']))

    load_parser = cmd2.Cmd2ArgumentParser()
    load_parser.add_argument('-I', '--include-dir',
                             dest='include_dir',
                             completer=cmd2.Cmd.path_complete,
                             help='Base directory to load extensions')
    load_parser.add_argument('-v', '--verbose',
                             action='store_true',
                             help='verbose mode')

    @cmd2.as_subcommand_to('extensions', 'load', load_parser)
    def extensions_load(self, args):
        for ext in load_extensions(args.include_dir):
            self.register_extension(ext, args.verbose)


    unload_parser = cmd2.Cmd2ArgumentParser()
    unload_parser.add_argument('extname',
                             help='Extension name')
    unload_parser.add_argument('-v', '--verbose',
                             action='store_true',
                             help='verbose mode')

    @cmd2.as_subcommand_to('extensions', 'unload', unload_parser)
    def extensions_unload(self, args):
        self.unregister_extension(args.extname, args.verbose)
