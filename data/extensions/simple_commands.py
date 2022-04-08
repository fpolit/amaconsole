#!/usr/bin/env python3
#
# EXAMPLE: simple commands - amaconsole extension (commands)


import cmd2
import argparse
import pyfiglet
from time import sleep
from cmd2 import with_argparser
from datetime import datetime
from tabulate import tabulate


@cmd2.with_default_category('External Commands (EXAMPLE)')
class SimpleCommands(cmd2.CommandSet):

    repeater_parser = argparse.ArgumentParser(
        formatter_class=argparse.ArgumentDefaultsHelpFormatter
    )

    repeater_parser.add_argument('message',
                                 help='Message to repeat')
    repeater_parser.add_argument('-n','--number',
                                 default=1,
                                 type=int,
                                 help='Number of repetitions')
    repeater_parser.add_argument('-s','--sleep',
                                 default=0.5,
                                 type=float,
                                 help='Number of second to sleep between repetitions')

    @with_argparser(repeater_parser)
    def do_repeater(self, args):
        repetitions = args.number if args.number > 0 else 1
        count = 0
        while count < repetitions:
            now = datetime.now()
            self._cmd.poutput(f"[{now}] {args.message}")
            sleep(args.sleep)
            count += 1

    asciigen_parser = argparse.ArgumentParser(
        formatter_class=argparse.ArgumentDefaultsHelpFormatter
    )

    asciigen_parser.add_argument('-f', '--font',
                                 default='shadow',
                                 help='Letter font')
    action_parser = asciigen_parser.add_mutually_exclusive_group(required=True)
    action_parser.add_argument('-m','--message',
                               help='Message to generate ascci')
    action_parser.add_argument('-l', '--list-fonts',
                               dest='list_fonts',
                               action='store_true',
                               help='List availables fonts')

    @with_argparser(asciigen_parser)
    def do_asciigen(self, args):
        if args.list_fonts:
            print(pyfiglet.Figlet().getFonts())
        else:
            font =  pyfiglet.Figlet(font=args.font)
            self._cmd.poutput(font.renderText(args.message))
