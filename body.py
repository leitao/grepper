import curses
import re
import tab

import colors
import globvar
from buffer import PrintBuffer


def print_body():
    """Print body text"""
    win = curses.newwin(curses.LINES - 3, curses.COLS, 3, 0)
    win.scrollok(True)

    # scroll = globvar.pristine.scroll
    text = globvar.pristine.get_main()

    if tab.get_idx() < 0 or tab.get_idx() > tab.get_amount_tabs() - 1:
        raise Exception(f"Something goes wrong with tabs {tab.get_idx()} - {tab.get_idx()} | {tab.get_amount_tabs()}")

    # Word to highlight light
    word = tab.titles[tab.get_idx()].grep
    # any additional word to highlight
    array_and_colors = [(word, colors.COLOR_ADDITIONAL_WORD_FOUND) for word in tab.titles[tab.get_idx()].highlight]
    # Main word should come first
    if word:
        array_and_colors.insert(0, (word, colors.COLOR_WORD_FOUND))

    pb = PrintBuffer(array_and_colors)

    # Grep from bottoms up (Performance)
    for line in reversed(text):
        if word in line:
            pb.add(line)

        if pb.full():
            break

    pb.print_all(win)
