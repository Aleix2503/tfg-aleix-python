class FSM:
    def __init__(self, name):
        self.name = name
        self.initial_state = None
        self.states = []
        self.transitions = []

    def add_state(self, state):
        self.states.append(state)
        if self.initial_state is None:
            self.initial_state = state.id

    def add_transition(self, transition):
        self.transitions.append(transition)

    def to_dict(self):
        return {
            "version": "1.0",
            "name": self.name,
            "initial_state": self.initial_state if self.initial_state else None,
            "states": [s.to_dict() for s in self.states],
            "transitions": [t.to_dict() for t in self.transitions]
        }
