import pathlib
import time

import globvar


def ingest_text(s):
    globvar.pristine.ingest(s)

def ingest_from_file(filename):
    with open(filename) as f:
        for line in f:
            time.sleep(.05)
            ingest_text(line)
            if globvar.quitting:
                return
