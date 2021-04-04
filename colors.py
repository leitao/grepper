import curses

# Color names
COLOR_INSENSITIVE_NOT_SELECTED = 1
COLOR_INSENSITIVE_SELECTED = 2
COLOR_SENSITIVE_SELECTED = 3
COLOR_SENSITIVE_NOT_SELECTED = 4
COLOR_STOPPED = 5
COLOR_WORD_FOUND = 6


def set_colors():
    curses.init_pair(COLOR_STOPPED, curses.COLOR_RED, curses.COLOR_BLACK)

    # Case insenstive and no selected
    curses.init_pair(COLOR_INSENSITIVE_NOT_SELECTED, curses.COLOR_BLUE, curses.COLOR_BLACK)
    # Case insenstive and selected
    curses.init_pair(COLOR_INSENSITIVE_SELECTED, curses.COLOR_BLUE, curses.COLOR_WHITE)
    # Case senstive and not selected
    curses.init_pair(COLOR_SENSITIVE_NOT_SELECTED, curses.COLOR_GREEN, curses.COLOR_BLACK)
    # Case senstive and selected
    curses.init_pair(COLOR_SENSITIVE_SELECTED, curses.COLOR_GREEN, curses.COLOR_WHITE)
    # In the body
    curses.init_pair(COLOR_WORD_FOUND, curses.COLOR_RED, curses.COLOR_BLACK)
