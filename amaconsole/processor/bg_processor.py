#!/usr/bin/env python3
#
# Background processor

from __future__ import annotations

import logging
from typing import List
from queue import PriorityQueue
from time import sleep

from amaconsole.processor import Process
from amaconsole.utils import Logger

class BGProcessor:
    """Background processor"""

    SUBMITTED_PROCESS_COUNT: int
    MAX_ACTIVE_PROCESSES: int
    pending: PriorityQueue
    processing: List[Process]
    completed: List[Process]
    logger: Logger

    _instance: BGProcessor = None

    def __new__(cls, logfile: str,
                max_active_processes=8,
                maxsize=1000,
                logformat: str = None,
                loglevel = logging.DEBUG):
        if not cls._instance:
            cls.SUBMITTED_PROCESS_COUNT = 0
            cls.MAX_ACTIVE_PROCESSES = max_active_processes
            cls.pending = PriorityQueue(maxsize)
            cls.completed = []
            cls.processing = []

            # logger creation
            cls.logger = Logger(__file__, logformat, loglevel)
            cls.logger.add_file_handler(logfile)

            cls._instance = super(BGProcessor, cls).__new__(cls)

        return cls._instance

    @classmethod
    def submit(cls, process: Process):
        cls.SUBMITTED_PROCESS_COUNT += 1
        process.set_pid(cls.SUBMITTED_PROCESS_COUNT)

        print(f"[*] Submitted process: {cls.SUBMITTED_PROCESS_COUNT}")
        cls.pending.put(process)

        cls.logger.info(f"Submitted process: {process.pid} - process: {process}")

    @classmethod
    def processor(cls):
        while True:
            _, process = cls.pending.get()
            sleep(.001)
