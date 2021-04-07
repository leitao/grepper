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


def scroll_text(stdscr, lines):
    if draw_screen.scroll <= 0:
        globvar.pristine.unpause()
    draw_screen(stdscr, lines)


def draw_screen(stdscr, scroll):
    if not hasattr(draw_screen, "scroll"):
        draw_screen.scroll = 0

    draw_screen.scroll += scroll

    if globvar.clear_screen:
        stdscr.clear()
        globvar.clear_screen = False

    # No scroll set anymore. Let the test run
    if draw_screen.scroll <= 0:
        draw_screen.scroll = 0
    else:
        globvar.pristine.pause()

    tab.print_all_tabs(stdscr)
    print_body(draw_screen.scroll)
    stdscr.refresh()


def main(stdscr):
    set_screen_defaults(stdscr)

    # Add initial tab
    tab.add_new_tab()
    globvar.redraw = True

    key = ''

    while key != ord('q') and globvar.quitting is False:
        if globvar.redraw:
            draw_screen(stdscr, 0)
            globvar.redraw = False

        key = stdscr.getch()
        if key == curses.ERR:
            continue

        if key == ord('a'):
            tab.add_new_tab()
        if key == ord('d'):
            tab.delete_tab()
        if key == curses.KEY_LEFT:
            tab.move_left()
        if key == curses.KEY_RIGHT:
            tab.move_right()
        if key == ord('/'):
            tab.set_grep_word(stdscr)
            globvar.clear_screen = True
        if key == curses.KEY_UP:
            scroll_text(stdscr, 1)
        if key == curses.KEY_DOWN:
            scroll_text(stdscr, -1)
        if key == curses.KEY_PPAGE:
            scroll_text(stdscr, 10)
        if key == ord('?') or key == ord('h'):
            show_help(stdscr)
        if key == curses.KEY_NPAGE:
            scroll_text(stdscr, -10)
        if key == ord('c'):
            # Chance the case sensitive
            tab.titles[tab.get_idx()].case_sensitive = not tab.titles[tab.get_idx()].case_sensitive
        if key == ord('s'):
            # Chance the case sensitive
            save_profile(stdscr)
        if key == ord('l'):
            # Chance the case sensitive
            load_profile(stdscr)

        if key == curses.KEY_HOME:
            # size of the window
            scroll_text(stdscr, len(globvar.pristine.get_main()) - (curses.LINES - hsize - 2))

        KEY_ENTER = 10
        if key == KEY_ENTER or key == curses.KEY_END:
            draw_screen.scroll = 0
            globvar.pristine.unpause()

        if key == ord('p'):
            if not globvar.pristine.paused:
                globvar.pristine.pause()
            else:
                globvar.pristine.unpause()
                # Hack to go to the bottom of the text on unpause
                draw_screen.scroll = 0
                scroll_text(stdscr, -200)

    globvar.quitting = True


if __name__ == "__main__":
    if len(sys.argv) < 2:
        usage()
        sys.exit(1)

    profile = sys.argv[2:] or []
    if len(profile) == 2 and profile[0] == '-f':
        load_profile_from_file(profile[1])

    curses.initscr()

    curses.cbreak()
    curses.noecho()
    curses.curs_set(0)
    curses.start_color()
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
