#!/usr/bin/env python3
#
# Hash helper commands for ama console
#
# Status: REFACTORED - Dec 8 2021

from cmd2 import (
    Cmd,
    CommandSet,
    Cmd2ArgumentParser,
    with_default_category,
    with_argparser
)
from colorama import Style
import hashlib

from ama.commands import CommandCategory
from ama.utils.fineprint import (
    print_status,
    print_successful
)
from ama.utils import color


@with_default_category(CommandCategory.UTILITIES)
class HashHelper(CommandSet):
    """Hash helper commands for ama console"""

    hashgen_parser = Cmd2ArgumentParser()
    hashgen_parser.add_argument('text', type=str,
                                help='Plaintext')
    hashgen_parser.add_argument('-t', '--type', dest='hash_type',
                                choices=hashlib.algorithms_available,
                                required=True, metavar='HASH_FUNCTION',
                                help="Hash Type")
    hashgen_parser.add_argument('-o', '--output', default=None,
                                completer=Cmd.path_complete,
                                help='Output file')

    hashgen_parser.add_argument('-s', '--salt', help="Hash Salt")
    salt_parser = hashgen_parser.add_argument_group('Salt Position')
    salt_parser.add_argument('-i', '--init', action='store_true',
                             help="Add salt to the start")
    salt_parser.add_argument('-e', '--end', action='store_true',
                             help="Add salt to the end")


    @with_argparser(hashgen_parser)
    def do_hashgen(self, args):
        """
        Hashes Generator
        """

        print_status(f"Plaintext: {color(args.text, style=Style.BRIGHT)}")

        hash_algorithm = hashlib.new(args.hash_type)
        text = args.text
        hstruct = "$pass"

        if args.salt:
            print_status(f"Salt: {args.salt}")
            salt = args.salt

            if args.init:
                text = salt + text
                hstruct = "$salt." + hstruct

            if args.end:
                text = text + salt
                hstruct = hstruct + ".$salt"

        print_status(f"Hash struct: {args.hash_type}({hstruct})")

        hash_algorithm.update(bytes(text, 'utf-8'))

        generated_hash = hash_algorithm.hexdigest()
        print_successful(f"Hash: {color(generated_hash, style=Style.BRIGHT)}")

        if args.output:
            with open(args.output, 'w', encoding='utf-8') as output:
                output.write(f"{generated_hash}\n")

            print_status(f"Hash was saved to {args.output} file")



# === OLD =======
    # hashtype_parser = argparse.ArgumentParser()
    # hash_crackers = [cracker.MAINNAME for cracker in get_hash_crackers()]
    # hashtype_parser.add_argument('-c', '--cracker', choices=hash_crackers, required=True,
    #                            help="Hash cracker")
    # hashtype_parser.add_argument('pattern',
    #                            help="Pattern to search")

    # @with_argparser(hashtype_parser)
    # def do_hashtype(self, args):
    #     """
    #     Search by valid hashes types
    #     """
    #     search_hash(args.cracker, args.pattern)
