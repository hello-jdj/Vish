class GraphClipboard:
    def __init__(self):
        self.data = None

    def set(self, data: dict):
        self.data = data

    def get(self):
        return self.data

    def has_data(self):
        return self.data is not None