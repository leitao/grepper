import threading
from curses import wrapper
import sys

# Project files
import colors
from body import print_body
from defaults import set_screen_defaults
from file_ingestion import ingest_from_file
from help import usage, show_help
import tab
from profiles import *
from colors import *
import globvar


# def scroll_text(stdscr):
#     if draw_screen.scroll <= 0:
#         globvar.pristine.unpause()
#     draw_screen(stdscr)


def draw_screen(stdscr):
    if globvar.clear_screen:
        stdscr.clear()
        globvar.clear_screen = False

    tab.print_all_tabs(stdscr)
    print_body()
    stdscr.refresh()


def scroll_to_zero():
    globvar.pristine.goto_home()
    globvar.redraw = True


def set_scroll(param):
    globvar.pristine.scroll += param

    if globvar.pristine.scroll < 0:
        globvar.pristine.scroll = 0
    if globvar.pristine.scroll > globvar.pristine.len():
        globvar.pristine.scroll = globvar.pristine.len()

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
            tab.set_grep_word(stdscr)
        if key == ord('?') or key == ord('h'):
            show_help(stdscr)
        if key == ord('s'):
            # Save profile
            save_profile(stdscr)
        if key == ord('l'):
            # Load profile
            load_profile(stdscr)
        if key == ord('*'):
            # highlight another word
            tab.highlight(stdscr)
        if key == ord('/'):
            # highlight another word
            tab.goto(stdscr)
        if key == ord('p'):
            if not globvar.pristine.paused:
                globvar.pristine.pause()
            else:
                globvar.pristine.unpause()
                # Hack to go to the bottom of the text on unpause
                globvar.pristine.scroll = 0
        if key == curses.KEY_LEFT:
            tab.move_left()
        if key == curses.KEY_RIGHT:
            tab.move_right()
        if key == curses.KEY_UP:
            set_scroll(1)
        if key == curses.KEY_DOWN:
            set_scroll(-1)
        if key == curses.KEY_PPAGE:
            set_scroll(-10)
        if key == curses.KEY_NPAGE:
            set_scroll(10)
        if key == curses.KEY_HOME:
            # size of the window
            scroll_to_zero()
        KEY_ENTER = 10
        if key == KEY_ENTER or key == curses.KEY_END:
            draw_screen.scroll = 0
            globvar.pristine.unpause()

    globvar.quitting = True


if __name__ == "__main__":
    if len(sys.argv) < 2:
        usage()
        sys.exit(1)

    profile = sys.argv[2:] or []
    if len(profile) == 2 and profile[0] == '-f':
        load_profile_from_file(profile[1])

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
