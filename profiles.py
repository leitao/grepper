import json
from tabencoder import TabEncoder
from tab import Tab
from input import get_input

def save_profile(stdscr):
    """ Save profile to file"""

    word = get_input(stdscr, "Saving: Profile name:")
    # Get resulting contents
    save_profile_to_file(word)

def save_profile_to_file(word):
    global titles
    with open(f"{word.strip()}.json", 'w') as f:
        json.dump(titles, f, sort_keys=True, cls=TabEncoder)

def load_profile_from_file(word):
    global titles
    with open(f"{word.strip()}.json", 'r') as f:
        input_json = json.loads(f.read())
        titles = []
        for t in input_json:
            tab = Tab(t['name'])
            tab.case_sensitive = t['case_sensitive']
            tab.grep = t['grep']
            titles.append(tab)


def load_profile(stdscr):
    """ Save profile to file"""

    word = get_input(stdscr, "Loading: Profile name:")
    # Get resulting contents
    load_profile_from_file(word)
