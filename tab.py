from curses.textpad import rectangle
from colors import *
from input import get_input

import globvar

wsize = 15
hsize = 2
titles = []
# index is the current index in the array. Tab 0 will be index 0
index = -1
cur_pos = 2


def get_idx():
    return index


def set_grep_word(stdscr):
    word = get_input(stdscr, "Grep for: ")
    titles[get_idx()].grep = word.strip()
    titles[get_idx()].name = word.strip()


def decrease_idx():
    global index
    if index > 0:
        index -= 1


def increase_idx():
    global index
    index += 1


def delete_tab():
    globvar.clear_screen = True
    globvar.redraw = True

    if len(titles) > 1:
        titles.pop(get_idx())
        decrease_idx()


def add_new_tab():
    globvar.redraw = True
    increase_idx()
    titles.append(Tab(globvar.unamed))


def print_all_tabs(stdscr):
    globvar.cur_pos = 0

    for idx, tab in enumerate(titles):
        print_tab(stdscr, tab, idx == get_idx())
    stdscr.refresh()


def print_tab(stdscr, tab, active):
    uly = 0
    ulx = globvar.cur_pos
    lry = hsize
    lrx = globvar.cur_pos + wsize
    if lrx >= curses.COLS:
        # No enough space in the x row
        return

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


def is_last_tab():
    if get_idx() == len(titles) - 1:
        return True
    return False


def move_left():
    globvar.clear_screen = True
    globvar.redraw = True

    # is the current tab the last one
    if is_last_tab() and titles[get_idx()].name == "Unfiltered":
        delete_tab()
        return

    # Just go left
    decrease_idx()


def move_right():
    globvar.clear_screen = True
    globvar.redraw = True

    # is the current tab the last one
    if is_last_tab():
        # add a new one
        add_new_tab()
        return

    # Just move
    increase_idx()


class Tab:
    def __init__(self, title):
        self.name = title
        self.grep = ""
        self.case_sensitive = True


def get_amount_tabs():
    return len(titles)
