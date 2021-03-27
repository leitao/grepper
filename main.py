
import curses
import threading
from curses import wrapper
from curses.textpad import Textbox, rectangle
import time
import sys
import pathlib

cur_pos = 2
wsize = 15
hsize = 2
titles = []
curtab = -1
quitting = False
EOF = False
clear_screen = False
redraw = True


# refresh timeout
TIMEOUT = 100

class Buffer:
    global redraw
    # Main buffer
    main_buffer = []
    # Buffer when the ingestion is paused
    tmp = []

    paused = False
    consumable = False

    def pause(self):
        global redraw
        self.paused = True
        redraw = True

    def unpause(self):
        global clear_screen
        global redraw

        self.paused = False

        if self.tmp:
            self.main_buffer = self.main_buffer + self.tmp
            self.tmp = []
        self.consumable = True
        clear_screen = True
        redraw = True

    def ingest(self, line):
        global redraw
        if not self.paused:
            self.main_buffer.append(line)
            self.consumable = True
            redraw = True
        else:
            self.tmp.append(line)

    def get_main(self):
        self.consumable = False
        return self.main_buffer

# Ingestion Buffer
pristine = Buffer()


class Tab:
    name = ""
    buffer = []
    grep = ""
    case_sensitive = True
    i = 0

    def __init__(self, title):
        self.name = title

    # def ingest_into_tab(self, string: str):
    #     if not self.grep:
    #         self.buffer.append(f" {self.name}: {self.i}: " + string)
    #     elif self.grep in string:
    #         self.buffer.append(string)
    #     self.i += 1



def delete_tab():
    global curtab
    global clear_screen
    global redraw

    clear_screen = True
    redraw = True


    if curtab > 0:
        titles.pop(curtab)
        curtab -= 1

def add_new_tab():
    global curtab
    global redraw

    redraw = True
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
    if (tab.case_sensitive and active):
        color = curses.color_pair(COLOR_SENSITIVE_SELECTED)
    elif (tab.case_sensitive and not active):
        color = curses.color_pair(COLOR_SENSITIVE_NOT_SELECTED)
    elif (not tab.case_sensitive and active):
        color = curses.color_pair(COLOR_INSENSITIVE_SELECTED)
    elif (not tab.case_sensitive and not active):
        color = curses.color_pair(COLOR_INSENSITIVE_NOT_SELECTED)
    else:
        raise Exception("no color selected")

    # if tab.case_sensitive:
    # else:
    #     color = curses.color_pair(case_insensitive)
    stdscr.addstr(uly+1, cur_pos + 1, f"{title}", color)
    cur_pos += wsize + 1

    if pristine.paused:
        stdscr.addstr(uly+1, curses.COLS - 10, f"PAUSED", curses.color_pair(COLOR_STOPPED))


def move_left():
    global curtab
    global clear_screen
    global redraw

    clear_screen = True
    redraw = True

    curtab -= 1
    if (curtab < 0):
        curtab = 0


def move_right():
    global curtab
    global clear_screen
    global redraw

    clear_screen = True
    redraw = True
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
    stdscr.clear()

def print_text_box(scroll):
    global curtab
    global pristine
    global titles

    win = curses.newwin(curses.LINES - 3, curses.COLS, 3, 0)
    win.scrollok(True)

    if scroll == 0:
        # No scroll set. Get the whole text
        text = pristine.get_main()
    else:
        text = pristine.get_main()[:-scroll]

    word = titles[curtab].grep
    case_sensitive = titles[curtab].case_sensitive

    if (case_sensitive):
        word = word.upper()

    for line in text:
        if curtab < 0:
            # Dump the whole text
            win.addstr(line)
            continue

        # Not grep word selected
        if not word:
            win.addstr(line)
            continue

        if (case_sensitive):
            line_ = line.upper()
        else:
            line_ = line

        if word in line_:
            win.addstr(line)
            continue


    win.refresh()


def ingest_text(s):
    global pristine

    pristine.ingest(s)

def help(stdscr):
    pristine.pause()
    mid_x = 4 # int(curses.LINES/2) - 15
    mid_y = int(curses.COLS/2) - 15

    stdscr.clear()
    stdscr.refresh()
    editwin = curses.newwin(mid_x, mid_y, mid_x+10, mid_y + 40)
    rectangle(stdscr, mid_x, mid_y, mid_x+10, mid_y + 40)
    stdscr.addstr(mid_x, mid_y + 13, "Help")
    stdscr.addstr(mid_x + 1, mid_y + 2, "a   -   Add a new Tab")
    stdscr.addstr(mid_x + 2, mid_y + 2, "c   -   Toggle case sensitive search")
    stdscr.addstr(mid_x + 3, mid_y + 2, "d   -   Delete Tab")
    stdscr.addstr(mid_x + 4, mid_y + 2, "p   -   Pause")
    stdscr.addstr(mid_x + 5, mid_y + 2, "/   -   Toggle case sensitive search")
    stdscr.addstr(mid_x + 6, mid_y + 2, "e   -   Edit the tab name")
    stdscr.addstr(mid_x + 9, mid_y + 2, "Home, Page UP, Page Down works also")
    stdscr.refresh()
    stdscr.timeout(-1)
    stdscr.getch()
    stdscr.timeout(TIMEOUT)


# Set find word
def set_find(stdscr):
    global clear_screen
    global redraw
    clear_screen = True
    redraw = True

    # Enable cursor
    curses.curs_set(1)

    # Add a window on top of the current title
    mid_x = int(curses.LINES/2)
    mid_y = int(curses.COLS/2) - 20
    editwin = curses.newwin(1, 20, mid_x, mid_y)
    rectangle(stdscr, mid_x - 1, mid_y -1, mid_x+1, mid_y + 30)
    stdscr.addstr(mid_x -1, mid_y + 2, "Grep for")

    stdscr.refresh()
    box = Textbox(editwin)
    # Edit it up to wsize -1
    box.edit()

    # Disable cursor again
    curses.curs_set(0)

    # Get resulting contents
    word = box.gather()
    titles[curtab].grep = word.strip()
    titles[curtab].name = word.strip()


def draw_screen(stdscr, scroll):
    global clear_screen

    if not hasattr(draw_screen, "scroll"):
        draw_screen.scroll = 0

    draw_screen.scroll += scroll

    if clear_screen:
        stdscr.clear()
        clear_screen = False

    # No scroll set anymore. Let the test run
    if draw_screen.scroll <= 0:
        draw_screen.scroll = 0
        # pristine.unpause()
    else:
        pristine.pause()


    print_all_tabs(stdscr)
    print_text_box(draw_screen.scroll)
    stdscr.refresh()

def scroll_text(stdscr, lines):
    if draw_screen.scroll <= 0:
        pristine.unpause()
    draw_screen(stdscr, lines)


def main(stdscr):
    global quitting
    global redraw
    global clear_screen
    stdscr.keypad(True)
    # Block TIMEOUT ms (100 ms)
    stdscr.timeout(TIMEOUT)
    stdscr.getch()



# Set find word
def set_find(stdscr):
    global clear_screen
    global redraw
    clear_screen = True
    redraw = True

    # Enable cursor
    curses.curs_set(1)

    # Add a window on top of the current title
    mid_x = int(curses.LINES/2)
    mid_y = int(curses.COLS/2) - 20
    editwin = curses.newwin(1, 20, mid_x, mid_y)
    rectangle(stdscr, mid_x - 1, mid_y -1, mid_x+1, mid_y + 30)
    stdscr.addstr(mid_x -1, mid_y + 2, "Grep for")

    stdscr.refresh()
    box = Textbox(editwin)
    # Edit it up to wsize -1
    box.edit()

    # Disable cursor again
    curses.curs_set(0)

    # Get resulting contents
    word = box.gather()
    titles[curtab].grep = word.strip()
    titles[curtab].name = word.strip()


def draw_screen(stdscr, scroll):
    global clear_screen

    if not hasattr(draw_screen, "scroll"):
        draw_screen.scroll = 0

    draw_screen.scroll += scroll

    if clear_screen:
        stdscr.clear()
        clear_screen = False

    # static variable

    # No scroll set anymore. Let the test run
    if draw_screen.scroll <= 0:
        draw_screen.scroll = 0
        # pristine.unpause()
    else:
        pristine.pause()


    print_all_tabs(stdscr)
    print_text_box(draw_screen.scroll)
    stdscr.refresh()

def scroll_text(stdscr, lines):
    if draw_screen.scroll <= 0:
        pristine.unpause()
    draw_screen(stdscr, lines)


def main(stdscr):
    global quitting
    global redraw
    global clear_screen
    stdscr.keypad(True)
    # Block TIMEOUT ms (100 ms)
    stdscr.timeout(TIMEOUT)
    stdscr.getch()


# Set find word
def set_find(stdscr):
    global clear_screen
    global redraw
    clear_screen = True
    redraw = True

    # Enable cursor
    curses.curs_set(1)

    # Add a window on top of the current title
    mid_x = int(curses.LINES/2)
    mid_y = int(curses.COLS/2) - 20
    editwin = curses.newwin(1, 20, mid_x, mid_y)
    rectangle(stdscr, mid_x - 1, mid_y -1, mid_x+1, mid_y + 30)
    stdscr.addstr(mid_x -1, mid_y + 2, "Grep for")

    stdscr.refresh()
    box = Textbox(editwin)
    # Edit it up to wsize -1
    box.edit()

    # Disable cursor again
    curses.curs_set(0)

    # Get resulting contents
    word = box.gather()
    titles[curtab].grep = word.strip()
    titles[curtab].name = word.strip()


def draw_screen(stdscr, scroll):
    global clear_screen

    if not hasattr(draw_screen, "scroll"):
        draw_screen.scroll = 0

    draw_screen.scroll += scroll

    if clear_screen:
        stdscr.clear()
        clear_screen = False

    # No scroll set anymore. Let the test run
    if draw_screen.scroll <= 0:
        draw_screen.scroll = 0
        # pristine.unpause()
    else:
        pristine.pause()


    print_all_tabs(stdscr)
    print_text_box(draw_screen.scroll)
    stdscr.refresh()

def scroll_text(stdscr, lines):
    if draw_screen.scroll <= 0:
        pristine.unpause()
    draw_screen(stdscr, lines)


def main(stdscr):
    global quitting
    global redraw
    global clear_screen
    stdscr.keypad(True)
    # Block TIMEOUT ms (100 ms)
    stdscr.timeout(TIMEOUT)
    stdscr.getch()


# Set find word
def set_find(stdscr):
    global clear_screen
    global redraw
    clear_screen = True
    redraw = True

    # Enable cursor
    curses.curs_set(1)

    # Add a window on top of the current title
    mid_x = int(curses.LINES/2)
    mid_y = int(curses.COLS/2) - 20
    editwin = curses.newwin(1, 20, mid_x, mid_y)
    rectangle(stdscr, mid_x - 1, mid_y -1, mid_x+1, mid_y + 30)
    stdscr.addstr(mid_x -1, mid_y + 2, "Grep for")

    stdscr.refresh()
    box = Textbox(editwin)
    # Edit it up to wsize -1
    box.edit()

    # Disable cursor again
    curses.curs_set(0)

    # Get resulting contents
    word = box.gather()
    titles[curtab].grep = word.strip()
    titles[curtab].name = word.strip()


def draw_screen(stdscr, scroll):
    global clear_screen

    if not hasattr(draw_screen, "scroll"):
        draw_screen.scroll = 0

    draw_screen.scroll += scroll

    if clear_screen:
        stdscr.clear()
        clear_screen = False

    # static variable

    # No scroll set anymore. Let the test run
    if draw_screen.scroll <= 0:
        draw_screen.scroll = 0
        # pristine.unpause()
    else:
        pristine.pause()


    print_all_tabs(stdscr)
    print_text_box(draw_screen.scroll)
    stdscr.refresh()

def scroll_text(stdscr, lines):
    if draw_screen.scroll <= 0:
        pristine.unpause()
    draw_screen(stdscr, lines)


def main(stdscr):
    global quitting
    global redraw
    global clear_screen
    stdscr.keypad(True)
    # Block TIMEOUT ms (100 ms)
    stdscr.timeout(TIMEOUT)
    stdscr.getch()


# Set find word
def set_find(stdscr):
    global clear_screen
    global redraw
    clear_screen = True
    redraw = True

    # Enable cursor
    curses.curs_set(1)

    # Add a window on top of the current title
    mid_x = int(curses.LINES/2)
    mid_y = int(curses.COLS/2) - 20
    editwin = curses.newwin(1, 20, mid_x, mid_y)
    rectangle(stdscr, mid_x - 1, mid_y -1, mid_x+1, mid_y + 30)
    stdscr.addstr(mid_x -1, mid_y + 2, "Grep for")

    stdscr.refresh()
    box = Textbox(editwin)
    # Edit it up to wsize -1
    box.edit()

    # Disable cursor again
    curses.curs_set(0)

    # Get resulting contents
    word = box.gather()
    titles[curtab].grep = word.strip()
    titles[curtab].name = word.strip()


def draw_screen(stdscr, scroll):
    global clear_screen

    if not hasattr(draw_screen, "scroll"):
        draw_screen.scroll = 0

    draw_screen.scroll += scroll

    if clear_screen:
        stdscr.clear()
        clear_screen = False

    # static variable

    # No scroll set anymore. Let the test run
    if draw_screen.scroll <= 0:
        draw_screen.scroll = 0
        # pristine.unpause()
    else:
        pristine.pause()


    print_all_tabs(stdscr)
    print_text_box(draw_screen.scroll)
    stdscr.refresh()

def scroll_text(stdscr, lines):
    if draw_screen.scroll <= 0:
        pristine.unpause()
    draw_screen(stdscr, lines)


def main(stdscr):
    global quitting
    global redraw
    global clear_screen
    stdscr.keypad(True)
    # Block TIMEOUT ms (100 ms)
    stdscr.timeout(TIMEOUT)
    stdscr.getch()


# Set find word
def set_grep_word(stdscr):
    global clear_screen
    global redraw
    clear_screen = True
    redraw = True

    # Enable cursor
    curses.curs_set(1)

    # Add a window on top of the current title
    mid_x = int(curses.LINES/2)
    mid_y = int(curses.COLS/2) - 20
    editwin = curses.newwin(1, 20, mid_x, mid_y)
    rectangle(stdscr, mid_x - 1, mid_y -1, mid_x+1, mid_y + 30)
    stdscr.addstr(mid_x -1, mid_y + 2, "Grep for")

    stdscr.refresh()
    box = Textbox(editwin)
    # Edit it up to wsize -1
    box.edit()

    # Disable cursor again
    curses.curs_set(0)

    # Get resulting contents
    word = box.gather()
    titles[curtab].grep = word.strip()
    titles[curtab].name = word.strip()


def draw_screen(stdscr, scroll):
    global clear_screen

    if not hasattr(draw_screen, "scroll"):
         draw_screen.scroll = 0

    draw_screen.scroll += scroll

    if clear_screen:
        stdscr.clear()
        clear_screen = False

    # static variable

    # No scroll set anymore. Let the test run
    if draw_screen.scroll <= 0:
        draw_screen.scroll = 0
        # pristine.unpause()
    else:
        pristine.pause()


    print_all_tabs(stdscr)
    print_text_box(draw_screen.scroll)
    stdscr.refresh()

def scroll_text(stdscr, lines):
    if draw_screen.scroll <= 0:
        pristine.unpause()
    draw_screen(stdscr, lines)


def main(stdscr):
    global quitting
    global redraw
    global clear_screen
    stdscr.keypad(True)
    # Block TIMEOUT ms (100 ms)
    stdscr.timeout(TIMEOUT)

    key = ''

    # Add initial tab
    add_new_tab()
    while key != ord('q'):
        if redraw:
            draw_screen(stdscr, 0)
            redraw = False

        key = stdscr.getch()
        if key == curses.ERR:
            continue

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
            set_grep_word(stdscr)
        if key == curses.KEY_UP:
            scroll_text(stdscr, 1)
        if key == curses.KEY_DOWN:
            scroll_text(stdscr, -1)
        if key == curses.KEY_PPAGE:
            scroll_text(stdscr, 10)
        if key == ord('?') or key == ord('h'):
            help(stdscr)
        if key == curses.KEY_NPAGE:
            scroll_text(stdscr, -10)
        if key == ord('c'):
            # Chance the case sensitive
            titles[curtab].case_sensitive = not titles[curtab].case_sensitive

        if key == curses.KEY_HOME:
            # size of the window
            scroll_text(stdscr, len(pristine.get_main()) - (curses.LINES - hsize - 2))

        KEY_ENTER = 10
        if key == KEY_ENTER or key == curses.KEY_END:
            draw_screen.scroll = 0
            pristine.unpause()

        if key == ord('p'):
            if not pristine.paused:
                pristine.pause()
            else:
                pristine.unpause()
                # Hack to go to the bottom of the text on unpause
                draw_screen.scroll = 0
                scroll_text(stdscr, -200)
        # else:
        #     print(f"Key = {key}")

    quitting = True


def ingest_from_file(filename):
    global quitting

    sec = 0
    file = pathlib.Path(filename)
    stat = file.stat()

    with open(filename) as f:
        for line in f:
            time.sleep(.05)
            ingest_text(line)
            if quitting:
                return

def usage():
    print("Multi tab grepper")
    print("Usage:")
    print(f"  {sys.argv[0]} <file to dump>")

COLOR_INSENSITIVE_NOT_SELECTED = 1
COLOR_INSENSITIVE_SELECTED = 2
COLOR_SENSITIVE_SELECTED = 3
COLOR_SENSITIVE_NOT_SELECTED = 4
COLOR_STOPPED = 5


if __name__ == "__main__":
    if len(sys.argv) < 2:
        usage()
        sys.exit(1)


    curses.initscr()

    curses.cbreak()
    curses.noecho()
    curses.curs_set(0)
    curses.start_color()
    curses.init_pair(COLOR_STOPPED, curses.COLOR_RED, curses.COLOR_BLACK)

    # Case insenstive and no selected
    curses.init_pair(COLOR_INSENSITIVE_NOT_SELECTED, curses.COLOR_BLUE, curses.COLOR_BLACK)
    # Case insenstive and selected
    curses.init_pair(COLOR_INSENSITIVE_SELECTED, curses.COLOR_BLUE, curses.COLOR_WHITE)
    # Case senstive and not selected
    curses.init_pair(COLOR_SENSITIVE_NOT_SELECTED, curses.COLOR_GREEN, curses.COLOR_BLACK)
    # Case senstive and selected
    curses.init_pair(COLOR_SENSITIVE_SELECTED, curses.COLOR_GREEN, curses.COLOR_WHITE)


    x = threading.Thread(target=ingest_from_file, args=(sys.argv[1],))
    # x = threading.Thread(target=ingest_from_stdin)
    x.start()

    try:
        wrapper(main)
    except KeyboardInterrupt:
        # Let the other thread exist also
        quitting = True

    x.join()

curses.endwin()