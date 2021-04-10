
import goto
import header
from input import get_input

import globvar

titles = []
# index is the current index in the array. Tab 0 will be index 0
index = -1
SCROLL_TO_HOME = -1


def get_idx():
    return index


def decrease_idx():
    global index
    if index > 0:
        index -= 1


def increase_idx():
    global index
    index += 1


def delete_tab():
    globvar.clear_screen = True
    globvar.redraw = True

    if len(titles) > 1:
        titles.pop(get_idx())
        decrease_idx()


def add_new_tab():
    globvar.redraw = True
    increase_idx()
    titles.append(Tab(globvar.unamed))


def is_last_tab():
    if get_idx() == len(titles) - 1:
        return True
    return False

def get_amount_tabs():
    return len(titles)

def get_current_tab():
    return titles[get_idx()]

class Tab:
    def __init__(self, title):
        self.name = title
        self.grep = ""
        # List of additional words to high light
        self.highlight = []
        self.scroll = 0
        self.paused = False

    def toggle_pause(self):
        self.paused = not self.paused
        # Clear screen to get rid of the PAUSE text
        globvar.clear_screen = True
        globvar.redraw = True
