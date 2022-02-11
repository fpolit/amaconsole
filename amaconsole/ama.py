#!/usr/bin/env python3
#
# Ama console executable
#
# State: REFACTORED - Nov 29 2021
# Maintainer: glozanoa <glozanoa@uni.pe>

import sys
import argparse

from ama import AMA_HOME
from ama.home import create_ama_home
from ama.console import AmaConsole

from ama.utils.fineprint import print_status, print_successful

def init(args: argparse.Namespace):
    """
    Create ama home and init database
    """
    print_status(f"Initializing Ama-Framework home directory: {AMA_HOME}")
    create_ama_home()


def main():
    """
    Ama console executable
    """

    parser = argparse.ArgumentParser(prog='ama', description="Ama console")
    subparser = parser.add_subparsers()

    init_parser = subparser.add_parser('init',
                                       description="Initialize Ama-Framework home directory")
    init_parser.set_defaults(func=init)

    args = parser.parse_args()
    if 'func' in args:
        args.func(args)
    else:
        console = AmaConsole()
        sys.exit(console.cmdloop())
