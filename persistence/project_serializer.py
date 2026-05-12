import json
from editor.node_item import StateNode

def save_project(fsm, scene, path):

    node_positions = {}

    # Guardar posiciones visuales
    for item in scene.items():

        if isinstance(item, StateNode):

            node_positions[item.state.id] = {
                "x": item.pos().x(),
                "y": item.pos().y()
            }

    data = {
        "project_version": "1.0",

        "fsm": fsm.to_dict(),

        "editor": {
            "nodes": node_positions,
            "zoom": 1.0
        }
    }

    with open(path, "w", encoding="utf-8") as file:
        json.dump(data, file, indent=4)

    print("Project saved:", path)