class Action:
    def __init__(self, name):
        self.name = name
        self.params = {}  # key: value

    def to_dict(self):
        return {
            "action": self.name,
            "params": self.params
        }

    def __str__(self):
        return f"{self.name} {self.params}"
