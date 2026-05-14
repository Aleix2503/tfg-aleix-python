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

    # Preparar datos de FSM, excluyendo any_state
    fsm_dict = fsm.to_dict()
    fsm_dict["states"] = [s for s in fsm_dict["states"] if not s.get("is_any_state", False)]
    
    # Filtrar transiciones que involucren any_state (opcional - permitir transiciones desde any_state)
    # Por ahora, permitimos transiciones desde any_state pero no mostramos el any_state en el JSON

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

    print("Project saved:", path)