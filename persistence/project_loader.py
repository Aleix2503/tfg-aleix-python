import json

from model.fsm import FSM
from model.state import State
from model.transition import Transition

from editor.node_item import StateNode
from editor.edge_item import TransitionEdge

def load_project(path, scene):

    with open(path, "r", encoding="utf-8") as file:
        data = json.load(file)

    fsm_data = data["fsm"]
    editor_data = data["editor"]

    # Crear FSM nueva
    fsm = FSM(fsm_data["name"])

    node_map = {}

    # ─────────────────────────────────────
    # ESTADOS
    # ─────────────────────────────────────

    for state_data in fsm_data["states"]:

        state = State(state_data["id"])

        fsm.add_state(state)

        # Posición visual
        pos = editor_data["nodes"].get(state.id, {})

        x = pos.get("x", 0)
        y = pos.get("y", 0)

        node = StateNode(state)
        node.setPos(x, y)
        node.view = scene.views()[0]

        node.create_transition_requested.connect(
            lambda n=node: node.view.start_transition_creation(n)
        )

        node.clicked_for_transition.connect(
            lambda n=node: node.view.complete_transition(n)
        )

        scene.addItem(node)

        node_map[state.id] = node

    # ─────────────────────────────────────
    # TRANSICIONES
    # ─────────────────────────────────────

    for transition_data in fsm_data["transitions"]:

        from_state = transition_data["from"]
        to_state = transition_data["to"]

        source_node = node_map[from_state]
        target_node = node_map[to_state]

        transition = Transition(
            source_node.state,
            target_node.state
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