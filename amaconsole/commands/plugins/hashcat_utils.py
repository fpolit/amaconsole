#!/usr/bin/env python3
#
# hashcat utils plugin - commands

import logging
from cmd2 import (
    Cmd,
    CommandSet,
    with_default_category,
    with_argparser,
    Cmd2ArgumentParser
)

from ama.commands import CommandCategory
from ama.exceptions import RankedException
from ama.utils.fineprint import print_failure

from _hcutils import (
    combinator,
    combinator3,
    combipow,
    #splitlen
)


@with_default_category(CommandCategory.HCUTILS)
class HCUtils(CommandSet):
    """
    hashcat utilities plugin
    """

    combinator_parser = Cmd2ArgumentParser(description="Combinator - Hashcat utils")
    combinator_parser.add_argument('wordlists',
                                   nargs='+',
                                   completer=Cmd.path_complete,
                                   help='wordlists to combinate')
    combinator_parser.add_argument('-o', '--output',
                                   required=True,
                                   completer=Cmd.path_complete,
                                   help='output file')

    @with_argparser(combinator_parser)
    def do_combinator(self, args):
        try:
            nwl: int = len(args.wordlists)
            if nwl < 2:
                raise RankedException(
                    "At least 2 wordlists are needed to combine",
                    severity=logging.INFO)

            retv: int = 0 # return value

            if nwl == 2:
                wl1, wl2 = args.wordlists
                retv = combinator(wl1, wl2, args.output)

            elif nwl == 3:
                wl1, wl2, wl3 = args.wordlists
                retv = combinator3(wl1, wl2, wl3, args.output)
            else:
                raise RankedException(
                    "combinatorx has not been implemented yet",
                    severity=logging.INFO)

            if retv != 0:
                raise RankedException(
                    "Some error has been occurred while combining wordlists",
                    severity=logging.ERROR)

        except RankedException as error:
            print_failure(error.warning)


    combipow_parser = Cmd2ArgumentParser(description="Combipow - Hashcat utils")
    combipow_parser.add_argument('wordlist',
                                 completer=Cmd.path_complete,
                                 help='wordlist to produce combinations')
    combipow_parser.add_argument('-o', '--output',
                                 required=True,
                                 completer=Cmd.path_complete,
                                 help='output file')

    @with_argparser(combipow_parser)
    def do_combipow(self, args):
        try:
            retv: int = 0
            retv = combipow(args.wordlist, args.output)

            if retv != 0:
                raise RankedException(
                    "Some error has been occurred while combining wordlist",
                    severity=logging.ERROR)

        except RankedException as error:
            print_failure(error.warning)


    # splitlen_parser = Cmd2ArgumentParser(description="Splitlen - Hashcat utils")
    # splitlen_parser.add_argument('wordlist',
    #                              completer=Cmd.path_complete,
    #                              help='wordlist to split by len')
    # splitlen_parser.add_argument('-o', '--outdir',
    #                              required=True,
    #                              completer=Cmd.path_complete,
    #                              help='output directory')

    # @with_argparser(splitlen_parser)
    # def do_splitlen(self, args):
    #     try:
    #         retv: int = 0
    #         retv = splitlen(args.wordlist, args.outdir)

    #         if retv != 0:
    #             raise RankedException(
    #                 "Some error has been occurred while splitting by length",
    #                 severity=logging.ERROR)

    #     except RankedException as error:
    #         print_failure(error.warning)
