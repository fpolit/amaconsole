#!/usr/bin/env python3

import re
import cmd2
from datetime import timedelta

def str2timedelta(stime: str) -> timedelta:
    """
    Parse a string witht the form (AhBmCs : A hours + B minutes + C seconds) and generate
    a timedelta object
    """

    try:
        hours, mins, secs = re.search(r'(\d*h)?(\d*m)?(\d*s)?', stime).groups()
        tdelta = {}
        if hours:
            tdelta_hours = int(hours[:-1])
            if tdelta_hours > 0:
                tdelta["hours"] = tdelta_hours
        if mins:
            tdelta_mins = int(mins[:-1])
            if tdelta_mins > 0:
                tdelta["minutes"] = tdelta_mins
        if secs:
            tdelta_secs = int(secs[:-1])
            if tdelta_secs > 0:
                tdelta["seconds"] = tdelta_secs

        return timedelta(**tdelta)

    except Exception as error:
        print(error)

def commands_count(extension:cmd2.CommandSet) -> int:
    cmds_count = 0
    for attribute in dir(extension):
        if attribute.startswith('do_') and callable(getattr(extension, attribute)):
            cmds_count += 1

    return cmds_count
