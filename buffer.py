import re

import colors
import globvar
import curses


class Buffer:
    # Main buffer
    main_buffer = []
    # Buffer when the ingestion is paused
    tmp = []

    paused = False
    consumable = False
    scroll = 0

    def len(self):
        return len(self.main_buffer)

    def goto_home(self):
        scroll = -1

    def pause(self):
        self.paused = True
        globvar.redraw = True

    def unpause(self):
        self.paused = False

        if self.tmp:
            self.main_buffer = self.main_buffer + self.tmp
            self.tmp = []
        self.consumable = True
        globvar.clear_screen = True
        globvar.redraw = True

    def ingest(self, line):
        if not self.paused:
            self.main_buffer.append(line)
            self.consumable = True
            globvar.redraw = True
        else:
            self.tmp.append(line)

    def get_main(self):
        self.consumable = False
        return self.main_buffer


class PrintBuffer:
    """ Just the buffer that will be printed to the body"""

    def __init__(self, array_and_colors):
        self.words = array_and_colors
        self.text = []

    def should_highlight(self, line):
        """ Does this line contains any word from the array of words we care"""
        for word, _ in self.words:
            if word in line:
                return True
        return False

    def full(self):
        body_size = curses.LINES - 5
        return False

    def add(self, line):
        self.text.insert(0, line)

    def print_all(self, win):
        for line in self.text:
            self.print_each_line(win, line)

        win.refresh()

    def highlight_all(self, win, line, array_of_words):
        # Start with the whole line, and breakding down as we found words
        array_to_be_printed = [(line, colors.COLOR_DEFAULT)]
        for word, color in array_of_words:
            if not word:
                raise Exception("Got a null string to highlight")

            array_to_be_printed = self.highlight_single_word(array_to_be_printed, word, color)

        self.print_array(win, array_to_be_printed)

    def highlight_single_word(self, setence_array, word, color):
        # Going to return substrings with the proper colors
        # Example: [("foo", color: 1), ("bar", color:2)]
        ret = []

        found = False
        for subsentences, c in setence_array:
            # arr = [(word, color), ...]
            if word in subsentences:
                parts = re.split(f"({word}|[()])", subsentences)
                for part in parts:
                    if word == part:
                        # Set the new color
                        ret.append((part, color))
                    else:
                        # Continue with the old color
                        ret.append((part, c))
            else:
                # Don't care about a subsentence without words we care
                ret.append((subsentences,c))

        return ret

    def print_each_line(self, win, line):
        if not self.should_highlight(line):
            # Just print
            win.addstr(line, colors.COLOR_DEFAULT)
            return

        self.highlight_all(win, line, self.words)

    def print_array(self, win, array_to_be_printed):
        for word, color in array_to_be_printed:
            win.addstr(word, curses.color_pair(color))

