#!/usr/bin/env python3
#
# Background process

from __future__ import annotations

from datetime import timedelta, datetime
from threading import Thread
from typing import Callable, Tuple, List

from amaconsole.utils import RedirectOutput

class Process:
    def __init__(self, target: Callable, args: Tuple,
                 depends: List[int] = None,
                 priority: int = 0,
                 name: str = None,
                 delay: timedelta = None,
                 outfile: str = None):
        self.pid: int = None # assigned by Background Processor
        self.name = name
        self.thread = Thread(target=target, args=args)
        self.priority = Process.validate_priority(priority)
        self.delay = delay if delay else timedelta()
        self.submit_time = datetime.now()
        self.command = target.__name__
        self.reason: str = None # assigned by Background Processor
        self.args = args
        self.depends = depends if depends else []

        self.outfile = outfile
        if not outfile:
            self.outfile = 'ama-%i.out'


    def set_pid(self, pid):
        self.pid = pid

        if self.outfile.find('%i') != -1:
            self.outfile = self.outfile % pid

    def start(self):
        with RedirectOutput(filepath=self.outfile):
            self.thread.start()


    @staticmethod
    def validate_priority(priority) -> int:
        if priority < -20:
            priority = -20
        elif priority > 19:
            priority = 19

        return priority


    def __lt__(self, process: Process):
        return self.priority > process.priority


    def __str__(self):
        return f"Process(cmd: {self.command}, args: {self.args})"
