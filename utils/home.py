#!/usr/bin/env python3
#
# amaconsole home - create directories and files in amaconsole home


import os
import sys
import yaml
import shutil
import logging
import logging.handlers
import argparse
import configparser
from pathlib import Path
from typing import Dict, Any

from amaconsole import LOGGING_LEVELS, DEFAULT_LOGFMT
from amaconsole.utils import FileSystem, DirNode, FileNode
from amaconsole.parsers import (
    parser,
    bgprocparser,
    cmdparser,
    ctrlparser,
    resmanparser
)

def dump2file(data: Dict[str, Any], filepath: str, **kwargs) -> None:
    with open(filepath, 'w', encoding='utf-8') as f:
        yaml.dump(data, f, indent=4, **kwargs)

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

    parser.add_argument('--logformat',
                        default=DEFAULT_LOGFMT,
                        help='Format for default logger')
    parser.add_argument('--loglevel',
                        default=10,
                        choices=LOGGING_LEVELS,
                        type=int,
                        help='Log level for default logger')


    cmdparser.add_argument('--console-logformat',
                           dest='console_logformat',
                           default=DEFAULT_LOGFMT,
                           help='Format for console logs')
    cmdparser.add_argument('--console-loglevel',
                           default=10,
                           dest='console_loglevel',
                           choices=LOGGING_LEVELS,
                           type=int,
                           help='Log level for console logger')

    bgprocparser.add_argument('--bgprocessor-logformat',
                              dest='bgprocessor_logformat',
                              default=DEFAULT_LOGFMT,
                              help='Format for background processor logs')
    bgprocparser.add_argument('--bgprocessor-loglevel',
                              default=10,
                              dest='bgprocessor_loglevel',
                              choices=LOGGING_LEVELS,
                              type=int,
                              help='Log level for background processes logger')

    resmanparser.add_argument('--resman-logformat',
                              dest='resman_logformat',
                              default=DEFAULT_LOGFMT,
                              help='Format for resource manager logs')
    resmanparser.add_argument('--resman-loglevel',
                              default=10,
                              dest='resman_loglevel',
                              choices=LOGGING_LEVELS,
                              type=int,
                              help='Log level for resource manager logger')

    ctrlparser.add_argument('--controller-logformat',
                            dest='controller_logformat',
                            default=DEFAULT_LOGFMT,
                            help='Format for resource manager logs')
    ctrlparser.add_argument('--controller-loglevel',
                            default=10,
                            dest='controller_loglevel',
                            choices=LOGGING_LEVELS,
                            type=int,
                            help='Log level for controller logger')


    args = parser.parse_args()

    basedir = Path(args.basedir)
    AMACONSOLE_HOME = FileSystem(root=basedir)
    HISTORY_FILE = AMACONSOLE_HOME.add_file('history.dat')
    AMACONSOLE_EXTENSIONS = AMACONSOLE_HOME.add_subdir('extensions')
    AMACONSOLE_LOGS = AMACONSOLE_HOME.add_subdir('logs')
    MAIN_LOGFILE = AMACONSOLE_LOGS.add_file('amaconsole.log')
    BGPROCESSOR_LOGFILE = AMACONSOLE_LOGS.add_file('bgprocessor.log')
    CONTROLLER_LOGFILE = AMACONSOLE_LOGS.add_file('controller.log')
    RESMAN_LOGFILE = AMACONSOLE_LOGS.add_file('resman.log')


    # Creating amaconsole directories and file
    if AMACONSOLE_HOME.path.exists() and not args.asume_yes:
        print(f"Directory {AMACONSOLE_HOME.path} does already exists")
        answer = input('Do you want to override configuration files?[y/n] ')
        if answer == 'n':
            sys.exit(1)

    AMACONSOLE_HOME.create()

    # Initializing configuration file

    config: Dict[str, Any] = {}
    config['LOCATION'] = {
        'amaconsole_home': str(AMACONSOLE_HOME.path),
        'amaconsole_extensions': str(AMACONSOLE_EXTENSIONS.path),
    }

    config['CONTROLLER'] = {
        'controller_port': args.controller_port,
        'controller_data_port': args.controller_data_port
    }

    config['LOGGING'] = {
        'version': 1,
        'loglevel': args.loglevel,
        'root': { # default logger
            'handlers': ['main_logfile'],
            'level': logging.DEBUG,
        },
        'loggers':{
            'console':{
                'handlers': ['main_logfile'],
                'level': logging.DEBUG,
            },
            'bgprocessor':{
                'handlers': ['main_logfile', 'bgprocessor_logfile'],
                'level': logging.DEBUG,
            },
            'controller':{
                'handlers': ['main_logfile', 'controller_logfile'],
                'level': logging.DEBUG,
            },
            'resman':{
                'handlers': ['main_logfile', 'resman_logfile'],
                'level': logging.DEBUG,
            }
        },
        'handlers':
        {
            'main_logfile': {
                'class': 'logging.handlers.RotatingFileHandler',
                'filename': str(MAIN_LOGFILE.path),
                'level': args.console_loglevel,
                'formatter': 'console_logfmt',
                'maxBytes': 1024*1024,
                'backupCount': 5
            },
            'bgprocessor_logfile': {
                'class': 'logging.FileHandler',
                'filename': str(BGPROCESSOR_LOGFILE.path),
                'level': args.bgprocessor_loglevel,
                'formatter': 'bgprocessor_logfmt',
            },
            'controller_logfile':{
                'class': 'logging.FileHandler',
                'filename': str(CONTROLLER_LOGFILE.path),
                'level': args.controller_loglevel,
                'formatter': 'controller_logfmt',
            },
            'resman_logfile':{
                'class': 'logging.FileHandler',
                'filename': str(RESMAN_LOGFILE.path),
                'level': args.resman_loglevel,
                'formatter': 'resman_logfmt',
            }
        },
        'formatters':{
            'default_logfmt':{
                'format': DEFAULT_LOGFMT,
            },
            'console_logfmt':{
                'format': args.console_logformat,
            },
            'bgprocessor_logfmt':{
                'format': args.bgprocessor_logformat,
            },
            'controller_logfmt':{
                'format': args.controller_logformat,
            },
            'resman_logfmt':{
                'format': args.resman_logformat,
            }
        }
    }

    config['PROCESSES'] = {
        'max_active_processes': args.max_active_processes,
        'max_queue_size': args.max_queue_size,
    }

    config['CONSOLE'] = {
        'history_file': str(HISTORY_FILE.path),
        'tablefmt': args.tablefmt,
        'show_tips': args.show_tips
    }

    AMACONSOLE_CONFIGFILE = os.path.join(AMACONSOLE_HOME.path, 'amaconsole.yml')
    dump2file(config, AMACONSOLE_CONFIGFILE)

    REPO_SOURCE_DIR=os.path.dirname(os.path.dirname(__file__))
    README_EXTENSIONS = os.path.join(REPO_SOURCE_DIR, 'data/extensions/README')
    copyfile(README_EXTENSIONS, AMACONSOLE_EXTENSIONS.path)

    EXTENSIONS_EXAMPLE = os.path.join(REPO_SOURCE_DIR, 'data/extensions/simple_commands.py')
    copyfile(EXTENSIONS_EXAMPLE, AMACONSOLE_EXTENSIONS.path)

    EXTENSIONS_REQUIREMENTS = os.path.join(REPO_SOURCE_DIR, 'data/extensions/requirements.txt')
    copyfile(EXTENSIONS_REQUIREMENTS, AMACONSOLE_EXTENSIONS.path)

if __name__=='__main__':
    create()
