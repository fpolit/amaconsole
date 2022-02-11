#!/usr/bin/env python3
#
# Commands to interact with modules
#
# State: REFACTORED - Dec 8 2021

from typing import List
import argparse
from cmd2 import (
    CommandSet,
    with_default_category,
    with_argparser,
    Cmd2ArgumentParser
)

from ama.commands import CommandCategory
from ama.utils.fineprint import (
    print_status
)
from ama.processor.process import ProcessState, Process

from ama.utils.misc import processes2table

@with_default_category(CommandCategory.SCHEDULER)
class SchedulerMonitor(CommandSet):
    """
    Commands to monitor scheduler
    """

    threads_parser = argparse.ArgumentParser()


    def do_nthreads(self, _):
        """
        Monitor active threads in scheduler
        """

        nthreads: int = len(self._cmd.scheduler._active_threads)
        print_status(f"Active threads: {nthreads}")

    sjobs_parser = argparse.ArgumentParser()
    sjobs_state_help = (
        "filter jobs by states "
        f"(states: {[state for state in ProcessState.__members__]})"
    )
    sjobs_parser.add_argument(
        '-s', '--states',
        nargs='*',
        metavar='STATE',
        default=[ProcessState.PENDING,
                 ProcessState.RUNNING,
                 ProcessState.COMPLETED],
        choices=[state for state in ProcessState.__members__],
        help=sjobs_state_help
    )
    sjobs_parser.add_argument('-v', '--verbose',
                              action='store_true',
                              help='include state reason')

    @with_argparser(sjobs_parser)
    def do_sjobs(self, args):
        """
        Monitor scheduled jobs
        """
        processes: List[Process] = []
        for state in args.states:
            processes += self._cmd.scheduler.getjobs(state)

        processes2table(processes,
                        verbose=args.verbose)

    # def do_jkill(self, args):
    #     """
    #     Job killer
    #     """
    #     pass
