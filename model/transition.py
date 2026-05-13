class Transition:
    def __init__(self, from_state, to_state):
        self.from_state = from_state
        self.to_state = to_state
        self.conditions = []  # Lista de condiciones

    def to_dict(self):
        return {
            "from": self.from_state.id,
            "to": self.to_state.id,
            "conditions": [c.to_dict() for c in self.conditions]
        }