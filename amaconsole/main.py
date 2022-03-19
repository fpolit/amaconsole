#!/usr/bin/env python3
#
# amaconsole executable

import sys
import argparse

from amaconsole.console import AmaConsole


def run():
    """
    Run amaconsole
    """

    parser = argparse.ArgumentParser(prog='amaconsole', description="Ama console")
    parser.add_argument('-H', '--host', required=True,
                        help='amactld host')
    parser.add_argument('-p', '--port', type=int, default=10001,
                        help='amactld port')
    parser.add_argument('-dp', '--data-port', dest='dport',
                        type=int, default=10101,
                        help='amactld data port')
    parser.add_argument('-t', '--threads', type=int, default=8,
                        help='Maximun active threads')
    parser.add_argument('-v', '--verbose', action='store_true',
                        help='Verbose mode')

    args = parser.parse_args()
    console = None
    try:
        console = AmaConsole(args.host, args.port, args.dport,
                             threads=args.threads,
                             verbose=args.verbose)
        sys.exit(console.cmdloop())
    except KeyboardInterrupt:
        if console:
            print("Closing connection.")

    except Exception as error:
        print(f"[-] Error: {error}")
