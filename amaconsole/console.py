#!/usr/bin/env python3
#
# ama-framework console
#
# Status: REFACTORED - Nov 29 2021
# Maintainer: glozanoa <glozanoa@uni.pe>

import os
from threading import Thread
import json
from cmd2 import Cmd
from pathlib import Path
from typing import Dict, Any
import psutil

from ama import (
    AMA_HISTORY_FILE,
    AMA_CONFIG_FILE,
    CUSTOM_MODULES_PATH,
    AMA_PROMPT
)

from ama.manager.logger_manager import LoggerManager
from ama.processor.scheduler import Scheduler
from ama.manager.module_manager import ModuleManager
from ama.manager.session_manager import SessionManager
from ama.manager.module_pool import ModulePool
from ama.commands import CommandCategory as Category
from ama.banner import BannerGenerator
from ama.utils import Logger
from ama.exceptions import RankedException

# commands
from ama.commands.console import SimpleCmds
from ama.commands.module import (
    Search,
    ModuleInteraction,
    ModuleInformation,
    ModuleLoader
)
from ama.commands.session import SessionInteraction
from ama.commands.utilities import HashHelper
from ama.commands.plugins import (
    Cupp,
    HCUtils,
    Longtongue,
    ToHash
)
from ama.commands.scheduler import SchedulerMonitor


class AmaConsole(Cmd):
    """
    Console to interact with Ama-Framework (Ama Console)
    """

    def __init__(self):
        super().__init__(allow_redirection=True,
                         persistent_history_file=AMA_HISTORY_FILE)

        self.default_to_shell = True
        self.debug = True
        self.intro = None
        self.prompt = AMA_PROMPT
        self.continuation_prompt = "> "
        self.default_category = Category.CONSOLE
        self.config: Dict[str, Any] = {}

        self.logger: Logger = None
        self.logger_manager: LoggerManager = None
        self.module_pool: ModulePool = None
        self.module_manager: ModuleManager = None
        self.session_manager: SessionManager = None
        self.scheduler: Scheduler = None
        self.module_processor: Thread = None
        #self.db_manager = None
        self.banner_generator: BannerGenerator = None

        # preloop hooks
        self.register_preloop_hook(self.init_logger_manager)
        self.register_preloop_hook(self.init_config)
        self.register_preloop_hook(self.init_scheduler)
        self.register_preloop_hook(self.init_module_processor)
        self.register_preloop_hook(self.init_module_pool)
        self.register_preloop_hook(self.init_module_manager)
        self.register_preloop_hook(self.init_session_manager)
        #self.register_preloop_hook(self.init_db)
        self.register_preloop_hook(self.init_banner_generator)

        # postloop hooks
        self.register_postloop_hook(self.save_config)
        #self.register_postloop_hook(self.close_db_connection)



    def init_config(self) -> None:
        try:
            self.config = {}
            with open(AMA_CONFIG_FILE, 'r', encoding='utf-8') as config_file:
                self.config = json.load(config_file)

        except Exception as error:
            self.logger.exception(error)

    def init_logger_manager(self) -> None:
        self.logger_manager = LoggerManager(
            logformat='[%(asctime)s] %(name)s - %(levelname)s - %(message)s',
            main_logger_name=__name__
        )
        self.logger = self.logger_manager.main_logger

    def init_scheduler(self) -> None:
        self.logger.info("Init process schedule")

        max_active_threads: int = self.config.get('MAX_ACTIVE_THREADS', -1)
        if max_active_threads == -1:
            max_active_threads = psutil.cpu_count()

        self.scheduler = Scheduler(
            max_active_threads=max_active_threads,
            process_count=self.config.get('PROCESS_COUNT', 0),
            max_queue_size=self.config.get('MAX_QUEUE_SIZE', 1000)
        )

    def init_module_processor(self) -> None:
        self.logger.info("Init module processor")
        self.module_processor = Thread(target=self.scheduler.processor,
                                       name='module_processor',
                                       daemon=True)
        self.module_processor.start()

    def init_module_pool(self) -> None:
        module_path = Path(os.path.dirname(__file__)).joinpath('modules')
        self.module_pool = ModulePool(
            sdirs=[module_path,
                   CUSTOM_MODULES_PATH]
        )
        self.logger.info(
            f"Loaded modules: {self.module_pool.modules.count()}"
        )

    def init_module_manager(self) -> None:
        self.logger.info("Init module manager")
        self.module_manager = ModuleManager(
            module_pool=self.module_pool,
            scheduler=self.scheduler
        )

    def init_session_manager(self) -> None:
        self.logger.info("Init session manager")
        self.session_manager = SessionManager(self.module_manager)

    def save_config(self) -> None:
        try:
            oldconfig = {}
            with open(AMA_CONFIG_FILE, 'r', encoding='utf-8') as config_file:
                oldconfig = json.load(config_file)

            if self.config and self.config != oldconfig:
                with open(AMA_CONFIG_FILE, 'w', encoding='utf-8') as config_file:
                    json.dump(self.config, config_file, indent=4)

        except RankedException as error:
            self.logger.exception(error)


    # def init_db(self) -> None:
    #     try:
    #         import_module('cassandra')  # testing if cassadra-driver is installed

    #         from ama import DB_KEYSPACE, DB_CREDS_FILE
    #         from ama.manager.db import DBManager
    #         from ama.commands.db import (
    #             Connection,
    #             Loot,
    #             Workspace,
    #             Session
    #         )

    #         self.db_manager = DBManager(DB_KEYSPACE, DB_CREDS_FILE)

    #         cmdsets = [Connection, Loot, Workspace, Session]
    #         for cmdset in cmdsets:
    #             self.register_command_set(cmdset())

    #     except ImportError:
    #         self.logger.warning("Not found cassandra module")
    #         self.db_manager = None

    #     except Exception as error:
    #         self.logger.error(
    #             f"An error occurred while connecting to {DB_KEYSPACE} keyspace")
    #         self.logger.exception(error)

    def init_banner_generator(self) -> None:
        self.banner_generator = BannerGenerator(self.module_pool)
        self.intro = self.banner_generator.random()

    # def close_db_connection(self) -> None:
    #     """
    #     Close connection to database
    #     """
    #     if self.db_manager:
    #         self.db_manager.close()
    #         self.logger.info("Database session was closed")
