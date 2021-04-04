from json import JSONEncoder

class TabEncoder(JSONEncoder):
    def default(self, o):
        return o.__dict__