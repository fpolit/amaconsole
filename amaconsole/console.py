#!/usr/bin/env python3
#
# ama console

import os
from threading import Thread
import json
from cmd2 import Cmd
#from pathlib import Path
from typing import Dict, Any
#import psutil

from amaconsole import (
    HISTORY_FILE,
    CONFIG_FILE,
    PROMPT
)

from amaconsole.commands import CommandCategory
#from amaconsole.banner import BannerGenerator

# commands
#from amaconsole.commands.console import SimpleCmds
# from amaconsole.commands.module import (
#     Search,
#     ModuleInteraction,
#     ModuleInformation,
#     ModuleLoader
# )


class AmaConsole(Cmd):
    """
    Console to interact with Ama-Framework (Ama Console)
    """

    def __init__(self, host:str,
                 port:int = 10001, dport:int = 10101, **kwargs):
        super().__init__(allow_redirection=True,
                         persistent_history_file=HISTORY_FILE)

        self.default_to_shell = True
        self.debug = True
        self.intro = None
        self.prompt = PROMPT
        self.continuation_prompt = "> "
        self.default_category = CommandCategory.CONSOLE
        self.channel = None
        self.connection_args = {
            'host': host,
            'port': port,
            'dport': dport,
            'kwargs': kwargs
        }
        self.config: Dict[str, Any] = {}

        self.logger = None
        #self.banner_generator: BannerGenerator = None

        # preloop hooks
        # self.register_preloop_hook(self.init_logger)
        # self.register_preloop_hook(self.init_config)
        # self.register_preloop_hook(self.init_amactld_connection)
        # self.register_preloop_hook(self.init_banner_generator)

        # postloop hooks
        #self.register_postloop_hook(self.save_config)


    def init_config(self) -> None:
        try:
            self.config = {}
            with open(CONFIG_FILE, 'r', encoding='utf-8') as config_file:
                self.config = json.load(config_file)

        except Exception as error:
            self.logger.exception(error)

    def init_logger(self) -> None:
        # self.logger_manager = LoggerManager(
        #     logformat='[%(asctime)s] %(name)s - %(levelname)s - %(message)s',
        #     main_logger_name=__name__
        # )
        self.logger = self.logger_manager.main_logger


    def save_config(self) -> None:
        try:
            oldconfig = {}
            with open(CONFIG_FILE, 'r', encoding='utf-8') as config_file:
                oldconfig = json.load(config_file)

            if self.config and self.config != oldconfig:
                with open(CONFIG_FILE, 'w', encoding='utf-8') as config_file:
                    json.dump(self.config, config_file, indent=4)

        except Exception as error:
            self.logger.exception(error)

    # def init_banner_generator(self) -> None:
    #     self.banner_generator = BannerGenerator(self.module_pool)
    #     self.intro = self.banner_generator.random()
