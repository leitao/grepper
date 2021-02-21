
import curses
import threading
from curses import wrapper
from curses.textpad import Textbox, rectangle
import time
import sys

cur_pos = 2
wsize = 15
hsize = 2
titles = []
curtab = -1
quitting = False
EOF = False

# refresh timeout
TIMEOUT = 100

class Buffer:
    # Main buffer
    main = []
    # Buffer when the ingestion is paused
    tmp = []

    paused = False

    def pause(self):
        self.paused = True

    def unpause(self):
        self.paused = False
        self.main = self.main + self.tmp
        self.tmp = []

    def ingest(self, line):
        if not self.paused:
            self.main.append(line)
        else:
            self.tmp.append(line)


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


# Ingestion Buffer
pristine = Buffer()


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


def print_text_box(scroll):
    global curtab
    global pristine
    global titles

    win = curses.newwin(curses.LINES - 3, curses.COLS, 3, 0)
    win.scrollok(True)

    for line in pristine.main:
        if (curtab < 0) or (titles[curtab].grep in line):
            win.addstr(line)


    win.refresh()


def ingest_text(s):
    global pristine

    pristine.ingest(s)


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


def draw_screen(stdscr, scroll):
    stdscr.clear()
    print_all_tabs(stdscr)
    print_text_box(scroll)
    stdscr.refresh()


def main(stdscr):
    global quitting
    stdscr.keypad(True)
    stdscr.timeout(TIMEOUT)

    key = ''

    # Add initial tab
    add_new_tab()
    pause = False
    scroll = 0
    while key != ord('q'):
        draw_screen(stdscr, scroll)
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
        if key == curses.KEY_UP:
            pristine.pause()
            scroll -= 1
        if key == curses.KEY_DOWN:
            pristine.pause()
            scroll += 1
            if scroll >= 0:
                pristine.unpause()
                scroll = 0
        if key == ord('p'):
            pause = not pause
            if pause:
                pristine.pause()
            else:
                pristine.unpause()

    quitting = True




def ingest_from_file():
    global quitting

    with open("a.txt") as f:
        for line in f:
            time.sleep(.05)
            ingest_text(line)
            if quitting:
                # The other thread stopped. Say goodbye
                return

def ingest_from_stdin():
    global quitting
    global EOF

    while True:
        line = sys.stdin.readline()

        if not line:
            debug()
            EOF = True
            quitting = True
            break
        ingest_text(line)

    # for line in sys.stdin:
    #     if not sys.stdin.readable():
    #         EOF = True
    #         debug()
    #     ingest_text(line)
    #     if quitting:
    #         # The other thread stopped. Say goodbye
    #         return





if __name__ == "__main__":

    curses.initscr()

    curses.cbreak()
    curses.noecho()
    curses.curs_set(0)
    curses.start_color()
    curses.init_pair(1, curses.COLOR_RED, curses.COLOR_WHITE)

    x = threading.Thread(target=ingest_from_file)
    # x = threading.Thread(target=ingest_from_stdin)
    x.start()

    try:
        wrapper(main)
    except Exception:
        # Let the other thread exist also
        quitting = True

    x.join()

curses.endwin()
