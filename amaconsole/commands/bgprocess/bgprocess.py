#!/usr/bin/env python3
#
# Background processes - commands

import os
import cmd2
import argparse
from cmd2 import with_argparser

from amaconsole.commands import CommandCategory as Category
from amaconsole.processor import Process
from amaconsole.utils.misc import str2timedelta
from amaconsole.utils import Shell


@cmd2.with_default_category(Category.BGPROCESS)
class BGProcessCmds(cmd2.CommandSet):
    parser = cmd2.Cmd2ArgumentParser(
        formatter_class=argparse.ArgumentDefaultsHelpFormatter
    )
    parser.add_argument('-d', '--depends',
                        nargs='*', help='Dependecy process')
    parser.add_argument('-p', '--priority',
                        type=int, default=0,
                        help='Priority of process')
    parser.add_argument('-D', '--delay',
                        type=str, default='0s',
                        help='Delay of process (e.g: 30s, 2m, 1h, 1h10m, 2h5m10s)')
    parser.add_argument('-n', '--name', default=None,
                        help='Process name')
    parser.add_argument('-o', '--output',
                        completer=cmd2.Cmd.path_complete,
                        default=None,
                        help='Output file')
    parser.add_subparsers(title='command', help='Command to process in background')

    @with_argparser(parser)
    def do_process(self, ns: argparse.Namespace):
        handler = ns.cmd2_handler.get()
        if handler:
            delay = str2timedelta(ns.delay)
            process = Process(
                target=handler,
                args=(ns,),
                depends=ns.depends,
                priority=ns.priority,
                name=ns.name,
                delay=delay,
                outfile=ns.output
            )
            self._cmd.bg_processor.submit(process)

        else:
            self.do_help('process')


    script_parser = cmd2.Cmd2ArgumentParser(
        formatter_class=argparse.ArgumentDefaultsHelpFormatter
    )
    script_parser.add_argument('filepath',
                               completer=cmd2.Cmd.path_complete,
                               help='Path of script file')
    script_parser.add_argument('-b', '--binary-shell',
                               dest='binary_shell',
                               default='/bin/bash',
                               help='Path to binary shell')
    @cmd2.as_subcommand_to('process', 'script', script_parser)
    def process_script(self , args):
        if not os.path.isfile(args.filepath):
            raise FileNotFoundError("Script {filepath} does not exist")

        cmd = [args.binary_shell, args.filepath]
        Shell.exec(cmd)
