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
    try:
        os.makedirs(globvar.path)
    except FileExistsError:
        return


def save_profile_to_file(profile):
    file = globvar.path + "/" + profile + ".json"

    assure_config_dir_exists()

    with open(file, 'w') as f:
        json.dump(tab.titles, f, sort_keys=True, cls=TabEncoder)


def load_profile_from_file(profile):
    file = globvar.path + "/" + profile + ".json"

    try:
        with open(file, 'r') as f:
            input_json = json.loads(f.read())
            tab.titles = []
            for t in input_json:
                atab = tab.Tab(t['name'])
                atab.grep = t['grep']
                tab.titles.append(atab)
    except FileNotFoundError:
        return


def load_profile(stdscr):
    """ Save profile to file"""

    word = get_input(stdscr, "Loading: Profile name:")
    # Get resulting contents
    load_profile_from_file(word)
