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

    if tab.get_idx() < 0 or tab.get_idx() > tab.get_amount_tabs() - 1:
        raise Exception(f"Something goes wrong with tabs {tab.get_idx()} - {tab.get_idx()} | {tab.get_amount_tabs()}")

    current = tab.get_current_tab()
    # Word to highlight light
    word = current.grep
    # any additional word to highlight
    array_and_colors = [(word, colors.COLOR_ADDITIONAL_WORD_FOUND) for word in current.highlight]
    # Main word should come first
    if word:
        array_and_colors.insert(0, (word, colors.COLOR_WORD_FOUND))

    pb = PrintBuffer(array_and_colors)
    scroll = tab.get_current_tab().scroll

    # Grep from bottoms up (Performance)
    for line in reversed(globvar.pristine.get_main()):
        if word in line:
            pb.add(line)

        if pb.is_full(scroll):
            # Do not import more. Not going to display anyway
            break

    pb.print_all(win, scroll)
