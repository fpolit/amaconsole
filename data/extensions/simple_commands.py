#!/usr/bin/env python3
#
# EXAMPLE: simple commands - amaconsole extension (commands)


import cmd2
import argparse
from time import sleep
from cmd2 import with_argparser
from datetime import datetime


@cmd2.with_default_category('External Commands (EXAMPLE)')
class SimpleCommands(cmd2.CommandSet):

    repeater_parser = argparse.ArgumentParser(
        formatter_class=argparse.ArgumentDefaultsHelpFormatter
    )

    repeater_parser.add_argument('message',
                                 help='Message to repeat')
    repeater_parser.add_argument('-n','--number',
                                 default=1,
                                 help='Number of repetitions')
    repeater_parser.add_argument('-s','--sleep',
                                 default=0.5,
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
