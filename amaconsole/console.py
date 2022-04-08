
#!/usr/bin/env python3
#
# ama console

import os
#import json
import argparse
import logging
import cmd2
import configparser
from cmd2 import Cmd
from pathlib import Path
from threading import Thread
from typing import Dict, List, Any

from amaconsole import PROMPT
from amaconsole.commands import CommandCategory
from amaconsole.banner import BannerGenerator
from amaconsole.processor import BGProcessor
from amaconsole.utils import Logger
from amaconsole.extensions import load_extensions

# commands
from amaconsole.commands.bgprocess import BGProcessCmds
from amaconsole.commands.console import (
    ExtensionsCommands,
    SimpleCmds
)


class AmaConsole(Cmd):
    """
    Console to interact with Ama-Framework
    """

    def __init__(self,
                 config_args: argparse.Namespace = None,
                 config_file: str = None,
                 **kwargs):
        self.config: Dict[str, Dict[str, Any]] = {}
        #self.connection_args = {}
        self.init_config(config_args, config_file)

        super().__init__(allow_redirection=True,
                         persistent_history_file=self.config['CONSOLE']['history_file'], **kwargs)

        self.default_to_shell = True
        self.debug = True
        self.intro = None
        self.prompt = PROMPT
        self.continuation_prompt = "> "
        self.default_category = CommandCategory.DEFAULT_CONSOLE
        self.channel = None
        self.extensions: Dict[str, cmd2.CommandSet] = {}

        self.logger = None
        self.banner_generator: BannerGenerator = None

        self.bg_processor: BGProcessor = None
        self.bg_processor_thread: Thread = None


        # preloop hooks
        self.register_preloop_hook(self.init_logger)
        # self.register_preloop_hook(self.init_amacontroller_connection)
        self.register_preloop_hook(self.init_custom_extensions)
        self.register_preloop_hook(self.init_background_processor)
        self.register_preloop_hook(self.init_banner_generator)

        # postloop hooks

    def init_background_processor(self) -> None:
        self.bg_processor = BGProcessor(
            logfile=self.config['LOGGING']['logfile'],
            max_active_processes=self.config['PROCESSES']['max_active_processes'],
            logformat=self.config['LOGGING']['logformat'],
            loglevel=self.config['LOGGING']['loglevel']
        )

        # start processor thread
        self.bg_processor_thread = Thread(
            target=self.bg_processor.processor,
            name='process-processor',
            daemon=True)

        self.bg_processor_thread.start()

    def init_custom_extensions(self) -> None:
        sdir: List[Path] = []

        if amaconsole_extensions := self.config['LOCATION']['amaconsole_extensions']:
            sdir.append(amaconsole_extensions)

        if include_dir := self.config['EXTRA'].get('include_dir'):
            sdir.append(include_dir)

        for basedir in sdir:
            extensions = load_extensions(basedir, self.config['CONSOLE']['verbose'])
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
        try:
            if not config_file:
                # check config file in home directory
                config_file = os.path.join(os.environ['HOME'],
                                               '.amaconsole/amaconsole.conf')
                if not os.path.isfile(config_file):
                    config_file=None

                # check if AMACONSOLE_HOME variable was configured
                amaconsole_home = os.getenv('AMACONSOLE_HOME')
                if amaconsole_home:
                    config_file = os.path.join(amaconsole_home, 'amaconsole.conf')
                    if not os.path.isfile(config_file):
                        config_file=None

            config_file_parser = configparser.ConfigParser(interpolation=None)
            if config_file:
                config_file_parser.read(config_file)

            config_args = vars(config_args)
            parsed_config_args = {k.replace('-', '_'): v for k, v in config_args.items() if v is not None}

            sections = config_file_parser.sections()
            for section in sections:
                self.config[section] = dict(config_file_parser.items(section))
                print(f"([BEFORE]section: {section}) {self.config[section]}")

                tmp_parsed_config_args = parsed_config_args.copy()
                for key in parsed_config_args:
                    if key in self.config[section]:
                        self.config[section][key] = tmp_parsed_config_args.pop(key)

                parsed_config_args = tmp_parsed_config_args


                print(f"([AFTER]section: {section}) {self.config[section]}")


            self.config['EXTRA'] = parsed_config_args

            if config_file:
                self.config['EXTRA']['config_file'] = config_file

            # casting values
            self.config['CONTROLLER']['controller_port'] = int(self.config['CONTROLLER']['controller_port'])
            self.config['CONTROLLER']['controller_data_port'] = int(self.config['CONTROLLER']['controller_data_port'])
            self.config['LOGGING']['loglevel'] = int(self.config['LOGGING']['loglevel'])
            self.config['PROCESSES']['max_active_processes'] = int(self.config['PROCESSES']['max_active_processes'])
            self.config['PROCESSES']['max_queue_size'] = int(self.config['PROCESSES']['max_queue_size'])

        except Exception as error:
            print(error)

    def init_logger(self) -> None:
        self.logger = Logger(name=__file__,
                             logformat=self.config['LOGGING']['logformat'],
                             level=self.config['LOGGING']['loglevel'])
        self.logger.add_file_handler(self.config['LOGGING']['logfile'])


    def init_banner_generator(self) -> None:
        self.banner_generator = BannerGenerator(cmd_app=self)
        self.intro = self.banner_generator.random()
