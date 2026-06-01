import copy
from .command_manager import Command


class CreateStateCommand(Command):
    """Comando para crear un estado"""

    def __init__(self, fsm, graph_view, x, y, state_type="normal"):
        self.fsm = fsm
        self.graph_view = graph_view
        self.x = x
        self.y = y
        self.state_type = state_type
        self.state = None
        self.node = None

    def execute(self):
        # Use internal implementation to avoid recursion
        self.state, self.node = self.graph_view._create_state_at_impl(self.x, self.y, self.state_type)

    def undo(self):
        if self.node:
            self.graph_view._delete_state_impl(self.node)


class DeleteStateCommand(Command):
    """Comando para eliminar un estado"""

    def __init__(self, fsm, node, graph_view):
        self.fsm = fsm
        self.node = node
        self.graph_view = graph_view
        # Save state information to recreate it
        self.state_data = {
            'id': node.state.id,
            'is_entry_point': node.state.is_entry_point,
            'is_any_state': node.state.is_any_state,
            'is_global_state': node.state.is_global_state,
            'pos': node.pos(),
            'enter': copy.deepcopy(node.state.enter),
            'tick': copy.deepcopy(node.state.tick),
            'exit': copy.deepcopy(node.state.exit),
        }

    def execute(self):
        self.graph_view._delete_state_impl(self.node)

    def undo(self):
        # Recrear el estado
        from model.state import State
        from editor.node_item import StateNode

        state = State(
            self.state_data['id'],
            is_entry_point=self.state_data['is_entry_point'],
            is_any_state=self.state_data['is_any_state'],
            is_global_state=self.state_data['is_global_state']
        )

        # Restaurar acciones
        state.enter = self.state_data['enter']
        state.tick = self.state_data['tick']
        state.exit = self.state_data['exit']

        self.fsm.add_state(state)

        node = StateNode(state, view=self.graph_view)
        node.setPos(self.state_data['pos'])
        node.update_appearance()

        node.create_transition_requested.connect(
            lambda: self.graph_view.start_transition_creation(node)
        )
        node.clicked_for_transition.connect(
            lambda: self.graph_view.complete_transition(node)
        )

        self.graph_view.scene.addItem(node)
        self.node = node


class CreateTransitionCommand(Command):
    """Command to create a transition"""

    def __init__(self, fsm, graph_view, source_node, target_node):
        self.fsm = fsm
        self.graph_view = graph_view
        self.source_node = source_node
        self.target_node = target_node
        self.edge = None

    def execute(self):
        self.edge = self.graph_view._create_transition_impl(self.source_node, self.target_node)

    def undo(self):
        if self.edge:
            self.graph_view._delete_edge_impl(self.edge)


class DeleteTransitionCommand(Command):
    """Command to delete a transition"""

    def __init__(self, fsm, graph_view, edge):
        self.fsm = fsm
        self.graph_view = graph_view
        self.edge = edge
        self.transition_data = {
            'from_state': edge.transition.from_state,
            'to_state': edge.transition.to_state,
            'condition': copy.deepcopy(edge.transition.condition) if edge.transition.condition else None,
            'source_node': edge.source,
            'target_node': edge.target,
        }

    def execute(self):
        self.graph_view._delete_edge_impl(self.edge)

    def undo(self):
        # Recreate the transition
        from model.transition import Transition
        from editor.edge_item import TransitionEdge

        transition = Transition(
            self.transition_data['from_state'],
            self.transition_data['to_state'],
            self.transition_data['condition']
        )

        self.fsm.add_transition(transition)

        source_node = self.transition_data['source_node']
        target_node = self.transition_data['target_node']

        edge = TransitionEdge(source_node, target_node, transition)
        source_node.add_edge(edge)
        target_node.add_edge(edge)
        self.graph_view.scene.addItem(edge)
        self.edge = edge
