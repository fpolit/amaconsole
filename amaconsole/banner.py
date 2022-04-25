#!/usr/bin/env python3
#
# ama-framework banners

from __future__ import annotations

import random
from colorama import Fore, Style
from typing import List

import cmd2
from amaconsole import AMACONSOLE_VERSION
from amaconsole.utils import color
from amaconsole.utils.misc import commands_count

class BannerGenerator:
    """
    Banner Generator
    """
    ama_info: str
    banners: List[str]
    tips: List[str]

    _cmd: cmd2.Cmd

    def __new__(cls, cmd_app: cmd2.Cmd = None):
        cls._cmd = cmd_app
        cls.ama_info = color(
            "An environment to manage and scale your attacks",
            style=Style.BRIGHT
        )
        cls.banners = [
            r"""
        eeeee eeeeeee eeeee
        8   8 8  8  8 8   8
        8eee8 8e 8  8 8eee8
        88  8 88 8  8 88  8
        88  8 88 8  8 88  8
        """,
                r"""
         █████╗ ███╗   ███╗ █████╗
        ██╔══██╗████╗ ████║██╔══██╗
        ███████║██╔████╔██║███████║
        ██╔══██║██║╚██╔╝██║██╔══██║
        ██║  ██║██║ ╚═╝ ██║██║  ██║
        ╚═╝  ╚═╝╚═╝     ╚═╝╚═╝  ╚═╝
        """,
                r"""
                                 ____
           ,---,               ,'  , `.   ,---,
          '  .' \           ,-+-,.' _ |  '  .' \
         /  ;    '.      ,-+-. ;   , || /  ;    '.
        :  :       \    ,--.'|'   |  ;|:  :       \
        :  |   /\   \  |   |  ,', |  '::  |   /\   \
        |  :  ' ;.   : |   | /  | |  |||  :  ' ;.   :
        |  |  ;/  \   \'   | :  | :  |,|  |  ;/  \   \
        '  :  | \  \ ,';   . |  ; |--' '  :  | \  \ ,'
        |  |  '  '--'  |   : |  | ,    |  |  '  '--'
        |  :  :        |   : '  |/     |  :  :
        |  | ,'        ;   | |`-'      |  | ,'
        `--''          |   ;/          `--''
                       '---'
        """,
                r"""
                @@      *@@@@m     m@@@*      @@
               m@@m       @@@@    @@@@       m@@m
              m@*@@!      @ @@   m@ @@      m@*@@!
             m@  *@@      @  @!  @* @@     m@  *@@
             @@@!@!@@     !  @!m@*  @@     @@@!@!@@
            !*      @@    !  *!@*   @@    !*      @@
             !!!!@!!@     !  !!!!*  !!     !!!!@!!@
            !*      !!    :  *!!*   !!    !*      !!
          : : :   : ::: : ::: :   : ::: : : :   : :::
        """,
                r"""
        _________________________________
        _____|______|_____|________|_____
        _|_______|_____|____|__|_______|_
        __/  _  \____/     \____/  _  \__
        _/  /_\  \__/  \ /  \__/  /_\  \_
        /    |    \/    \    \/    |    \
        \____|__  /\____/\_  /\____|__  /
        __|_____\/____|____\/___|_____\/_
        ___|___|_____|__|________|___|___
        """,
                r"""
          ______  __       __  ______
         /      \|  \     /  \/      \
        |  ▓▓▓▓▓▓\ ▓▓\   /  ▓▓  ▓▓▓▓▓▓\
        | ▓▓__| ▓▓ ▓▓▓\ /  ▓▓▓ ▓▓__| ▓▓
        | ▓▓    ▓▓ ▓▓▓▓\  ▓▓▓▓ ▓▓    ▓▓
        | ▓▓▓▓▓▓▓▓ ▓▓\▓▓ ▓▓ ▓▓ ▓▓▓▓▓▓▓▓
        | ▓▓  | ▓▓ ▓▓ \▓▓▓| ▓▓ ▓▓  | ▓▓
        | ▓▓  | ▓▓ ▓▓  \▓ | ▓▓ ▓▓  | ▓▓
         \▓▓   \▓▓\▓▓      \▓▓\▓▓   \▓▓
        """,
                r"""
          _|_|    _|      _|    _|_|
        _|    _|  _|_|  _|_|  _|    _|
        _|_|_|_|  _|  _|  _|  _|_|_|_|
        _|    _|  _|      _|  _|    _|
        _|    _|  _|      _|  _|    _|
        """,
                r"""
              /\       /\\       /\\      /\
             /\ \\     /\ /\\   /\\\     /\ \\
            /\  /\\    /\\ /\\ / /\\    /\  /\\
           /\\   /\\   /\\  /\\  /\\   /\\   /\\
          /\\\\\\ /\\  /\\   /\  /\\  /\\\\\\ /\\
         /\\       /\\ /\\       /\\ /\\       /\\
        /\\         /\\/\\       /\\/\\         /\\
        """,
                r"""
               _        _           _        _
             _(_)_     (_) _     _ (_)     _(_)_
           _(_) (_)_   (_)(_)   (_)(_)   _(_) (_)_
         _(_)     (_)_ (_) (_)_(_) (_) _(_)     (_)_
        (_) _  _  _ (_)(_)   (_)   (_)(_) _  _  _ (_)
        (_)(_)(_)(_)(_)(_)         (_)(_)(_)(_)(_)(_)
        (_)         (_)(_)         (_)(_)         (_)
        (_)         (_)(_)         (_)(_)         (_)
        """,
                r"""
              {_       {__       {__      {_
             {_ __     {_ {__   {___     {_ __
            {_  {__    {__ {__ { {__    {_  {__
           {__   {__   {__  {__  {__   {__   {__
          {______ {__  {__   {_  {__  {______ {__
         {__       {__ {__       {__ {__       {__
        {__         {__{__       {__{__         {__
        """,
        ]

        cls.tips = [
            f"""
        Select a module using its index {color('use ' + color('INDEX', style=Style.BRIGHT), fore=Fore.GREEN)} , instead of use its fullname.
        e.g. To select {color('auxiliary/passwords/password_generator', style=Style.BRIGHT)} module

        ama > search module -t aux -s pass
        +---+--------------------------------------+-----------------------------------------------+
        | # |                Module                |                    Summary                    |
        +---+--------------------------------------+-----------------------------------------------+
        | 0 | auxiliary/password/passord_generator |           Strong password generator           |
        | 1 |  auxiliary/password/passord_shuffle  | Strong password generator - shuffle passwords |
        +---+--------------------------------------+-----------------------------------------------+

        ama > {color('use 0', fore=Fore.GREEN, style=Style.BRIGHT)}
        """,
            f"""
        Use {color('search files', fore=Fore.GREEN)} to set a variable with several files.
        e.g. {color('search files /usr/share/seclists/Passwords -p ssh -r -i --set WORDLIST', fore=Fore.GREEN, style=Style.BRIGHT)}
        """,
            f"""
        Use {color('back -m', fore=Fore.GREEN)} command to interact with previous module
        """,
            f"""
        Use {color('unset VARIABLE', fore=Fore.GREEN)} command to unset the value of a variable
        e.g. {color('unset WORDLIST', fore=Fore.GREEN, style=Style.BRIGHT)}
        """,
            f"""
        To get help about a command, use {color('help COMMAND', fore=Fore.GREEN)} command or add {color('--help', fore=Fore.GREEN)} flag to the command.
        e.g. {color('help back', fore=Fore.GREEN, style=Style.BRIGHT)} or {color('back --help', fore=Fore.GREEN, style=Style.BRIGHT)}
        """,
            f"""
        Use the command {color('setv VARIABLE VALUE', fore=Fore.GREEN)} to set a variable with a value.
        e.g. {color('setv WORDLIST /usr/share/wordlists/rockyou.txt', fore=Fore.GREEN, style=Style.BRIGHT)}
        """,
            f"""
        Use the command {color('setvg VARIABLE VALUE', fore=Fore.GREEN)} to set a variable globally.
        e.g. {color('setvg HASHES_FILE shadow.hash', fore=Fore.GREEN, style=Style.BRIGHT)}
        """,
            f"""
        Check the tips, using {color('tips', fore=Fore.GREEN)} command, to quickly start using Ama-Framework.
        """,
            f"""
        Use {color('execute', fore=Fore.GREEN)} command to execute the active module.
        """,
            f"""
        Use {color('search module', fore=Fore.GREEN)} command to search availables modules
        e.g. To search an auxiliary module filtering its name with {color('gen', style=Style.BRIGHT)} pattern

        {color('search module -t auxiliary -n gen', fore=Fore.GREEN, style=Style.BRIGHT)}
        """
        ]

        _instance = super(BannerGenerator, cls).__new__(cls)

        return _instance


    @classmethod
    def modules_summary(cls) -> str:
        summary: str = None
        # modules_enum = cls.module_pool.modules.enum()
        # ama_modules = []
        # for mtype, mstype_enum in modules_enum.items():
        #     submodules_enum = []
        #     total_count = 0
        #     for mstype, count in mstype_enum.items():
        #         total_count += count
        #         submodules_enum.append(f"{count} {mstype}")

        #     ama_modules.append(
        #         f"\t[{total_count} {color(mtype, fore=Fore.RED)} : "
        #         f"{' - '.join(submodules_enum)}]"
        #     )

        # summary = '\n'.join(ama_modules)
        return summary


    def plugins_summary(cls) -> str:
        summary: str = None
        return summary

    @classmethod
    def extensions_summary(cls) -> Dict[str, int]:
        stats = {
            'extensions_count': 0,
            'injected_cmds': 0
        }

        for name, ext in cls._cmd.extensions.items():
            stats['extensions_count'] += 1
            stats['injected_cmds'] += commands_count(ext)

        return stats

    @classmethod
    def random(cls) -> str:
        """
        Generate a random banner
        """
        banner = random.choice(cls.banners)
        modules_summary = cls.modules_summary()
        plugins_summary = cls.modules_summary()
        extensions_summary = cls.extensions_summary()

        ama_versions = cls._cmd._get_ama_component_versions()

        for component, version in ama_versions.items():
            ama_versions[component] = color(version, fore=Fore.CYAN)

        return (
            f"""
        {banner}
    {cls.ama_info}

        COMPONENTS:
            amacore       : {ama_versions['amacore']}
            amaconsole    : {ama_versions['amaconsole']}
            amaproto      : {ama_versions['amaproto']}
            amacontroller : {ama_versions['amacontroller']}
            amadb         : {ama_versions['amadb']}

    {color('Modules:', style=Style.BRIGHT)}
{modules_summary}

    {color('Plugins:', style=Style.BRIGHT)}
{plugins_summary}

    {color('Command extensions:', style=Style.BRIGHT)}
            Extensions        : {extensions_summary['extensions_count']}
            Injected commands : {extensions_summary['injected_cmds']}
            """
        )
