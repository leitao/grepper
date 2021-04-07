# Ingestion Buffer
from buffer import Buffer
import os

# The Buffer ingesting data
pristine = Buffer()

# If set, the threads' loop exist
quitting = False

# Set if the screen needs to be cleared (Rewriting tab's name)
clear_screen = False

# Set if all the screen needs to be redrawn
redraw = True

# Wait for getchr() otherwise refresh
TIMEOUT = 100

# Path where profiles will be saved
path = os.path.expanduser("~") + "/.config/grepper"

# Name of the recently created tabs
unamed = "Unfiltered"
