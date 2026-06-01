import json
from editor.node_item import StateNode

def save_project(fsm, scene, path):

    node_positions = {}

    # Save visual positions
    for item in scene.items():

        if isinstance(item, StateNode):

            node_positions[item.state.id] = {
                "x": item.pos().x(),
                "y": item.pos().y()
            }

    # Prepare FSM data, excluding any_state
    fsm_dict = fsm.to_dict()
    fsm_dict["states"] = [s for s in fsm_dict["states"] if not s.get("is_any_state", False)]

    # Filter transitions involving any_state (optional - allow transitions from any_state)
    # For now, we allow transitions from any_state but do not show any_state in the JSON

    data = {
        "project_version": "1.0",

        "fsm": fsm_dict,

        "editor": {
            "nodes": node_positions,
            "zoom": 1.0
        }
    }

    with open(path, "w", encoding="utf-8") as file:
        json.dump(data, file, indent=4)