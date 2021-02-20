
import curses
from curses import wrapper
from curses.textpad import Textbox, rectangle

cur_pos = 2
wsize = 10
hsize = 2
titles = []
curtab = -1

def delete_tab():
    global curtab
    titles.pop(curtab)
    curtab -= 1


def add_new_tab():
    global curtab
    titles.append(f"Panel")
    curtab += 1

def print_all_tabs(stdscr):
    global cur_pos
    global titles
    cur_pos = 0

    stdscr.clear()
    for idx, tab in enumerate(titles):
        print_tab(stdscr, tab, idx == curtab)
    stdscr.refresh()

def print_tab(stdscr, name, active):
    global cur_pos
    global titles
    uly = 0
    ulx = cur_pos
    lry = hsize
    lrx = cur_pos + wsize
    rectangle(stdscr, uly, ulx, lry, lrx)

    stdscr.addstr(uly+1, cur_pos + 1, f"{name}", curses.color_pair(active)) # {uly} {ulx} {lry} {lrx}")

    # box = Textbox(win)

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
    # stdscr.addstr(0, 0, "New Title: (hit Ctrl-G to send)")

    curses.curs_set(1)
    editwin = curses.newwin(1,wsize - 1, 1, curtab*(wsize+1) + 1)

    stdscr.refresh()


    box = Textbox(editwin)
    box.edit()
    curses.curs_set(0)

    # Get resulting contents
    message = box.gather()
    titles[curtab] = message



def main(stdscr):
    # stdscr.addstr(0, 0, "Enter IM message: (hit Ctrl-G to send)")
    stdscr.keypad(True)
    curses.init_pair(1, curses.COLOR_RED, curses.COLOR_WHITE)
    key = ''
    while key != ord('q'):
        print_all_tabs(stdscr)
        stdscr.refresh()
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





if __name__ == "__main__":
    cur_pos = 0

    curses.initscr()
    curses.cbreak()
    curses.noecho()
    curses.curs_set(0)


    wrapper(main)
    curses.endwin()
