#!/usr/bin/env python3

import os
import argparse
from typing import List
import cmd2
from cmd2 import (
    Cmd,
    CommandSet,
    Cmd2ArgumentParser,
    with_default_category,
    with_argparser
)

from amaconsole.commands import CommandCategory

@with_default_category(CommandCategory.RESMAN)
class RegisterCommands(CommandSet):
    """Register - Resource Manager Commands"""

    register_parser = Cmd2ArgumentParser()
    register_subparser = register_parser.add_subparsers(
        title='type',
        help='Resource type to register'
    )

    @with_argparser(register_parser)
    def do_register(self, ns: argparse.Namespace):
        """
        Search modules and resources for set module options
        """
        handler = ns.cmd2_handler.get()
        if handler is not None:
            handler(ns)
        else:
            self._cmd.do_help('register')

    wordlists_parser = Cmd2ArgumentParser()
    wlorigin = wordlists_parser.add_mutually_exclusive_group(required=True)
    wlorigin.add_argument('-w', '--wordlists', nargs='+',
                          completer=Cmd.path_complete,
                          help='wordlists paths')
    wlorigin.add_argument('-wf', '--wordlists-file', dest='wlfile',
                          completer=Cmd.path_complete,
                          help='File of wordlists (one path per line)')

    wordlists_parser.add_argument('-t', '--threads',type=int,
                                  help='maximun number of threads')
    wordlists_parser.add_argument('-r', '--replica', nargs='+',
                                  help='Nodes to replica wordlists (default: ALL)')
    @cmd2.as_subcommand_to('register', 'wordlists', wordlists_parser)
    def register_wordlists(self, args):
        """
        Register wordlists in nodes
        """
        wordlists: List[str] = []

        if args.wordlists:
            for wl in args.wordlists:
                if os.path.isfile(wl) and os.access(wl, os.R_OK):
                    wordlists.append(wl)

        else:
            with open(args.wlfile, 'r') as wls:
                for wl in wls:
                    if os.path.isfile(wl) and os.access(wl, os.R_OK):
                        wordlists.append(wl)

        if not wordlists:
            raise Exception('No valid wordlists file was supplied')

        ## verificate replicas

        print(f"W")

        ## SEND WORDLISTS

    masksfiles_parser = Cmd2ArgumentParser()
    masksorigin = wordlists_parser.add_mutually_exclusive_group(required=True)
    masksorigin.add_argument('-m', '--masksfiles', nargs='+',
                          completer=Cmd.path_complete,
                          help='masksfiles paths')
    masksorigin.add_argument('-mf', '--masksfiles-file', dest='mfile',
                          completer=Cmd.path_complete,
                          help='File of maksfiles (one path per line)')

    wordlists_parser.add_argument('-t', '--threads',type=int,
                                  help='maximun number of threads')
    wordlists_parser.add_argument('-r', '--replica', nargs='+',
                                  help='Nodes to replica wordlists (default: ALL)')
    @cmd2.as_subcommand_to('register', 'masks', masksfiles_parser)
    def register_masks(self, args):
        """
        Register wordlists in nodes
        """
        masksfiles: List[str] = []

        if args.masksfiles:
            for wl in args.masksfiles:
                if os.path.isfile(wl) and os.access(wl, os.R_OK):
                    masksfiles.append(wl)

        else:
            with open(args.mfile, 'r') as mfs:
                for mf in mfs:
                    if os.path.isfile(mf) and os.access(mf, os.R_OK):
                        masksfiles.append(mf)

        if not masksfiles:
            raise Exception('No valid masks file was supplied')

        ## verificate replicas

        print(f"MF")

        ## SEND hashes


    rulesfiles_parser = Cmd2ArgumentParser()
    rulesorigin = rulesfiles_parser.add_mutually_exclusive_group(required=True)
    rulesorigin.add_argument('-r', '--rulesfiles', nargs='+',
                             completer=Cmd.path_complete,
                             help='masksfiles paths')
    rulesorigin.add_argument('-rf', '--rulesfiles-file', dest='rfile',
                             completer=Cmd.path_complete,
                             help='File of rulesfiles (one path per line)')

    rulesfiles_parser.add_argument('-t', '--threads',type=int,
                                   help='maximun number of threads')
    rulesfiles_parser.add_argument('-r', '--replica', nargs='+',
                                   help='Nodes to replica wordlists (default: ALL)')
    @cmd2.as_subcommand_to('register', 'rules', rulesfiles_parser)
    def register_rules(self, args):
        """
        Register wordlists in nodes
        """
        rulesfiles: List[str] = []

        if args.rulesfiles:
            for rf in args.rulesfiles:
                if os.path.isfile(rf) and os.access(rf, os.R_OK):
                    rulesfiles.append(rf)

        else:
            with open(args.rfile, 'r') as rfs:
                for rf in rfs:
                    if os.path.isfile(rf) and os.access(rf, os.R_OK):
                        rulesfiles.append(rf)

        if not rulesfiles:
            raise Exception('No valid rules file was supplied')

        ## verificate replicas

        print(f"RF")

        ## SEND hashes
