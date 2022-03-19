#!/usr/bin/env python

import argparse
import io
import os
import sys
from cmd2 import (
    Cmd,
    CommandSet,
    Cmd2ArgumentParser,
    with_default_category,
    with_argparser
)

from amaconsole.commands import CommandCategory
from amaconsole.plugins.hashID import (
    HashID ,
    writeResult,
     __author__,
    __version__,
    __github__,
    __license__,
    __banner__
)


@with_default_category(CommandCategory.UTILITIES)
class HashIDCommands(CommandSet):
    """HashID Commands"""

    usage = "{0} [-h] [-e] [-m] [-j] [-o FILE] [--version] INPUT".format(os.path.basename(__file__))

    hashid_parser = Cmd2ArgumentParser()
    parser = argparse.ArgumentParser(
        description="Identify the different types of hashes used to encrypt data",
        usage=usage,
        epilog=__license__,
        add_help=False,
        formatter_class=lambda prog: argparse.HelpFormatter(prog, max_help_position=27)
    )
    parser.add_argument("strings",
                        metavar="INPUT", type=str, nargs="*",
                        help="input to analyze (default: STDIN)")
    group = parser.add_argument_group('options')
    group.add_argument("-e", "--extended",
                       action="store_true",
                       help="list all possible hash algorithms including salted passwords")
    group.add_argument("-m", "--mode",
                       action="store_true",
                       help="show corresponding Hashcat mode in output")
    group.add_argument("-j", "--john",
                       action="store_true",
                       help="show corresponding JohnTheRipper format in output")
    group.add_argument("-o", "--outfile",
                       metavar="FILE", type=str,
                       help="write output to file")
    group.add_argument("-h", "--help",
                       action="help",
                       help="show this help message and exit")
    group.add_argument("--version",
                       action="version",
                       version=__banner__)

    def do_hashid(self, args):
        hashID = HashID()

        if not args.outfile:
            outfile = sys.stdout
        else:
            try:
                outfile = io.open(args.outfile, "w", encoding="utf-8")
            except EnvironmentError:
                parser.error("Could not open {0}".format(args.output))

        if not args.strings or args.strings[0] == "-":
            while True:
                line = sys.stdin.readline()
                if not line:
                    break
                outfile.write(u"Analyzing '{0}'\n".format(line.strip()))
                writeResult(hashID.identifyHash(line), outfile, args.mode, args.john, args.extended)
                sys.stdout.flush()
        else:
            for string in args.strings:
                if os.path.isfile(string):
                    try:
                        with io.open(string, "r", encoding="utf-8") as infile:
                            outfile.write("--File '{0}'--\n".format(string))
                            for line in infile:
                                if line.strip():
                                    outfile.write(u"Analyzing '{0}'\n".format(line.strip()))
                                    writeResult(hashID.identifyHash(line), outfile, args.mode, args.john, args.extended)
                    except (EnvironmentError, UnicodeDecodeError):
                        outfile.write("--File '{0}' - could not open--".format(string))
                    else:
                        outfile.write("--End of file '{0}'--".format(string))
                else:
                    outfile.write(u"Analyzing '{0}'\n".format(string.strip()))
                    writeResult(hashID.identifyHash(string), outfile, args.mode, args.john, args.extended)
