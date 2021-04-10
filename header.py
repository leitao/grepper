import globvar
import curses
from curses.textpad import rectangle
from colors import *
import tab

wsize = 14
hsize = 2

def print_all_tabs(stdscr):
    globvar.cur_pos = 0

    for idx, current_tab in enumerate(tab.titles):
        print_tab(stdscr, current_tab.name, idx == tab.get_idx())

    stdscr.refresh()

def print_tab(stdscr, title, active):
    """Print a new tab in the header"""
    uly = 0
    ulx = globvar.cur_pos
    lry = hsize
    lrx = globvar.cur_pos + wsize

    if lrx >= curses.COLS:
        # No enough space in the x row
        return

    rectangle(stdscr, uly, ulx, lry, lrx)

    if active:
        color = curses.color_pair(COLOR_SENSITIVE_SELECTED)
    else:
        color = curses.color_pair(COLOR_SENSITIVE_NOT_SELECTED)

    stdscr.addstr(uly + 1, globvar.cur_pos + 1, f"{title} ", color)
    globvar.cur_pos += wsize + 1

    current = tab.get_current_tab()
    if current.paused:
        stdscr.addstr(uly + 1, curses.COLS - 10, f"PAUSED", curses.color_pair(COLOR_STOPPED))
