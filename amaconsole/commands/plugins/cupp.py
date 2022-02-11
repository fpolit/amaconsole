#!/usr/bin/env python3
#
# cupp plugin - command

from cmd2 import (
    Cmd,
    CommandSet,
    with_default_category,
    with_argparser,
    Cmd2ArgumentParser
)
from ama import CUPP_CONFIG_FILE
from ama.commands import CommandCategory
from ama.plugins import Cupp as CuppPlugin


@with_default_category(CommandCategory.PLUGIN)
class Cupp(CommandSet):
    """
    cupp plugin - entry point
    """

    parser = Cmd2ArgumentParser(description="Common User Passwords Profiler")
    group = parser.add_mutually_exclusive_group(required=False)
    group.add_argument(
        "-i",
        "--interactive",
        action="store_true",
        help="Interactive questions for user password profiling",
    )
    group.add_argument(
        "-w",
        dest="improve",
        metavar="FILENAME",
        help="Use this option to improve existing dictionary,"
        " or WyD.pl output to make some pwnsauce",
        completer=Cmd.path_complete
    )
    group.add_argument(
        "-l",
        dest="download_wordlist",
        action="store_true",
        help="Download huge wordlists from repository",
    )
    group.add_argument(
        "-a",
        dest="alecto",
        action="store_true",
        help="Parse default usernames and passwords directly"
        " from Alecto DB. Project Alecto uses purified"
        " databases of Phenoelit and CIRT which were merged"
        " and enhanced",
    )
    group.add_argument(
        "-v", "--version", action="store_true", help="Show the version of this program."
    )
    parser.add_argument(
        "-q", "--quiet", action="store_true", help="Quiet mode (don't print banner)"
    )

    @with_argparser(parser)
    def do_cupp(self, args):
        cupp_plugin = CuppPlugin(CUPP_CONFIG_FILE)

        if not args.quiet:
            cupp_plugin.print_cow()

        if args.version:
            print(cupp_plugin.version)

        elif args.interactive:
            cupp_plugin.interactive()

        elif args.download_wordlist:
            cupp_plugin.download_wordlist()

        elif args.alecto:
            cupp_plugin.alectodb_download()

        elif args.improve:
            cupp_plugin.improve_dictionary(args.improve)
