#!/usr/bin/env python3
#
# amaconsole logger


import logging
from logging import (
    FileHandler,
    StreamHandler,
    Formatter
)
from pathlib import Path


class Logger(logging.Logger):
    def __init__(self, name: str, logformat: str, level=logging.DEBUG):
        super().__init__(name, level)
        self.logformat = logformat
        self.setLevel(level)
        self.level = level

    def add_file_handler(self, logfile: Path,
                         logformat: str = None, level=None):
        level = level if level else self.level
        logformat = logformat if logformat else self.logformat

        formatter = Formatter(fmt=logformat)

        handler = FileHandler(logfile)
        handler.setLevel(level)
        handler.setFormatter(formatter)

        self.addHandler(handler)

    def add_stream_handler(self, logformat: str = None, level=None):
        level = level if level is not None else self.level
        logformat = logformat if logformat is not None else self.logformat

        formatter = Formatter(fmt=logformat)

        handler = StreamHandler()
        handler.setLevel(level)
        handler.setFormatter(formatter)

        self.addHandler(handler)
