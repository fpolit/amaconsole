#!/usr/bin/env python3
#
# Commands to interact with modules
#
# State: REFACTORED - Dec 8 2021

import logging
import datetime
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
from pathlib import Path

from ama import AMA_PROMPT
from ama.commands import CommandCategory
#from ama.utils import color
from ama.utils.misc import gvalues2table
from ama.utils.fineprint import print_failure
from ama.exceptions import RankedException
from ama.utils.question import Question

@with_default_category(CommandCategory.MODULE)
class ModuleInteraction(CommandSet):
    """
    Commands to interact with modules
    """

    gvalues_parser = Cmd2ArgumentParser()
    gvalues_subparser = gvalues_parser.add_subparsers(
        title='operation',
        help='Operation to perform'
    )

    @with_argparser(gvalues_parser)
    def do_gvalues(self, ns: argparse.Namespace):
        """
        Command to manipulate global variables
        """
        handler = ns.cmd2_handler.get()
        if handler is not None:
            handler(ns)
        else:  # show gvalues in a table
            gvalues = self._cmd.module_manager.gvalues
            gvalues2table(gvalues)

    gvalues_set_parser = Cmd2ArgumentParser()
    gvalues_set_parser.add_argument('variable',
                                    help='global variable to set')
    gvalues_set_parser.add_argument('value', nargs='+',
                                    completer=Cmd.path_complete,
                                    help='value of global variable')

    @cmd2.as_subcommand_to('gvalues', 'set', gvalues_set_parser)
    def gvalues_set(self, args):
        """
        Set a global variable
        """
        self._cmd.module_manager.add_global_value(args.variable, args.value)

    gvalues_rm_parser = Cmd2ArgumentParser()
    gvalues_rm_parser.add_argument('variable',
                                   nargs='?',
                                   default=None,
                                   help='global variable to remove')
    gvalues_rm_parser.add_argument('-a', '--all',
                                   dest='all_variables',
                                   action='store_true',
                                   help='remove all global variables')

    @cmd2.as_subcommand_to('gvalues', 'rm', gvalues_rm_parser)
    def gvalues_rm(self, args):
        """
        Remove a global variable
        """
        if args.variable:
            self._cmd.module_manager.remove_global_value(args.variable)

        if args.all_variables:
            delete = Question.short_anwser(
                "Do you really want to delete"
                " all your global variables?[y/n] ")
            if delete:
                self._cmd.module_manager.gvalues = {}


    bkp_parser = Cmd2ArgumentParser()
    bkp_parser.add_argument('backup', completer=Cmd.path_complete,
                            help="Backup file")
    bkp_parser.add_argument('--load', action='store_true',
                            help="Restore backup file")

    @with_argparser(bkp_parser)
    def do_bkp(self, args):
        """
        Command to manipulate backup of active module
        """
        backup_file = Path(args.backup)
        if args.load:
            self._cmd.module_manager.load_backup(backup_file)
        else:
            active_module = self._cmd.module_manager.active_module
            self._cmd.module_manager.backup(active_module, backup_file)

    use_parser = argparse.ArgumentParser()
    use_parser.add_argument(
        'module',
        help="relative module id or module name")
    # use_parser.add_argument(
    #     '--args', nargs='*',
    #     dest='margs', default=[],
    #     help="arguments to initialize the module"
    # )
    use_parser.add_argument(
        '--kwargs', nargs='*', dest='mkwargs',
        default=[], metavar='KEY:VALUE',
        help="positional arguments to initialize the module"
    )

    @with_argparser(use_parser)
    def do_use(self, args):
        """
        Select a module from filtered modules
        """

        try:
            mkwargs = {}
            for pair in args.mkwargs:
                key, value = pair.split(':')
                mkwargs[key] = value

            active_module = self._cmd.module_manager.use(args.module,
                                                         **mkwargs)
            self._cmd.prompt = active_module.prompt

        except RankedException as error:
            print_failure(error.warning)
            self._cmd.logger.exception(error)

    unset_parser = argparse.ArgumentParser()
    unset_parser.add_argument('option', help='module option')

    @with_argparser(unset_parser)
    def do_unset(self, args):
        """
        Unset the value of a module option
        """

        if module := self._cmd.module_manager.active_module:
            module.setv(args.option, None)
        else:
            print_failure("There is no active module")

    setv_parser = Cmd2ArgumentParser()
    setv_parser.add_argument("option", help="module option")

    setv_parser.add_argument("value", nargs='+',
                             completer=Cmd.path_complete,
                             help="option value")

    @with_argparser(setv_parser)
    def do_setv(self, args):
        """
        Set an option
        """

        if module := self._cmd.module_manager.active_module:
            module.setv(args.option, args.value)
        else:
            print_failure("There is no active module")

    setvg_parser = Cmd2ArgumentParser()
    setvg_parser.add_argument("option", help="module option")

    setvg_parser.add_argument("value", nargs='+',
                              completer=Cmd.path_complete,
                              help="option value")

    @with_argparser(setvg_parser)
    def do_setvg(self, args):
        """
        Set an option globally
        """

        if module := self._cmd.module_manager.active_module:
            self._cmd.module_manager.add_global_value(args.option, args.value)
            module.setv(args.option, args.value)
        else:
            print_failure("There is no active module")

    back_parser = Cmd2ArgumentParser()
    back_parser.add_argument('-m', '--module', action='store_true',
                             help='Back to previous module')

    @with_argparser(back_parser)
    def do_back(self, args):
        """
        Close interaction with active module or switch to previous module
        """
        try:
            if args.module:
                active_module = self._cmd.module_manager.back()
                self._cmd.prompt = active_module.prompt
            else:
                self._cmd.module_manager.close()
                self._cmd.prompt = AMA_PROMPT

        except RankedException as error:
            print_failure(error.warning)
            self._cmd.exception(error)

    module_execute_parser = Cmd2ArgumentParser()
    module_execute_parser.add_argument(
        '-i', '--interactive',
        action='store_true',
        help='Execute active module interactively (main thread)'
    )

    module_submit_parser = module_execute_parser.add_argument_group(
        'Submit Options',
        description='Submit a module to execute it background'
    )
    module_submit_parser.add_argument(
        '-p', '--priority',
        type=int,
        default=0,
        help='Execution priority (MAX: -20 -> MIN: 20)'
    )
    module_submit_parser.add_argument(
        '-o', '--output',
        completer=Cmd.path_complete,
        default='ama-%j.out',
        help='Ouput File'
    )
    module_submit_parser.add_argument(
        '-dp', '--dependency-processes',
        dest='depends',
        nargs='*',
        default=[],
        help='dependency processes'
    )

    module_execution_delay = module_execute_parser.add_argument_group(
            'Delay Time',
            description='Delay time to initialize execution'
    )
    module_execution_delay.add_argument('-m', '--minutes',
                                        type=int,
                                        default=0,
                                        help='delay minutes')
    module_execution_delay.add_argument('-s', '--seconds',
                                        type=int,
                                        default=0,
                                        help='delay seconds')
    module_execution_delay.add_argument('-hr', '--hours',
                                        type=int,
                                        default=0,
                                        help='delay hours')
    module_execution_delay.add_argument('-d', '--days',
                                        type=int,
                                        default=0,
                                        help='delay days')
    module_execution_delay.add_argument('-w', '--weeks',
                                        type=int,
                                        default=0,
                                        help='delay weeks')

    @with_argparser(module_execute_parser)
    def do_execute(self, args):
        """
        Submit to scheduler or execute interactively the active module
        """
        try:
            module = self._cmd.module_manager.active_module
            if module is None:
                raise RankedException("There is no active module",
                                      severity=logging.WARNING)

            if not args.interactive:
                delay = datetime.timedelta(
                    days=args.days,
                    seconds=args.seconds,
                    minutes=args.minutes,
                    hours=args.hours,
                    weeks=args.weeks
                )

                self._cmd.module_manager.submit(
                    module,
                    output=args.output,
                    priority=args.priority,
                    depends=args.depends,
                    delay=delay
                )
                if config := self._cmd.config:
                    scheduler = self._cmd.module_manager.scheduler
                    config['PROCESS_COUNT'] = scheduler.SUBMITTED_PROCESS

            else:
                # ADD *args and **kwargs arguments to execute method
                module.execute()

        except RankedException as error:
            print_failure(error)
            self._cmd.logger.exception(error)
