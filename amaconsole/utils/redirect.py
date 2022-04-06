#!/usr/bin/env python3
#
# redirect stdout to a file

import sys
from pathlib import Path


class FlushFile:
    def __init__(self, f):
        self.f = f

    def write(self, x):
        self.f.write(x)
        self.f.flush()

    def close(self):
        self.f.close()

class RedirectOutput:
    """
    Redirect stdout output to file
    """
    def __init__(self, filepath: Path, mode: str = 'w'):
        self.filepath = filepath
        self.mode = mode
        self.stdout = sys.stdout
        self.outfile = None

    def __enter__(self):
        out = open(self.filepath, self.mode, encoding='utf-8')
        self.outfile = FlushFile(out)
        sys.stdout = self.outfile

        return self

    def __exit__(self, exc_type, exc_value, exc_traceback):
        sys.stdout = self.stdout
        if self.outfile:
            self.outfile.close()
