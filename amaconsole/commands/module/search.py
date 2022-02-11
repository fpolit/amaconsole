#!/usr/bin/env python3
#
# Commands to search modules and resources (files)
#
# Status: REFACTORED - Dec 8 2021

import argparse
from typing import List, Type
from pathlib import Path
import cmd2
from cmd2 import (
    Cmd,
    CommandSet,
    Cmd2ArgumentParser,
    with_default_category,
    with_argparser
)

from ama.modules import Module
from ama.manager.fullattack import FullAttack
from ama.commands import CommandCategory as Category
from ama.utils.files import search_files as find_files
from ama.utils.modules import modules2table
from ama.utils.fineprint import print_status
from ama.utils.misc import files2table, fullattacks2table

@with_default_category(Category.MODULE)
class Search(CommandSet):
    """
    Commands to search modules and resources (files)
    """

    search_parser = Cmd2ArgumentParser()
    search_subparser = search_parser.add_subparsers(
        title='type',
        help='search type'
    )

    @with_argparser(search_parser)
    def do_search(self, ns: argparse.Namespace):
        """
        Search modules and resources for set module options
        """
        handler = ns.cmd2_handler.get()
        if handler is not None:
            handler(ns)
        else:
            self._cmd.do_help('search')

    files_parser = Cmd2ArgumentParser()
    files_parser.add_argument('dirs', nargs='*',
                              default=None, completer=Cmd.path_complete,
                              help='directories to search')
    files_parser.add_argument('-r', '--recursive',
                              action='store_true',
                              help='recursive search')
    files_parser.add_argument('--setv', dest='variable',
                              default=None, metavar="VARIABLE",
                              help='set variable with results')
    files_parser.add_argument('-g', '--global',
                              dest='global_variable',
                              action='store_true',
                              help='set variable globally')

    filters = files_parser.add_argument_group(title='Filters')
    filters.add_argument('-e', '--extensions',
                         nargs='*', default=None,
                         help='filter by extension')
    files_parser.add_argument('-p', '--pattern',
                              default=None,
                              help='search pattern')
    files_parser.add_argument('-i', '--ignorecase',
                              action='store_true',
                              help='perform case-insensitive matching')
    filters.add_argument('-x', '--exclude', nargs='*',
                         help='files to exclude')

    @cmd2.as_subcommand_to('search', 'files', files_parser)
    def search_files(self, args):
        """
        Search files
        """
        sdirs: List[Path] = []
        if args.dirs:
            sdirs += [Path(sdir) for sdir in args.dirs]
        else:
            sdirs = [Path.cwd()]

        filtered_files = find_files(
            sdirs,
            pattern=args.pattern,
            extensions=args.extensions,
            ignorecase=args.ignorecase,
            recursive=args.recursive,
            exclude=args.exclude
        )

        files2table(filtered_files)

        if args.variable:
            if module := self._cmd.module_manager.active_module:
                module.setv(args.variable, filtered_files)

            if args.global_variable:
                print_status(
                    f"Variable {args.variable}"
                    " value was set globally with the result"
                )
                self._cmd.module_manager.add_global_value(
                    args.variable,
                    filtered_files
                )


    module_parser = argparse.ArgumentParser()
    module_parser.add_argument('-n', '--name',
                               default=None,
                               help="module name pattern")
    module_parser.add_argument('-t', '--type', dest='mtype',
                               default=None,
                               help="module type pattern")
    module_parser.add_argument('-s', '--subtype', dest='mstype',
                               default=None,
                               help="module subtype pattern")
    module_parser.add_argument('-p', '--previous', action='store_true',
                               help="show previous search")

    @cmd2.as_subcommand_to('search', 'module', module_parser)
    def search_module(self, args):
        """
        Search modules
        """
        filtered_modules: List[Type[Module]] = []
        if args.previous:
            filtered_modules = self._cmd.module_manager.filtered_modules
        else:
            filtered_modules = self._cmd.module_manager.search(
                name=args.name,
                mtype=args.mtype,
                mstype=args.mstype
            )

        modules2table(filtered_modules)


    fullattack_parser = argparse.ArgumentParser()
    fullattack_parser.add_argument('-p', '--previous', action='store_true',
                                   help="show previous search")
    @cmd2.as_subcommand_to('search', 'fullattack', fullattack_parser)
    def search_fullattack(self, args):
        """
        Search fullattacks
        """
        filtered_fullattacks: List[FullAttack] = []

        if args.previous:
            filtered_fullattacks = self._cmd.session_manager.filtered_fullattacks
        else:
            filtered_fullattacks = self._cmd.session_manager.find_fullattack()

        fullattacks2table(filtered_fullattacks)
