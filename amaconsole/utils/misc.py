#!/usr/bin/env python3

import re
from datetime import timedelta

def str2timedelta(stime: str) -> timedelta:
    """
    Parse a string witht the form (AhBmCs : A hours + B minutes + C seconds) and generate
    a timedelta object
    """

    try:
        hours, mins, secs = re.search('(\d*h)?(\d*m)?(\d*s)?').groups()
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
