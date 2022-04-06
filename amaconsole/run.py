#!/usr/bin/env python3
#
# amaconsole executable

import sys
import cmd2
import argparse


from amaconsole.console import AmaConsole
from amaconsole.config import parser

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
    amactld_parser = parser.add_argument_group(title='Amacontroller connection')
    amactld_parser.add_argument('-H', '--host', required=True,
                                dest='controller_host',
                                help='amacontroller host')
    amactld_parser.add_argument('-p', '--port', type=int,
                                dest='controller_port',
                                help='amacontroller port')
    amactld_parser.add_argument('-dP', '--data-port', type=int,
                                dest='controller_data_port',
                                help='amacontroller data port')


    args = parser.parse_args()
    console = None
    try:
        #import pdb; pdb.set_trace()
        console = AmaConsole(config_args=args,
                             config_file=args.config_file,
                             allow_cli_args=False)
        sys.exit(console.cmdloop())

    except KeyboardInterrupt:
        if console:
            print("Closing connection.")

    except Exception as error:
        print(f"[-] Error: {error}")
