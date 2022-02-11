#!/usr/bin/env python3
#
# something (john2hash or hashcat2hash) to hash commands

from cmd2 import (
    Cmd,
    CommandSet,
    with_default_category,
    with_argparser,
    Cmd2ArgumentParser
)

from ama.commands.category import CommandCategory

from ama.utils.tohash.ssh2john import read_private_key

@with_default_category(CommandCategory.TOHASH)
class ToHash(CommandSet):
    """
    Something to hash
    """

    ssh2hash_parser = Cmd2ArgumentParser()
    ssh2hash_parser.add_argument('pks',
                                 nargs='+',
                                 completer=Cmd.path_complete,
                                 help='SSH private key(s)')

    @with_argparser(ssh2hash_parser)
    def do_ssh2hash(self, args):
        """SSH private key to hash"""

        for ssh_pk in args.pks:
            read_private_key(ssh_pk)
