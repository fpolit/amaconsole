#!/usr/bin/env python3
#
# Commands to interact with sessions
#
# State: REFACTORED - Dec 12 2021

import datetime
import logging
import argparse
from typing import Optional, List
from colorama import Style
import cmd2
from cmd2 import (
    Cmd,
    CommandSet,
    Cmd2ArgumentParser,
    with_default_category,
    with_argparser
)
from ama import AMA_PROMPT, PRETTY_STYLE, GRID_STYLE
from ama.commands import CommandCategory as Category

from ama.manager.session import SessionModule, Session, SessionType
from ama.modules import Module
from ama.utils.misc import sessions2table
from ama.utils.fineprint import (
    print_failure,
    print_status
)
from ama.exceptions import RankedException
from ama.utils import color

@with_default_category(Category.SESSION)
class SessionInteraction(CommandSet):
    """
    Commands to interact with sessions
    """
    session_parser = Cmd2ArgumentParser()
    session_subparser = session_parser.add_subparsers(
        title='operation',
        help='Operation to perform'
    )

    @with_argparser(session_parser)
    def do_session(self, ns: argparse.Namespace):
        """
        Command to manipulate sessions
        """
        handler = ns.cmd2_handler.get()
        if handler is not None:
            handler(ns)
        else:
            self.do_help('session')


    session_create_parser = Cmd2ArgumentParser()
    session_create_parser.add_argument('--name', default=None,
                                       help='session name')
    session_create_parser.add_argument('-m', '--main-module',
                                       dest='module',
                                       type=int, default=None,
                                       help='session main module')
    session_create_parser.add_argument('-f', '--fullattack',
                                       type=int, default=None,
                                       help='fullattack id')
    session_create_parser.add_argument('-s', '--subsession',
                                       choices=[stype
                                                for stype in SessionType.__members__],
                                       default=None,
                                       help='create subsession of active session')

    session_create_parser.add_argument('-n', '--no-interact',
                                       dest='no_interact',
                                       action='store_true',
                                       help='no interact with created session')

    @cmd2.as_subcommand_to('session', 'create', session_create_parser)
    def session_create(self, args):
        """
        Create a new session
        """

        try:
            if self._cmd.module_manager.active_module is None \
               and args.module is None \
               and args.fullattack is None:
                raise RankedException(
                    "No active module or main module or fullattack was supplied",
                    severity=logging.ERROR)

            session: Session

            if rfid := args.fullattack:
                fullattack = self._cmd.session_manager.get_fullattack(rfid)
                session = self._cmd.session_manager.create_session_with_fullattack(
                    fullattack,
                    interact=False
                )

            else:
                main_module: Module = self._cmd.module_manager.active_module
                if args.module != -1:
                    main_module = self._cmd.module_manager.use(args.module,
                                                           interact=False)

                    session = self._cmd.session_manager.create_session(main_module,
                                                                       name=args.name,
                                                                       interact=False)

            if args.subsession:
                active_session = self._cmd.session_manager.active_session
                if active_session is None:
                    raise RankedException(
                        f"No active session to set session {session.uuid} as {args.subsession}",
                        severity=logging.WARNING
                    )

                stype: SessionType
                for name, value in SessionType.__members__.items():
                    if name == args.subsession:
                        stype = value
                        break

                active_session.set_subsession(session, stype)

            if not args.no_interact:
                self._cmd.session_manager.interact(session)
                self._cmd.prompt = session.prompt

        except RankedException as error:
            print_failure(error.warning)
            self._cmd.logger.exception(error)

    session_find_parser = Cmd2ArgumentParser()
    session_find_parser.add_argument('--name',
                                     help='name pattern')
    session_find_parser.add_argument('--with-modules',
                                     nargs='*',
                                     choices=[name
                                              for name in SessionModule.__members__],
                                     help='session with modules')
    session_find_parser.add_argument('--with-sessions',
                                     nargs='*',
                                     choices=[name
                                              for name in SessionType.__members__],
                                     help='session with subsessions')

    @cmd2.as_subcommand_to('session', 'find', session_find_parser)
    def session_find(self, _):
        """
        Show sessions
        """
        sessions: List[Session] = self._cmd.session_manager.sessions

        filtered_session: List[Session] = []
        print_status("Filtering session (IMPLEMENT ME)")
        # some stuff
        sessions2table(filtered_session, tablefmt=GRID_STYLE)



    session_ls_parser = Cmd2ArgumentParser()

    @cmd2.as_subcommand_to('session', 'ls', session_ls_parser)
    def session_ls(self, _):
        """
        Show sessions
        """
        sessions = self._cmd.session_manager.sessions
        sessions2table(sessions, tablefmt=GRID_STYLE)

    session_interact_parser = Cmd2ArgumentParser()
    interaction = session_interact_parser.add_mutually_exclusive_group(required=True)
    interaction.add_argument('session',
                             nargs='?',
                             help='session uuid')
    interaction.add_argument('-p', '--parent',
                             action='store_true',
                             help='switch interaction with parent session')
    interaction.add_argument('-t', '--type',
                             dest='stype',
                             choices=[stype
                                      for stype in SessionType.__members__],
                             default=None,
                             help='switch interaction with subsession')

    @cmd2.as_subcommand_to('session', 'interact', session_interact_parser)
    def session_interact(self, args):
        """
        Initialize interaction with session
        """

        try:
            session: Session # active session after switch
            if args.session:
                session = self._cmd.session_manager.interact_session(args.session)

            elif args.parent or args.stype:
                active_session: Optional[Session] = self._cmd.session_manager.active_session
                if active_session is None:
                    raise RankedException("There is no active session",
                                          severity=logging.WARNING)
                if args.parent:
                    if active_session.parent_session is None:
                        raise RankedException(
                            f"Session {active_session.uuid} has not parent session",
                            severity=logging.WARNING)
                    session = active_session.parent_session
                    self._cmd.session_manager.interact(session)

                else: # session type was supplied
                    stype: SessionType
                    for name, value in SessionModule.__members__.items():
                        if name == args.stype:
                            stype = value
                            break

                    session: Optional[Session] = active_session.get_subsession(stype)
                    if session is None:
                        raise RankedException(
                            f"Session {active_session.uuid} has not {stype} subsession",
                            severity=logging.WARNING
                        )

                    self._cmd.session_manager.interact(session)

            self._cmd.prompt = session.prompt

        except RankedException as error:
            print_failure(error.warning)
            self._cmd.logger.warning(error.warning)

    session_module_parser = Cmd2ArgumentParser()
    session_module_parser.add_argument(
        'smtype',
        choices=[name
                 for name in SessionModule.__members__],
        help='Session module type'
    )

    session_module_use = session_module_parser.add_argument_group(
        title='Module selector',
        description='Select modules of active session'
    )

    session_module_use.add_argument(
        '--use',
        type=int,
        default=None,
        metavar='rmid',
        help='relative module id'
    )
    session_module_use.add_argument(
        '-i', '--interact',
        action='store_true',
        help='interact with selected module'
    )

    @cmd2.as_subcommand_to('session', 'module', session_module_parser)
    def session_module(self, args):
        """
        Select session' modules and switch interaction between session's modules
        """

        try:
            if self._cmd.session_manager.active_session is None:
                raise RankedException("No active session",
                                      severity=logging.WARNING)

            smtype: SessionModule
            for name, value in SessionModule.__members__.items():
                if name == args.smtype:
                    smtype = value
                    break

            if rmid := args.use:
                self._cmd.session_manager.use(rmid, smtype)
                active_session = self._cmd.session_manager.active_session
                module: Module = active_session.active_module
                print_status(
                    f"Initialized {color(smtype.name, style=Style.BRIGHT)}"
                    f" with {color(module.mname, style=Style.BRIGHT)}"
                )

            if args.interact:
                self._cmd.session_manager.interact_module(smtype)
                active_session = self._cmd.session_manager.active_session
                self._cmd.prompt = active_session.prompt

        except RankedException as error:
            print_failure(error.warning)
            self._cmd.logger.warning(error.warning)

    session_info_parser = Cmd2ArgumentParser()
    session_info_parser.add_argument('session',
                                     nargs='?',
                                     default=None,
                                     help='Session uuid')

    @cmd2.as_subcommand_to('session', 'info', session_info_parser)
    def session_info(self, args):
        """
        Show information of active session or selected session
        """

        try:

            if self._cmd.session_manager.active_session is None and\
               args.session is None:
                raise RankedException(
                    "No active session and no session uuid supplied",
                    severity=logging.WARNING
                )

            session = self._cmd.session_manager.active_session
            if suuid := args.session:
                session = self._cmd.session_manager.search_session(suuid)

            suuid = session.uuid
            print_status(f"Session id: {suuid}")

            if name := session.name:
                print_status(f"Session name: {name}")

            if session.parent_session:
                print_status(f"Parent session: {session.parent_session.uuid}")

            if session.pre_session:
                print_status(f"Pre session: {session.pre_session.uuid}")

            if session.post_session:
                print_status(f"Post session: {session.post_session.uuid}")

            date = session.creation_date
            print_status(f"Creation date: {date}")
            sessions2table([session], tablefmt=PRETTY_STYLE)

        except RankedException as error:
            self._cmd.logger.warning(error.warning)
            print_failure(error.warning)

    session_submit_parser = Cmd2ArgumentParser()
    session_submit_parser.add_argument('suuid',
                                       nargs='?',
                                       default='',
                                       help='Session uuid')
    session_submit_parser.add_argument(
        '-p', '--priority',
        type=int,
        default=0,
        help='Execution priority (MAX: -20 -> MIN: 20)'
    )

    session_execution_delay = session_submit_parser.add_argument_group(
        'Delay Time',
        description='Delay time to initialize session execution'
    )
    session_execution_delay.add_argument('-m', '--minutes',
                                         type=int,
                                         default=0,
                                         help='delay minutes')
    session_execution_delay.add_argument('-s', '--seconds',
                                         type=int,
                                         default=0,
                                         help='delay seconds')
    session_execution_delay.add_argument('-hr', '--hours',
                                         type=int,
                                         default=0,
                                         help='delay hours')
    session_execution_delay.add_argument('-d', '--days',
                                         type=int,
                                         default=0,
                                         help='delay days')
    session_execution_delay.add_argument('-w', '--weeks',
                                         type=int,
                                         default=0,
                                         help='delay weeks')

    @cmd2.as_subcommand_to('session', 'submit', session_submit_parser)
    def session_submit(self, args):
        """
        Submit active session or selected session
        """
        try:
            if self._cmd.session_manager.active_session is None and\
               not args.suuid:
                raise RankedException(
                    "No active session and no session uuid was supplied",
                    severity=logging.WARNING)

            delay = datetime.timedelta(
                days=args.days,
                seconds=args.seconds,
                minutes=args.minutes,
                hours=args.hours,
                weeks=args.weeks
            )
            session = self._cmd.session_manager.active_session
            if args.suuid:
                session = self._cmd.session_manager.search_session(args.suuid)

            self._cmd.session_manager.submit(
                session,
                priority=args.priority,
                delay=delay
            )

        except RankedException as error:
            print_failure(error.warning)
            self._cmd.logger.warning(error)

    session_close_parser = Cmd2ArgumentParser()

    @cmd2.as_subcommand_to('session', 'close', session_close_parser)
    def session_close(self, _):
        """
        Close interaction with active session
        """
        try:
            self._cmd.session_manager.close()

        except RankedException as error:
            print_failure(error.warning)
            self._cmd.logger(error.warning,
                             severity=logging.WARNING)

        finally:
            self._cmd.prompt = AMA_PROMPT
