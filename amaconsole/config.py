#!/usr/bin/env python3

import argparse

parser = argparse.ArgumentParser(
    formatter_class=argparse.ArgumentDefaultsHelpFormatter
)
logparser = parser.add_argument_group(title='Logging options')
logparser.add_argument('--logfile', help='Location of logfile (default location: AMACONSOLE_HOME/amaconsole.log)')
logparser.add_argument('--logformat',
                       default="[%(asctime)s] %(name)s - %(levelname)s - %(message)s",
                       help='Log format')
logparser.add_argument('--loglevel',
                       default=10,
                       choices=[10, 20, 30, 40, 50],
                       type=int,
                       help='Log level')

procparser = parser.add_argument_group(title='Background processes options')
procparser.add_argument('-aP', '--max-active-processes',
                        dest='max_active_processes',
                        type=int, default=8,
                        help='Maximun active process')
procparser.add_argument('-qS', '--max-queue-size',
                        dest='max_queue_size',
                        type=int, default=100,
                        help='Maximun queue size')

cmdparser = parser.add_argument_group(title='Console options')
cmdparser.add_argument('-tF', '--tablefmt',
                       default='pretty',
                       help='Default table style')
cmdparser.add_argument('-sT', '--show-tips',
                       dest='show_tips',
                       action='store_true',
                       help='Show tips in console')
cmdparser.add_argument('-v', '--verbose',
                       action='store_true',
                       help='Verbose mode')
