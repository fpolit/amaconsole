
#!/usr/bin/env python3
#
# ama console

import os
import json
import argparse
import logging
from cmd2 import Cmd
from pathlib import Path
from threading import Thread
from typing import Dict, Any
from configparser import ConfigParser

from amaconsole import PROMPT
from amaconsole.commands import CommandCategory
from amaconsole.banner import BannerGenerator
from amaconsole.processor import BGProcessor
from amaconsole.utils import Logger
from amaconsole.extensions import load_extensions

# commands
from amaconsole.commands.bgprocess import BGProcessCmds
from amaconsole.commands.console import ExtensionsCommands


class AmaConsole(Cmd):
    """
    Console to interact with Ama-Framework
    """

    def __init__(self,
                 config_args: argparse.Namespace = None,
                 config_file: str = None,
                 **kwargs):
        self.config: ConfigParser = ConfigParser()
        self.connection_args = {}
        self.init_config(config_args, config_file)

        super().__init__(allow_redirection=True,
                         persistent_history_file=HISTORY_FILE, **kwargs)

        self.default_to_shell = True
        self.debug = True
        self.intro = None
        self.prompt = PROMPT
        self.continuation_prompt = "> "
        self.default_category = CommandCategory.CONSOLE
        self.channel = None
        self.extensions: Dict[str, cmd2.CommandSet] = {}

        self.logger = None
        self.banner_generator: BannerGenerator = None

        self.bg_processor: BGProcessor = None

        # preloop hooks
        self.register_preloop_hook(self.init_logger)
        # self.register_preloop_hook(self.init_amacontroller_connection)
        self.register_preloop_hook(self.init_custom_extensions)
        self.register_preloop_hook(self.init_background_processor)
        self.register_preloop_hook(self.init_banner_generator)

        # postloop hooks

    def init_background_processor(self) -> None:
        self.bg_processor = BGProcessor(
            logfile=self.config['LOGGING']['LOGFILE'],
            max_active_processes=self.config['PROCESSES']['MAX_ACTIVE_PROCESSES'],
            logformat=self.config['LOGGING']['LOGFORMAT'],
            loglevel=logging.DEBUG
        )

        # start processor thread
        self.bg_processor_thread = Thread(
            target=self.bg_processor.processor,
            name='process-processor',
            daemon=True)

        self.bg_processor_thread.start()

    def init_custom_extensions(self) -> None:
        sdir: List[Path] = []

        if amaconsole_extensions := self.config['DEFAULT']['AMACONSOLE_EXTENSIONS']:
            sdir.append(amaconsole_extensions)

        if include_dir := self.config['INCLUDE_DIR']:
            sdir.append(include_dir)

        for basedir in sdir:
            extensions = load_extensions(basedir, self.config['CONSOLE']['VERBOSE'])
            for ext in extensions:
                self.register_extension(ext)

    def register_extension(self, ext: cmd2.CommandSet, verbose: bool = False):
        extname = ext.__name__
        if verbose:
            self.poutput(f"Registering {extname} extension")
        self.extensions[extname] = ext()
        self.register_command_set(self.extensions[extname])

    def unregister_extension(self, extname: str, verbose: bool = False):
        ext = self.extensions.get(extname, None)
        if ext:
            if verbose:
                self.poutput(f"Unregistering {extname} extension")
            self.unregister_extension(ext)
            del self.extensions[extname]
        else:
            if verbose:
                self.poutput(f"Extension {extname} doesn't exist")

    def init_config(self,
                    config_args: argparse.Namespace,
                    config_file: str = None) -> None:
        """
        Override configurations of config_file (dafault configurations) with supplied config_args
        """
        pass
    #     try:
    #         if not config_file:
    #             # check if AMACONSOLE_CONFIGFILE variable was configured
    #             config_file = os.getenv('AMACONSOLE_CONFIGFILE')
    #             if not os.path.isfile(config_file):
    #                     config_file=None

    #             # check config file in home directory
    #             if not config_file:
    #                 config_file = os.path.join(os.environ['HOME'],
    #                                            '.amaconsole/amaconsole.cfg')
    #                 if not os.path.isfile(config_file):
    #                     config_file=None

    #         if config_file:
    #             self.config.read(config_file)

    #         # DEFAULT section
    #         #if config_file
    #         if controller_port := config_args.controller_port:
    #             self.config['DEFAULT']['CONTROLLER_PORT'] = controller_port

    #         if controller_data_port := config_args.controller_data_port:
    #             self.config['DEFAULT']['CONTROLLER_DATA_PORT'] = controller_data_port

    #         # LOGING section
    #         if logfile := config_args.logfile:
    #             self.config['LOGGING']['LOGFILE'] = logfile

    #         if logformat := config_args.logformat:
    #             self.config['LOGGING']['LOGFORMAT'] = logformat

    #         if loglevel := config_args.loglevel:
    #             self.config['LOGGING']['LOGLEVEL'] = loglevel

    #         # PROCESSES section
    #         if max_active_processes := config_args.max_active_processes:
    #             self.config['PROCESSES']['MAX_ACTIVE_PROCESSES'] = max_active_processes

    #         # CONSOLE section
    #         if table_style :=

    #     except Exception as error:
    #         self.logger.exception(error)

    def init_logger(self) -> None:
        self.logger = Logger(name=__file__,
                             logformat=self.config['LOGGING']['LOGFORMAT'],
                             loglevel=logging.DEBUG)
        self.logger.add_file_handler(self.config['LOGGING']['LOGFILE'])


    def init_banner_generator(self) -> None:
        self.banner_generator = BannerGenerator()
        self.intro = self.banner_generator.random()
