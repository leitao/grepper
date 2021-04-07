import curses
from curses.textpad import Textbox, rectangle

def get_input(stdscr, text):
    global clear_screen
    global redraw
    clear_screen = True
    redraw = True

    # Enable cursor
    curses.curs_set(1)

    # Add a window on top of the current title
    mid_x = int(curses.LINES / 2)
    mid_y = int(curses.COLS / 2) - 20
    editwin = curses.newwin(1, 20, mid_x, mid_y)
    rectangle(stdscr, mid_x - 1, mid_y - 1, mid_x + 1, mid_y + 30)
    stdscr.addstr(mid_x - 1, mid_y + 2, text)

    stdscr.refresh()
    box = Textbox(editwin)
    # Edit it up to wsize -1
    box.edit()

    # Disable cursor again
    curses.curs_set(0)
    return box.gather().strip()
