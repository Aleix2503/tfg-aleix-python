class State:
    def __init__(self, id, is_entry_point=False, is_any_state=False, is_global_state=False):
        self.id = id
        self.is_entry_point = is_entry_point
        self.is_any_state = is_any_state
        self.is_global_state = is_global_state
        self.enter = []
        self.tick = []
        self.exit = []

    def to_dict(self):
        return {
            "id": self.id,
            "is_entry_point": self.is_entry_point,
            "is_any_state": self.is_any_state,
            "is_global_state": self.is_global_state,
            "enter": [a.to_dict() for a in self.enter],
            "tick": [a.to_dict() for a in self.tick],
            "exit": [a.to_dict() for a in self.exit],
        }
