#!/usr/bin/env python3
#
# AMA home - create directories and files in AMA home

import os
import shutil
import psutil
import json

from typing import Dict, Any
from pathlib import Path

from ama.utils.files import Dir

from ama import (
    AMA_PKG_PATH,
    AMA_HOME,
    LOGS_PATH,
    CONFIG_PATH,
    POTFILES_PATH,
    SESSIONS_PATH,
    CUSTOM_MODULES_PATH,
    AMA_CONFIG_FILE,
    SESSION_CONFIG_FILE,
    PROCESSOR_CONFIG_FILE,
    AMA_HISTORY_FILE,
    AMA_DEBUG_LOG_FILE,
    AMA_WARNING_LOG_FILE,
    AMA_ERROR_LOG_FILE,
    AMA_PROCESSOR_LOG_FILE,
    DB_CREDS_FILE,
    JOHN_POTFILE,
    HASHCAT_POTFILE,
    ATTACK_MODULES,
    AUXILIARY_MODULES,
    PLUGINS_CONFIG_PATH,
    CUPP_CONFIG_FILE,
    LONGTONGUE_CONFIG_FILE,
    WORDLISTCTL_REPOS_FILE,
    WORDLISTCTL_CONFIG_FILE,
    EXTENSIONS_PATH,
    CUSTOM_FULLATTACKS_SCRIPT
)

def dump2file(data: Dict[str, Any], filepath: Path, **kwargs) -> None:
    with open(filepath, 'w', encoding='utf-8') as f:
        json.dump(data, f, indent=4, **kwargs)

def create_ama_home():
    """
    Create AMA home directory

    STRUCTURE: BASE_PATH is HOME user
    # .ama
    # |
    # |- logs
    # | |- debug.log       # log functionality of the framework (logging level: DEBUG)
    # | |- warning.log     # log warnings of framework (loging level: WARNING)
    # | |- error.log       # log errors (logging level: ERROR)
    # | |- processor.log   # log processor errors (logging level: DEBUG)
    # | |- history.dat     (history of commands)
    # |
    # |- config
    # | |- ama.json        (ama's configuration file)
    # | |- database.json   (database credentials)
    # | |- session.json    (session's configuration file)
    # | |- plugins         (configuration files - plugins
    # |                      struct:
    # |                        PLUGIN_NAME
    # |                           |- PLUGIN_NAME.json (configuration file)
    # |                           |- ...
    # |                    )
    # |
    # |- potfiles
    # | |- john.pot
    # | |- hashcat.pot
    # |
    # |- sessions          (generated files in sessions,
    # |                      struct:
    # |                          SESSION-ID
    # |                             |- pre-module.out
    # |                             |- main-module.out
    # |                             |- post-module.out
    # |                             |- output  (output files)
    # |                    )
    # | - setup.py         (Ama-Framework extensions package)
    # | - extensions
    # |   |- __init__.py
    # |   |- fullattacks.py    # custom fullattacks
    # |   |- modules           # custom modules
    # |   | |- __init__.py
    # |   | |- attack
    # |   | | |- __init__.py
    # |   | |- auxiliary
    # |   | | |- __init__.py
    # |
    """
    ama_home = Dir(AMA_HOME)

    # subdirs
    logs = Dir(LOGS_PATH,
               files=[AMA_DEBUG_LOG_FILE,
                      AMA_WARNING_LOG_FILE,
                      AMA_ERROR_LOG_FILE,
                      AMA_PROCESSOR_LOG_FILE,
                      AMA_HISTORY_FILE])

    config = Dir(CONFIG_PATH,
                 files=[AMA_CONFIG_FILE,
                        DB_CREDS_FILE,
                        SESSION_CONFIG_FILE,
                        PROCESSOR_CONFIG_FILE])

    plugins = Dir(PLUGINS_CONFIG_PATH,
                  subdirs=['cupp',
                           'wordlistctl',
                           'longtongue'])

    config.add_subdir(plugins)

    potfiles = Dir(POTFILES_PATH, files=[JOHN_POTFILE, HASHCAT_POTFILE])
    sessions = Dir(SESSIONS_PATH)

    extensions = Dir(EXTENSIONS_PATH,
                     files=['__init__.py',
                            CUSTOM_FULLATTACKS_SCRIPT])

    modules = Dir(CUSTOM_MODULES_PATH, files=['__init__.py'])
    attack_modules = Dir(ATTACK_MODULES, files=['__init__.py'])
    auxiliary_modules = Dir(AUXILIARY_MODULES, files=['__init__.py'])
    modules.add_subdirs([attack_modules, auxiliary_modules])

    extensions.add_subdir(modules)

    ama_home.add_subdirs([logs,
                          config,
                          potfiles,
                          sessions,
                          extensions])

    ama_home.create()


    #  init ama config file
    ama_config = {
        'PROCESS_COUNT': 0,
        'MAX_ACTIVE_THREADS': psutil.cpu_count(),
        'MAX_QUEUE_SIZE': 1000
    }

    wordlistctl_config = {
        'WORDLIST_PATH': "/usr/share/wordlists",
        'RETRY_COUNT': 5
    }

    longtongue_config = {
        'SYMBOLS': [
            ".",
            "-",
            "_",
            "?",
            "!",
            "@",
            "#",
            "+",
            "*",
            "%",
            "&",
            "$",
        ],
        'STARTING_YEAR': 1985,
        'ENDING_YEAR': 1999,
        'MIN_PASSWD_LENGTH': 6,
        'LEET_CHARS': {
            'a': ['4'],
            'b': ['8'],
            'e': ['3'],
            'g': ['6'],
            'i': ['1'],
            'o': ['0'],
            's': ['5'],
            't': ['7'],
            'z': ['2']
        },
        #'COMMON_PASSWDS': 'seclists/Passwords/Common-Credentials/10k-most-common.txt'
    }
    #import pdb; pdb.set_trace()
    extensions = Path(os.path.join(os.path.dirname(__file__), 'extensions'))

    dump2file(ama_config, AMA_CONFIG_FILE)
    dump2file(wordlistctl_config, WORDLISTCTL_CONFIG_FILE)
    dump2file(longtongue_config, LONGTONGUE_CONFIG_FILE)

    shutil.copy(extensions.joinpath('setup.py'), EXTENSIONS_PATH)
    shutil.copy(extensions.joinpath('fullattacks.py'), EXTENSIONS_PATH)
    shutil.copy(extensions.joinpath('README'), EXTENSIONS_PATH)
    extensions.joinpath('requirements.txt').touch()

    # init configuration file - plugins
    cupp_config = AMA_PKG_PATH.joinpath("plugins/src/cupp/cupp.cfg")
    repos_wordlistctl = AMA_PKG_PATH.joinpath("plugins/src/wordlistctl/repo.json")

    shutil.copyfile(cupp_config, CUPP_CONFIG_FILE)
    shutil.copyfile(repos_wordlistctl, WORDLISTCTL_REPOS_FILE)
