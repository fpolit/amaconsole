from pathlib import Path

VERSION='1.0.0'
AMACONSOLE_HOME= Path.joinpath(Path.home(), '.amaconsole')
HISTORY_FILE = AMACONSOLE_HOME.joinpath('console.dat')
CONFIG_FILE = AMACONSOLE_HOME.joinpath('amaconsole.json')
LOG_FILE = AMACONSOLE_HOME.joinpath('amaconsole.log')
PROMPT = 'ama > '
