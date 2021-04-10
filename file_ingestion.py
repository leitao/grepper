import pathlib
import time

import globvar


def ingest_text(s):
    globvar.pristine.ingest(s)


def ingest_from_file(filename):
    try:
        with open(filename) as f:
            for line in f:
                ingest_text(line)
                if globvar.quitting:
                    return
    except IOError:
        print("File not found")
        globvar.quitting = True
        return
