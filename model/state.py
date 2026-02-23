class State:
    def __init__(self, id):
        self.id = id
        self.enter = []
        self.tick = []
        self.exit = []

    def to_dict(self):
        return {
            "id": self.id,
            "enter": [a.to_dict() for a in self.enter],
            "tick": [a.to_dict() for a in self.tick],
            "exit": [a.to_dict() for a in self.exit],
        }
