
#!/usr/bin/env python3
#
# ama console

import os
#import json
import argparse
import cmd2
import yaml
import importlib
import logging
import logging.config
import configparser
from cmd2 import Cmd
from pathlib import Path
from threading import Thread
from typing import Dict, List, Any, Optional


from amaconsole import PROMPT, AMACONSOLE_VERSION
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
                 verbose: bool = False,
                 **kwargs):
        self.config: Dict[str, Dict[str, Any]] = {}
        self.init_config(config_args, config_file, verbose)

        super().__init__(allow_redirection=True,
                         persistent_history_file=self.config['CONSOLE']['history_file'], **kwargs)

        self.default_to_shell = True
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


        self.hidden_commands.append('pdbtrace')

        # preloop hooks
        self.register_preloop_hook(self.init_logger)
        # self.register_preloop_hook(self.init_amacontroller_connection)
        self.register_preloop_hook(self.init_custom_extensions)
        self.register_preloop_hook(self.init_background_processor)
        self.register_preloop_hook(self.init_banner_generator)

        # postloop hooks

    # def init_settable_options(self) -> None:
    #     options: List[cmd2.Settable] = [
    #         cmd2.Settable('pdb_trace', bool, 'Enable pdb trace (Debug purposes)', self, onchange_cb=self._enable_pdb_trace),
    #         #cmd2.Settable('loglevel', bool, 'Log level', self, onchange_cb=self._update_loglevel),
    #     ]

    #     for opt in options:
    #         self.add_settable(opt)

    def init_background_processor(self) -> None:
        self.bg_processor = BGProcessor(
            max_active_processes=self.config['PROCESSES']['max_active_processes'],
            maxsize = self.config['PROCESSES']['max_queue_size']
        )

        # start processor thread
        self.logger.info('Starting background processor thread')
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
            extensions = load_extensions(basedir, self.config['EXTRA']['verbose'])
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

    def _get_amacontroller_version(self) -> str:
        return 'None' # RPC CALL

    def _get_amadb_version(self) -> str:
        return 'None' # RPC CALL

    def _get_amacore_version(self) -> Optional[str]:
        version: str = None
        try:
            from amaconsole import AMACORE_VERSION
            version = AMACORE_VERSION
        except ModuleNotFoundError as error:
            self.logger.exception(error)

        return version

    def _get_amaproto_version(self) -> Optional[str]:
        version: str = None
        try:
            from amaconsole import AMAPROTO_VERSION
            version = AMAPROTO_VERSION
        except ModuleNotFoundError as error:
            self.logger.exception(error)

        return version

    def _get_ama_component_versions(self) -> Dict[str, str]:
        versions = {
            'amacore': self._get_amacore_version(),
            'amaproto': self._get_amaproto_version(),
            'amaconsole': AMACONSOLE_VERSION,
            'amacontroller': self._get_amacontroller_version(),
            'amadb': self._get_amadb_version()
        }

        return versions


    def init_config(self,
                    config_args: argparse.Namespace,
                    config_file: str = None,
                    verbose: bool = False) -> None:
        """
        Override configurations of config_file (dafault configurations) with supplied config_args
        """
        try:
            if not config_file:
                # check config file in home directory
                config_file = os.path.join(os.environ['HOME'],
                                               '.amaconsole/amaconsole.yml')
                if not os.path.isfile(config_file):
                    config_file=None

                # check if AMACONSOLE_HOME variable was configured
                amaconsole_home = os.getenv('AMACONSOLE_HOME')
                if amaconsole_home:
                    config_file = os.path.join(amaconsole_home, 'amaconsole.yml')
                    if not os.path.isfile(config_file):
                        config_file=None

            config_file_args = {}
            if config_file:
                if verbose:
                    self.poutput(f'Configuration file: {config_file}')
                with open(config_file, 'r') as f:
                    config_file_args = yaml.safe_load(f)

            config_args = vars(config_args)
            parsed_config_args = {k.replace('-', '_'): v for k, v in config_args.items() if v is not None}

            for section in config_file_args:
                self.config[section] = config_file_args.get(section, {})

                tmp_parsed_config_args = parsed_config_args.copy()
                for key in parsed_config_args:
                    if key in self.config[section]:
                        self.config[section][key] = tmp_parsed_config_args.pop(key)

                parsed_config_args = tmp_parsed_config_args

                if verbose:
                    self.poutput(f"(section: {section}) {self.config[section]}")


            self.config['EXTRA'] = parsed_config_args

            if config_file:
                self.config['EXTRA']['config_file'] = config_file

        except Exception as error:
            print(error)

    def init_logger(self) -> None:
        logging.config.dictConfig(self.config['LOGGING'])
        self.logger = logging.getLogger('main')

        if self.config['EXTRA']['debug']:
            self.logger.info(
                'Debug mode enable, adding stream handler to loggers'
            )
            stream_handler = logging.StreamHandler()
            stream_handler.setLevel(self.config['LOGGING']['loglevel'])
            for logger_name in self.config['LOGGING']['loggers']:
                logger = logging.getLogger(logger_name)
                logger.addHandler(stream_handler)

            default_logger = logging.getLogger('root')
            default_logger.addHandler(stream_handler)

    def init_banner_generator(self) -> None:
        self.banner_generator = BannerGenerator(cmd_app=self)
        self.intro = self.banner_generator.random()
