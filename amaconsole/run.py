#!/usr/bin/env python3
#
# amaconsole executable

import sys
import cmd2
import argparse


from amaconsole.console import AmaConsole
from amaconsole.parsers import (
    parser,
    ctrlparser,
    cmdparser
)

def main():
    """
    Run amaconsole
    """

    parser.prog='amaconsole'
    parser.description='Ama console'

    parser.add_argument('-I', '--include-dir', dest='include_dir',
                        completer=cmd2.Cmd.path_complete,
                        help='Include directory of extensions')
    parser.add_argument('-c', '--config-file', dest='config_file',
                        help='Configuration File')

    ctrlparser.add_argument('-H', '--host',
                            dest='controller_host',
                            help='amacontroller host')

    cmdparser.add_argument('-v', '--verbose',
                           action='store_true',
                           help='Verbose mode')
    cmdparser.add_argument('-d', '--debug',
                           action='store_true',
                           help='Debug mode')
    cmdparser.add_argument('--loglevel',
                           default=10,
                           choices=[0, 10, 20, 30, 40, 50],
                           type=int,
                           help='Log level for stream handler (used in debug mode)')


    args = parser.parse_args()
    console = None
    try:
        #import pdb; pdb.set_trace()
        console = AmaConsole(config_args=args,
                             config_file=args.config_file,
                             verbose=args.verbose,
                             allow_cli_args=False)
        sys.exit(console.cmdloop())

    except KeyboardInterrupt:
        if console:
            print("Closing connection.")

    except Exception as error:
        print(f"[-] Error: {error}")
