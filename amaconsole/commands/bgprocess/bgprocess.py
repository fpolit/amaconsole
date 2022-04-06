#!/usr/bin/env python3
#
# Background processes - commands

import cmd2
import argparse
from cmd2 import with_argparser

from amaconsole.commands import CommandCategory as Category
from amaconsole.utils.misc import str2timedelta
from amaconsole.processor import Process

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
            delay = str2timedelta(args.delay)
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
