
import curses
import threading
from curses import wrapper
from curses.textpad import Textbox, rectangle
import time

cur_pos = 2
wsize = 15
hsize = 2
titles = []
curtab = -1
# pristine input
pristine = []

# refresh timeout
TIMEOUT = 100

class Tab:
    name = ""
    buffer = []
    grep = ""
    i = 0

    def __init__(self, title):
        self.name = title

    def ingest(self, string: str):
        if not self.grep:
            self.buffer.append(f" {self.name}: {self.i}: " + string)
        elif self.grep in string:
            self.buffer.append(string)
        self.i += 1

        # debug()

def delete_tab():
    global curtab
    titles.pop(curtab)
    curtab -= 1

def add_new_tab():
    global curtab
    curtab += 1
    titles.append(Tab(f"Panel {curtab}"))

def print_all_tabs(stdscr):
    global cur_pos
    global titles
    cur_pos = 0

    for idx, tab in enumerate(titles):
        print_tab(stdscr, tab, idx == curtab)
    stdscr.refresh()

def print_tab(stdscr, tab, active):
    global cur_pos
    global titles
    uly = 0
    ulx = cur_pos
    lry = hsize
    lrx = cur_pos + wsize
    rectangle(stdscr, uly, ulx, lry, lrx)

    title = tab.name
    stdscr.addstr(uly+1, cur_pos + 1, f"{title}", curses.color_pair(active))

    cur_pos += wsize + 1


def move_left():
    global curtab
    curtab -= 1
    if (curtab < 0):
        curtab = 0


def move_right():
    global curtab
    curtab += 1
    if (curtab >= len(titles)):
        curtab = len(titles) - 1


def edit_title(stdscr):
    # Enable cursor
    curses.curs_set(1)

    # Add a window on top of the current title
    editwin = curses.newwin(1,wsize - 1, 1, curtab*(wsize+1) + 1)

    stdscr.refresh()
    box = Textbox(editwin)
    # Edit it up to wsize -1
    box.edit()

    # Disable cursor again
    curses.curs_set(0)

    # Get resulting contents
    message = box.gather()
    titles[curtab].name = message


def debug():
    import pdb
    curses.endwin()
    curses.endwin()
    pdb.set_trace()


def print_text_box():
    global curtab
    global pristine
    global titles

    win = curses.newwin(curses.LINES - 3, curses.COLS, 3, 0)
    win.scrollok(True)


    for line in pristine:
        # debug()
        # win.addstr(line)
        if (curtab < 0) or (titles[curtab].grep in line):
            win.addstr(line)
        # else:
        #     win.addstr(f"Not {titles[curtab].grep} : " + line)

    win.refresh()


def ingest_text(s):
    global pristine
    pristine.append(s)

# Set find word
def set_find(stdscr):
    # Enable cursor
    curses.curs_set(1)

    # Add a window on top of the current title

    editwin = curses.newwin(1,20, 10, 10)
    # editwin.addstr("Grep for: ")
    rectangle(stdscr, 9, 9, 11, 30)
    stdscr.addstr(9, 15, "Grep for")

    stdscr.refresh()
    box = Textbox(editwin)
    # Edit it up to wsize -1
    box.edit()

    # Disable cursor again
    curses.curs_set(0)

    # Get resulting contents
    word = box.gather()
    titles[curtab].grep = word.strip()


def draw_screen(stdscr):
    stdscr.clear()
    print_all_tabs(stdscr)
    print_text_box()
    stdscr.refresh()


def main(stdscr):
    stdscr.keypad(True)
    stdscr.timeout(TIMEOUT)

    key = ''

    while key != ord('q'):
        draw_screen(stdscr)

        # Block TIMEOUT ms (100 ms)
        key = stdscr.getch()

        if key == ord('a'):
            add_new_tab()
        if key == ord('d'):
            delete_tab()
        if key == curses.KEY_LEFT:
            move_left()
        if key == curses.KEY_RIGHT:
            move_right()
        if key == ord('e'):
            edit_title(stdscr)
        if key == ord('/'):
            set_find(stdscr)
        if key == ord('q'):
            break



def ingest_from_file():
    with open("a.txt") as f:
        for line in f:
            time.sleep(.2)
            ingest_text(line)


if __name__ == "__main__":

    curses.initscr()

    curses.cbreak()
    curses.noecho()
    curses.curs_set(0)
    curses.start_color()
    curses.init_pair(1, curses.COLOR_RED, curses.COLOR_WHITE)

    x = threading.Thread(target=ingest_from_file)
    x.start()

    wrapper(main)

    x.join()

curses.endwin()
