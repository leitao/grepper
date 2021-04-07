import curses
from curses.textpad import rectangle
from colors import *
from input import get_input

import globvar

wsize = 15
hsize = 2
titles = []
curtab = -1
cur_pos = 2

def set_grep_word(stdscr):
    word = get_input(stdscr, "Grep for: ")
    titles[curtab].grep = word.strip()
    titles[curtab].name = word.strip()

def delete_tab():
    global curtab
    globvar.clear_screen = True
    globvar.redraw = True

    if curtab > 0:
        titles.pop(curtab)
        curtab -= 1


def add_new_tab():
    global curtab
    globvar.redraw = True
    curtab += 1
    titles.append(Tab(f"Unfiltered"))


def print_all_tabs(stdscr):
    globvar.cur_pos = 0

    for idx, tab in enumerate(titles):
        print_tab(stdscr, tab, idx == curtab)
    stdscr.refresh()


def print_tab(stdscr, tab, active):
    uly = 0
    ulx = globvar.cur_pos
    lry = hsize
    lrx = globvar.cur_pos + wsize
    rectangle(stdscr, uly, ulx, lry, lrx)

    if tab.case_sensitive and active:
        color = curses.color_pair(COLOR_SENSITIVE_SELECTED)
    elif tab.case_sensitive and not active:
        color = curses.color_pair(COLOR_SENSITIVE_NOT_SELECTED)
    elif not tab.case_sensitive and active:
        color = curses.color_pair(COLOR_INSENSITIVE_SELECTED)
    elif not tab.case_sensitive and not active:
        color = curses.color_pair(COLOR_INSENSITIVE_NOT_SELECTED)
    else:
        raise Exception("no color selected")

    if not tab.case_sensitive:
        title = tab.name.lower()
    else:
        title = tab.name

    stdscr.addstr(uly + 1, globvar.cur_pos + 1, f"{title} ", color)
    globvar.cur_pos += wsize + 1

    if globvar.pristine.paused:
        stdscr.addstr(uly + 1, curses.COLS - 10, f"PAUSED", curses.color_pair(COLOR_STOPPED))


def move_left():
    global curtab
    globvar.clear_screen = True
    globvar.redraw = True

    curtab -= 1
    if curtab < 0:
        curtab = 0


def move_right():
    global curtab

    globvar.clear_screen = True
    globvar.redraw = True
    curtab += 1
    if curtab >= len(titles):
        globvar.curtab = len(titles) - 1


class Tab:
    def __init__(self, title):
        self.name = title
        self.grep = ""
        self.case_sensitive = True
