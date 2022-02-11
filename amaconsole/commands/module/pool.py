#!/usr/bin/env python3
#
# Commands to load dynamically modules

#import logging
#import datetime
import argparse
import cmd2
from cmd2 import (
    Cmd,
    CommandSet,
    with_default_category,
    with_argparser,
    Cmd2ArgumentParser
)
#from colorama import Fore
#from pathlib import Path

#from ama import AMA_PROMPT
from ama.commands import CommandCategory
#from ama.utils import color
#from ama.utils.misc import gvalues2table
#from ama.utils.fineprint import print_failure
#from ama.exceptions.utils.modules import NoPreviousModule
#from ama.exceptions import RankedException
#from ama.utils.question import Question

@with_default_category(CommandCategory.MODULE)
class ModuleLoader(CommandSet):
    """
    Commands to load dynamically modules
    """
    load_parser = Cmd2ArgumentParser()
    load_parser.add_argument('sdir',
                             help='search directory')
    load_parser.add_argument('-r', '--recursive',
                             action='store_true',
                             help='recursive search')
    @with_argparser(load_parser)
    def do_load(self, args):
        """
        Load custom modules
        """
        pass
