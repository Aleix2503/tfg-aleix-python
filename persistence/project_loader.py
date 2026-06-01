import json

from model.fsm import FSM
from model.state import State
from model.action import Action
from model.transition import Transition
from model.condition import condition_from_dict

from editor.node_item import StateNode
from editor.edge_item import TransitionEdge

def load_project(path, scene):

    with open(path, "r", encoding="utf-8") as file:
        data = json.load(file)

    fsm_data = data["fsm"]
    editor_data = data["editor"]

    # Create new FSM
    fsm = FSM(fsm_data["name"])

    node_map = {}

    # ─────────────────────────────────────
    # STATES
    # ─────────────────────────────────────

    # Load states WITHOUT is_entry_point so that FSM.add_state() handles them
    for state_data in fsm_data["states"]:
        # Ignore the any_state if it exists (it is created automatically)
        if state_data.get("is_any_state", False):
            continue
        
        state = State(
            state_data["id"],
            is_entry_point=False,
            is_any_state=False,
            is_global_state=state_data.get("is_global_state", False)
        )

        # Load actions (convert old format if necessary)
        def load_action_params(action_data):
            """Load parameters in new format (array) or old format (dict)"""
            params = action_data.get("params", [])

            # If params is a dictionary (old format), convert to array
            if isinstance(params, dict):
                params = [{"key": k, "value": v} for k, v in params.items()]

            return params if isinstance(params, list) else []

        for action_data in state_data.get("enter", []):
            action = Action(action_data["action"])
            action.params = load_action_params(action_data)
            state.enter.append(action)

        for action_data in state_data.get("tick", []):
            action = Action(action_data["action"])
            action.params = load_action_params(action_data)
            state.tick.append(action)

        for action_data in state_data.get("exit", []):
            action = Action(action_data["action"])
            action.params = load_action_params(action_data)
            state.exit.append(action)

        fsm.states.append(state)  # Add directly without using add_state()
    
    # Now set the correct entry point
    for state_data in fsm_data["states"]:
        if state_data.get("is_entry_point", False):
            for state in fsm.states:
                if state.id == state_data["id"]:
                    fsm.set_entry_point(state)
                    break
    
    # If there is no entry point and there are regular states, set the first one as entry point
    if fsm.get_entry_point() is None:
        regular_states = [s for s in fsm.states if not s.is_any_state and not s.is_global_state]
        if regular_states:
            fsm.set_entry_point(regular_states[0])
    
    # Create visual nodes for all states
    for state in fsm.states:
        # Visual position
        pos = editor_data["nodes"].get(state.id, {})

        x = pos.get("x", 0)
        y = pos.get("y", 0)
        
        # If it's any_state and has no saved position, position it in the upper left corner
        if state.is_any_state and not editor_data["nodes"].get(state.id):
            x = -50
            y = -50

        node = StateNode(state)
        node.setPos(x, y)
        node.view = scene.views()[0] if scene.views() else None
        node.update_appearance()

        if node.view:
            node.create_transition_requested.connect(
                lambda n=node: n.view.start_transition_creation(n)
            )
            node.clicked_for_transition.connect(
                lambda n=node: n.view.complete_transition(n)
            )

        scene.addItem(node)
        node_map[state.id] = node

    # ─────────────────────────────────────
    # TRANSITIONS
    # ─────────────────────────────────────

    for transition_data in fsm_data["transitions"]:

        from_state = transition_data["from"]
        to_state = transition_data["to"]

        source_node = node_map[from_state]
        target_node = node_map[to_state]

        # Deserialize condition
        condition_data = transition_data.get("condition")
        condition = condition_from_dict(condition_data) if condition_data else None

        transition = Transition(
            source_node.state,
            target_node.state,
            condition
        )

        fsm.add_transition(transition)

        edge = TransitionEdge(
            source_node,
            target_node,
            transition
        )

        source_node.add_edge(edge)
        target_node.add_edge(edge)

        scene.addItem(edge)

    return fsm