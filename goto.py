from input import get_input
import globvar
import tab

BACK = 1
FORWARD = 2


def goto_backward(stdscr):
    globvar.redraw = True
    word = get_input(stdscr, "Go to: ")
    if not word:
        return
    tab.get_current_tab().goto = (word, BACK)


def scroll_to_top():
    """ Go to the line 0"""
    current = tab.get_current_tab()
    current.scroll = tab.SCROLL_TO_HOME
    globvar.redraw = True

def scroll_to_bottom():
    """ Go to the last line"""
    current = tab.get_current_tab()
    current.scroll = -1
    globvar.redraw = True
