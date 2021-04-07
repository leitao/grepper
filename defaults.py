import globvar

def set_screen_defaults(stdscr):
    stdscr.keypad(True)
    # Block TIMEOUT ms (100 ms)
    stdscr.timeout(globvar.TIMEOUT)
