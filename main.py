import threading
from curses import wrapper
import sys

# Project files
import colors
import goto
import header
import popup
import body
from defaults import set_screen_defaults
from file_ingestion import ingest_from_file
import help
import tab
import move
import profile
from colors import *
import globvar


def draw_screen(stdscr):
    if globvar.clear_screen:
        stdscr.clear()
        globvar.clear_screen = False

    # Print Header
    header.print_all_tabs(stdscr)
    # Print body
    body.print_body()

    # And refresh screen
    stdscr.refresh()


def set_scroll(param):
    current = tab.get_current_tab()
    length_min = curses.LINES - 4

    current.scroll += param

    if current.scroll < 0:
        current.scroll = 0

    globvar.redraw = True


def main(stdscr):
    set_screen_defaults(stdscr)

    # Add initial tab
    tab.add_new_tab()
    globvar.redraw = True

    key = ''

    while key != ord('q') and globvar.quitting is False:
        if globvar.redraw:
            draw_screen(stdscr)
            globvar.redraw = False

        key = stdscr.getch()
        if key == curses.ERR:
            continue

        if key == ord('a'):
            tab.add_new_tab()
        if key == ord('d'):
            tab.delete_tab()
        if key == ord('f'):
            popup.set_grep_word(stdscr)
        if key == ord('h'):
            help.show_help(stdscr)
        if key == ord('s'):
            # Save profile
            profile.save_profile(stdscr)
        if key == ord('l'):
            # Load profile
            profile.load_profile(stdscr)
        if key == ord('*'):
            # highlight another word
            popup.highlight(stdscr)
        if key == ord('?'):
            # highlight another word
            goto.goto_backward(stdscr)
        if key == ord('p'):
            tab.get_current_tab().toggle_pause()
        if key == curses.KEY_LEFT:
            move.move_left()
        if key == curses.KEY_RIGHT:
            move.move_right()
        if key == curses.KEY_UP:
            set_scroll(1)
        if key == curses.KEY_DOWN:
            set_scroll(-1)
        if key == curses.KEY_PPAGE:
            set_scroll(10)
        if key == curses.KEY_NPAGE:
            set_scroll(-10)
        if key == curses.KEY_HOME:
            # size of the window
            goto.scroll_to_top()
        KEY_ENTER = 10
        if key == KEY_ENTER or key == curses.KEY_END:
            goto.scroll_to_bottom()

    globvar.quitting = True


if __name__ == "__main__":
    if len(sys.argv) < 2:
        help.usage()
        sys.exit(1)

    profile = sys.argv[2:] or []
    if len(profile) == 2 and profile[0] == '-f':
        profile.load_profile_from_file(profile[1])

    curses.initscr()
    curses.start_color()

    curses.cbreak()
    curses.noecho()
    curses.curs_set(0)

    colors.set_colors()

    threads = threading.Thread(target=ingest_from_file, args=(sys.argv[1],))
    # x = threading.Thread(target=ingest_from_stdin)
    threads.start()

    try:
        wrapper(main)
    except KeyboardInterrupt:
        # Let the other thread exist also
        globvar.quitting = True

    # Wait for the ingestor thread
    threads.join()

    curses.endwin()
