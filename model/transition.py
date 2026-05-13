class Transition:
    def __init__(self, from_state, to_state, condition=None):
        self.from_state = from_state
        self.to_state = to_state
        self.condition = condition

    def to_dict(self):
        return {
            "from": self.from_state.id,
            "to": self.to_state.id,
            "condition": self.condition.to_dict() if self.condition else None
        }