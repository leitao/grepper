from curses.textpad import rectangle
import sys

def usage():
    print("Multi tab grepper")
    print("Usage:")
    print(f"  {sys.argv[0]} <file to dump> [-f <profile>]")

def help(stdscr):
    pristine.pause()
    mid_x = 4  # int(curses.LINES/2) - 15
    mid_y = int(curses.COLS / 2) - 15

    stdscr.clear()
    stdscr.refresh()
    rectangle(stdscr, mid_x, mid_y, mid_x + 10, mid_y + 40)
    stdscr.addstr(mid_x, mid_y + 13, "Help")
    stdscr.addstr(mid_x + 1, mid_y + 2, "a   -   Add a new Tab")
    stdscr.addstr(mid_x + 2, mid_y + 2, "c   -   Toggle case sensitive search")
    stdscr.addstr(mid_x + 3, mid_y + 2, "d   -   Delete Tab")
    stdscr.addstr(mid_x + 4, mid_y + 2, "p   -   Pause")
    stdscr.addstr(mid_x + 5, mid_y + 2, "/   -   Toggle case sensitive search")
    stdscr.addstr(mid_x + 6, mid_y + 2, "s   -   Save profile")
    stdscr.addstr(mid_x + 7, mid_y + 2, "l   -   Load profile")
    stdscr.addstr(mid_x + 9, mid_y + 2, "Home, Page UP, Page Down works also")
    stdscr.refresh()
    stdscr.timeout(-1)
    stdscr.getch()
    stdscr.timeout(TIMEOUT)
