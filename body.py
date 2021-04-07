import curses
import re
import tab

import colors
import globvar


def print_body(scroll):
    """Print body text"""
    win = curses.newwin(curses.LINES - 3, curses.COLS, 3, 0)
    win.scrollok(True)

    if scroll == 0:
        # No scroll set. Get the whole text
        text = globvar.pristine.get_main()
    else:
        text = globvar.pristine.get_main()[:-scroll]

    if tab.get_idx() < 0:
        raise Exception("Something goes wrong with tabs")

    word = tab.titles[tab.get_idx()].grep
    case_sensitive = tab.titles[tab.get_idx()].case_sensitive

    if case_sensitive:
        word = word.upper()

    for line in text:
        # Not grep word selected
        if not word:
            win.addstr(line)
            continue

        if case_sensitive:
            line_ = line.upper()
        else:
            line_ = line

        if word in line_:
            parts = re.split(f"({word}|[()])", line)
            for part in parts:
                if word == part:
                    color = curses.color_pair(colors.COLOR_WORD_FOUND)
                    win.addstr(part, color)
                else:
                    win.addstr(part)
            continue

    win.refresh()
