from model.state import State

class FSM:
    def __init__(self, name):
        self.name = name
        self.states = []
        self.transitions = []
        
        # Create the any_state automatically
        any_state = State("ANY_STATE", is_any_state=True)
        self.states.append(any_state)

    def add_state(self, state):
        # The first regular state (non any_state, non global_state) is automatically the entry point
        if not state.is_any_state and not state.is_global_state:
            regular_states = [s for s in self.states if not s.is_any_state and not s.is_global_state]
            if len(regular_states) == 0:
                state.is_entry_point = True
        self.states.append(state)

    def set_entry_point(self, state):
        """Sets a state as the entry point and deactivates others"""
        for s in self.states:
            s.is_entry_point = False
        state.is_entry_point = True

    def get_entry_point(self):
        """Gets the entry point state"""
        for state in self.states:
            if state.is_entry_point:
                return state
        return None
    
    def get_any_state(self):
        """Gets the any_state"""
        for state in self.states:
            if state.is_any_state:
                return state
        return None

    def add_transition(self, transition):
        self.transitions.append(transition)

    def to_dict(self):
        return {
            "version": "1.0",
            "name": self.name,
            "states": [s.to_dict() for s in self.states],
            "transitions": [t.to_dict() for t in self.transitions]
        }
