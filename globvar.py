# Ingestion Buffer
from buffer import Buffer

pristine = Buffer()
quitting = False
clear_screen = False
redraw = True
# Wait for getchr() otherwise refresh
TIMEOUT = 100