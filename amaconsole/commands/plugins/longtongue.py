#!/usr/bin/env python3
#
# longtongue plugin - command

from cmd2 import (
    Cmd,
    CommandSet,
    with_default_category,
    with_argparser,
    Cmd2ArgumentParser
)
from ama import LONGTONGUE_CONFIG_FILE
from ama.commands import CommandCategory
from ama.plugins.src.longtongue import get_parser
from ama.plugins import Longtongue as LongtonguePlugin

@with_default_category(CommandCategory.PLUGIN)
class Longtongue(CommandSet):
    """
    longtongue plugin - entry point
    """

    parser = get_parser()  # longtongue parser
    parser.add_argument('-q', '--quiet',
                        action='store_true',
                        help='Run quietly')
    parser.add_argument('--config',
                        default=LONGTONGUE_CONFIG_FILE,
                        help='path of config file')
    @with_argparser(parser)
    def do_longtongue(self, args):
        """Customized Password/Passphrase List inputting Target Info"""
        longtongue = LongtonguePlugin(args.config)
        if args.company:
            longtongue.target_company(args.leet,
                                      args.years,
                                      args.numbers,
                                      args.quiet)
        else:
            longtongue.target_person(args.leet,
                                     args.years,
                                     args.numbers,
                                     args.quiet)
