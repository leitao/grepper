import globvar
from input import get_input
import tab


def highlight(stdscr):
    globvar.redraw = True
    word = get_input(stdscr, "Highlight word: ")
    if not word:
        return
    tab.get_current_tab().highlight.append(word)


def set_grep_word(stdscr):
    word = get_input(stdscr, "Grep for: ")
    tab.get_current_tab().grep = word
    tab.get_current_tab().name = word
    # Clear screen is required since the word size (in the tab) could have changed
    globvar.clear_screen = True
    globvar.redraw = True
