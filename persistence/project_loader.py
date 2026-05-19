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

    # Crear FSM nueva
    fsm = FSM(fsm_data["name"])

    node_map = {}

    # ─────────────────────────────────────
    # ESTADOS
    # ─────────────────────────────────────

    # Cargar estados SIN is_entry_point para que FSM.add_state() los maneje
    for state_data in fsm_data["states"]:
        # Ignorar el any_state si existe (se crea automáticamente)
        if state_data.get("is_any_state", False):
            continue
        
        state = State(
            state_data["id"],
            is_entry_point=False,
            is_any_state=False,
            is_global_state=state_data.get("is_global_state", False)
        )

        # Cargar acciones (convertir formato antiguo si es necesario)
        def load_action_params(action_data):
            """Cargar parámetros en formato nuevo (array) o antiguo (dict)"""
            params = action_data.get("params", [])

            # Si params es un diccionario (formato antiguo), convertir a array
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

        fsm.states.append(state)  # Agregar directamente sin usar add_state()
    
    # Ahora establecer el entry point correcto
    for state_data in fsm_data["states"]:
        if state_data.get("is_entry_point", False):
            for state in fsm.states:
                if state.id == state_data["id"]:
                    fsm.set_entry_point(state)
                    break
    
    # Si no hay entry point y hay estados regulares, establecer el primero como entry point
    if fsm.get_entry_point() is None:
        regular_states = [s for s in fsm.states if not s.is_any_state and not s.is_global_state]
        if regular_states:
            fsm.set_entry_point(regular_states[0])
    
    # Crear nodos visuales para todos los estados
    for state in fsm.states:
        # Posición visual
        pos = editor_data["nodes"].get(state.id, {})

        x = pos.get("x", 0)
        y = pos.get("y", 0)
        
        # Si es any_state y no tiene posición guardada, posicionarlo en esquina superior izquierda
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
    # TRANSICIONES
    # ─────────────────────────────────────

    for transition_data in fsm_data["transitions"]:

        from_state = transition_data["from"]
        to_state = transition_data["to"]

        source_node = node_map[from_state]
        target_node = node_map[to_state]

        # Deserializar condición
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