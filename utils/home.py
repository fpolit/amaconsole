#!/usr/bin/env python3
#
# amaconsole home - create directories and files in amaconsole home


import os
import sys
import json
import shutil
import argparse
import configparser
from pathlib import Path
from typing import Dict, Any

from amaconsole.utils import FileSystem, DirNode, FileNode
from amaconsole.config import parser

def dump2file(data: Dict[str, Any], filepath: str, **kwargs) -> None:
    with open(filepath, 'w', encoding='utf-8') as f:
        json.dump(data, f, indent=4, **kwargs)

def copyfile(filepath: str, destination: str) -> None:
    if os.path.isdir(destination):
        shutil.copy(filepath, destination)
    elif os.path.isfile(destination):
        shutil.copyfile(filepath, destination)
    else:
        print("Some error occurred")

def create():
    parser.description='Initialize amaconsole home directory and configuration files'

    parser.add_argument('-b', '--basedir',
                        default=os.path.join(os.environ['HOME'], '.amaconsole'),
                        help='amaconsole home directory')
    parser.add_argument('-y', '--asume-yes',
                        dest='asume_yes',
                        action='store_true',
                        help='Automatic yes to prompts; assume "yes" as answer to all prompts and run non-interactively')
    parser.add_argument('-hF','--history-file', dest='history_file',
                        help='Location of history file (default location: AMACONSOLE_HOME/history.dat)')
    parser.add_argument('-cP','--controller-port',
                        default=1317,
                        dest='controller_port',
                        help='Amacontroller port')
    parser.add_argument('-dP','--data-port',
                        default=1318,
                        dest='controller_data_port',
                        help='Amacontroller port')

    args = parser.parse_args()

    basedir = Path(args.basedir)
    AMACONSOLE_HOME = FileSystem(root=basedir)

    AMACONSOLE_EXTENSIONS = AMACONSOLE_HOME.add_subdir('extensions')

    if not args.logfile:
        LOGFILE = AMACONSOLE_HOME.add_file('amaconsole.log')
    else:
        LOGFILE = FileNode(name=args.logfile)

    if not args.history_file:
        HISTORY_FILE = AMACONSOLE_HOME.add_file('history.dat')
    else:
        HISTORY_FILE = FileNode(name=args.history_file)


    # Creating amaconsole directories and file
    if AMACONSOLE_HOME.path.exists() and not args.asume_yes:
        print(f"Directory {AMACONSOLE_HOME.path} does already exists")
        answer = input('Do you want to override configuration files?[y/n] ')
        if answer == 'n':
            sys.exit(1)

    AMACONSOLE_HOME.create()

    if args.logfile:
        LOGFILE.create()

    if args.history_file:
        HISTORY_FILE.create()

    # Initializing configuration file

    config = configparser.ConfigParser()
    config['LOCATION'] = {
        'amaconsole_home': AMACONSOLE_HOME.path,
        'amaconsole_extensions': AMACONSOLE_EXTENSIONS.path,
    }

    config['CONTROLLER'] = {
        'controller_port': args.controller_port,
        'controller_data_port': args.controller_data_port
    }

    config['LOGGING'] = {
        'logfile': LOGFILE.path,
        'logformat': args.logformat,
        'loglevel': 10
    }

    config['PROCESSES'] = {
        'max_active_processes': args.max_active_processes,
        'max_queue_size': args.max_queue_size,
    }

    config['CONSOLE'] = {
        'history_file': HISTORY_FILE.path,
        'tablefmt': args.tablefmt,
        'show_tips': args.show_tips,
        'verbose': args.verbose
    }

    AMACONSOLE_CONFIGFILE = os.path.join(AMACONSOLE_HOME.path, 'amaconsole.conf')
    with open(AMACONSOLE_CONFIGFILE, 'w') as f:
        config.write(f)

    REPO_SOURCE_DIR=os.path.dirname(os.path.dirname(__file__))
    README_EXTENSIONS = os.path.join(REPO_SOURCE_DIR, 'data/extensions/README')
    copyfile(README_EXTENSIONS, AMACONSOLE_EXTENSIONS.path)

    EXTENSIONS_EXAMPLE = os.path.join(REPO_SOURCE_DIR, 'data/extensions/simple_commands.py')
    copyfile(EXTENSIONS_EXAMPLE, AMACONSOLE_EXTENSIONS.path)

    EXTENSIONS_REQUIREMENTS = os.path.join(REPO_SOURCE_DIR, 'data/extensions/requirements.txt')
    copyfile(EXTENSIONS_REQUIREMENTS, AMACONSOLE_EXTENSIONS.path)

if __name__=='__main__':
    create()
