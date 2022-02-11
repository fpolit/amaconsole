#!/usr/bin/env python3
#
# Commands to get information about a module
#
# State: REFACTORED - Dec 12 2021

import argparse
import logging
from cmd2 import (
    CommandSet,
    with_default_category,
    with_argparser
)

from ama.modules.base import Module
from ama.commands import CommandCategory
from ama.exceptions import RankedException
from ama.utils.misc import options2table
from ama.utils.fineprint import print_failure

@with_default_category(CommandCategory.MODULE)
class ModuleInformation(CommandSet):
    """
    Commands to get information about a module
    """

    info_parser = argparse.ArgumentParser()
    info_parser.add_argument('rmid',
                             nargs='?',
                             default=None,
                             type=int,
                             help="Relative module ID")

    @with_argparser(info_parser)
    def do_info(self, args):
        """
        Provide information about selected module or active module
        """
        try:
            if self._cmd.module_manager.active_module is None and \
               args.rmid is None:
                raise RankedException("No active module and no supplied rmid",
                                      severity=logging.WARNING)

            module: Module = self._cmd.module_manager.active_module
            rmid = args.rmid
            if rmid is not None:
                mcls = self._cmd.module_manager.select(rmid)
                # add *args and **kwargs to constructor
                module = mcls()

            module.info()

        except RankedException as error:
            print_failure(error.warning)
            self._cmd.logger.exception(error)

    options_parser = argparse.ArgumentParser()
    options_parser.add_argument('rmid',
                                nargs='?',
                                default=None,
                                type=int,
                                help="module id")

    @with_argparser(options_parser)
    def do_options(self, args):
        """
        Show options of selected module or active module
        """

        try:
            if self._cmd.module_manager.active_module is None and \
               args.rmid is None:
                raise RankedException("No active module and no supplied rmid",
                                      severity=logging.WARNING)

            module: Module = self._cmd.module_manager.active_module
            rmid = args.rmid
            if rmid is not None:
                mcls = self._cmd.module_manager.select(rmid)
                # add *args and **kwargs to constructor
                module = mcls()

            options2table(module.options)

        except RankedException as error:
            print_failure(error.warning)
            self._cmd.logger.exception(error)
