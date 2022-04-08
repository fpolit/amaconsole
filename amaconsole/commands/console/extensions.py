#!/usr/bin/env python3
#
# Commands to manipulate extensions

import cmd2
import argparse
from cmd2 import with_argparser
from tabulate import tabulate

from amaconsole.commands import CommandCategory as Category
from amaconsole.extensions import load_extensions

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
            table = [[ext_name] for ext_name in self._cmd.extensions]

            self._cmd.poutput(tabulate(table,
                                       headers=['Extensions'],
                                       tablefmt=self.config['CONSOLE']['TABLEFMT']))

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
