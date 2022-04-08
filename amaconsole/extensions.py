#!/usr/bin/env python3
#
# Functions to import custom extensions (commands)

import os
import cmd2
import importlib
import inspect

from typing import List
from pathlib import Path

def load_extension_from_script(script_path: Path, verbose:bool = True) -> List[cmd2.CommandSet]:
    extensions: List[cmd2.CommandSet] = []

    script = os.path.basename(script_path)
    scriptname, ext = os.path.splitext(script)
    if ext != '.py':
        raise Exception(f"Script {script_path} isn't a python script")

    spec = importlib.util.spec_from_file_location(scriptname, script_path)
    module = importlib.util.module_from_spec(spec)

    if verbose:
        print(f"Analyzing {module.__name__} module")

    for name, cls in inspect.getmembers(module):
        try:
            if cls and issubclass(cls, cmd2.CommandSet) and cls != cmd2.CommandSet:
                if verbose:
                    print("Importing {name} extension from {script_path}")
                extensions.append(cls)

        except Exception as error:
            if verbose:
                print(f"Error: {error}")

    return extensions

def load_extensions(basedir: Path, verbose : bool = True) -> List[cmd2.CommandSet]:
    if not os.path.isdir(basedir):
        raise NotADirectoryError(f"Directory {basedir} doesn't exist")

    extensions: List[cmd2.CommandSet] = []

    for filename in os.listdir(basedir):
        if filename.endswith('.py'):
            filepath = os.path.join(basedir, filename)
            extensions += load_extension_from_script(filepath, verbose)

    return extensions
