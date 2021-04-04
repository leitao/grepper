# refresh timeout
TIMEOUT = 100

def set_screen_defaults(stdscr):
    stdscr.keypad(True)
    # Block TIMEOUT ms (100 ms)
    stdscr.timeout(TIMEOUT)
