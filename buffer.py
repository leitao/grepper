import globvar


class Buffer:
    # Main buffer
    main_buffer = []
    # Buffer when the ingestion is paused
    tmp = []

    paused = False
    consumable = False

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
