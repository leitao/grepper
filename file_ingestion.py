import time

import globvar
import os


def ingest_text(s):
    globvar.pristine.ingest(s)


def ingest_from_file(filename):
    last_check = os.stat(filename).st_mtime
    parse_file(filename)
    while not globvar.quitting:
        new_time = os.stat(filename).st_mtime
        if new_time != last_check:
            last_check = new_time
            parse_file(filename)
        time.sleep(globvar.file_refresh_ms / 1000)


def reset_buffer(buffer):
    globvar.pristine.reset(buffer)
    globvar.redraw = True


def parse_file(filename):
    buffer = []
    try:
        with open(filename) as f:
            for line in f:
                buffer.append(line)
                if globvar.quitting:
                    return
    except IOError:
        print("File not found")
        globvar.quitting = True
        return

    reset_buffer(buffer)
