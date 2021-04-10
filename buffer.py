class Buffer:
    # Main buffer
    main_buffer = []

    def len(self):
        return len(self.main_buffer)

    def reset(self, newbuffer):
        self.main_buffer = newbuffer

    def ingest(self, line):
        self.main_buffer.append(line)

    def get_main(self):
        return self.main_buffer

