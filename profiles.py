import json
import os

# Project files
import globvar
from tabencoder import TabEncoder
from input import get_input
import tab

def save_profile(stdscr):
    """ Save profile to file"""

    word = get_input(stdscr, "Saving: Profile name:")
    # Get resulting contents
    save_profile_to_file(word.strip())


def assure_config_dir_exists():
    os.makedirs(globvar.path)


def save_profile_to_file(profile):
    file = globvar.path + "/" + profile + ".json"

    assure_config_dir_exists()

    with open(file, 'w') as f:
        json.dump(tab.titles, f, sort_keys=True, cls=TabEncoder)

def load_profile_from_file(profile):
    file = globvar.path + "/" + profile + ".json"

    with open(file, 'r') as f:
        input_json = json.loads(f.read())
        tab.titles = []
        for t in input_json:
            atab = tab.Tab(t['name'])
            atab.case_sensitive = t['case_sensitive']
            atab.grep = t['grep']
            tab.titles.append(atab)


def load_profile(stdscr):
    """ Save profile to file"""

    word = get_input(stdscr, "Loading: Profile name:")
    # Get resulting contents
    load_profile_from_file(word)
