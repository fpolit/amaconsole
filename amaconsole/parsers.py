#!/usr/bin/env python3

import argparse

parser = argparse.ArgumentParser(
    formatter_class=argparse.ArgumentDefaultsHelpFormatter
)

bgprocparser = parser.add_argument_group(title='Background processes options')
bgprocparser.add_argument('-aP', '--max-active-processes',
                          dest='max_active_processes',
                          type=int, default=8,
                          help='Maximun active process')
bgprocparser.add_argument('-qS', '--max-queue-size',
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

resmanparser = parser.add_argument_group(title='Resource manager options')
resmanparser.add_argument('-rP','--resman-port',
                          default=1318,
                          dest='resman_port',
                          help='Resource manager port')

ctrlparser = parser.add_argument_group(title='Controller options')
ctrlparser.add_argument('-cP','--controller-port',
                        default=1317,
                        dest='controller_port',
                        help='Amacontroller port')

dbparser = parser.add_argument_group(title='Database options')
dbparser.add_argument('-dP','--amadb-port',
                      default=1319,
                      dest='amadb_port',
                      help='AmaDB port')
