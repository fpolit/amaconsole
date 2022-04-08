#!/usr/bin/env python3


import sys
import shlex
import subprocess
from subprocess import Popen
from typing import List, Union

class Shell:
    """
    Shell class to execute shell commands in the system
    """
    @staticmethod
    def exec(cmd: Union[str, List[str]], **kwargs):
        """
        Arguments
        =========
        cmd: Union[str, List[str]]
            Command to execute
        kwargs:
            Arguments to pass to Popen class
        """
        if isinstance(cmd, str):
            cmd = shlex.split(cmd)

        kwargs['stdin']  = subprocess.DEVNULL
        kwargs['stdout'] = kwargs['stderr'] = sys.stdout

        with Popen(cmd, **kwargs) as proc:
            proc.wait()
