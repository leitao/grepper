# Ingestion Buffer
from buffer import Buffer
import os

pristine = Buffer()
quitting = False
clear_screen = False
redraw = True
# Wait for getchr() otherwise refresh
TIMEOUT = 100
path = os.path.expanduser("~") + "/.config/grepper"