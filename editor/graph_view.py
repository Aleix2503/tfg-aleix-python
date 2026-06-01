from PySide6.QtWidgets import QGraphicsView, QGraphicsScene, QMenu, QGraphicsLineItem
from PySide6.QtGui import QPainter, QPen, QColor
from PySide6.QtCore import Qt

from editor.edge_item import TransitionEdge
from model.transition import Transition
from model.state import State
from editor.node_item import StateNode

class GraphView(QGraphicsView):
    def __init__(self, inspector=None, fsm=None, on_change_callback=None, command_manager=None, on_command_executed=None):
        super().__init__()

        self.inspector = inspector
        self.fsm = fsm
        self.on_change_callback = on_change_callback
        self.command_manager = command_manager
        self.on_command_executed = on_command_executed  # Callback cuando se ejecuta un comando

        self.scene = QGraphicsScene()
        self.setScene(self.scene)
        self.setRenderHint(QPainter.Antialiasing)

        self.scene.selectionChanged.connect(self.on_selection_changed)

        # State for transition creation
        self.transition_source = None
        self.temp_line = None
        self.creating_transition = False
        
        self.setFocusPolicy(Qt.StrongFocus)
        
        # Crear el nodo visual del any_state
        if self.fsm:
            self.setup_any_state()

    def setup_any_state(self):
        """Creates the visual node of any_state in the upper left corner"""
        if not self.fsm:
            return

        any_state = self.fsm.get_any_state()
        if any_state:
            # Check if visual node already exists
            for item in self.scene.items():
                if isinstance(item, StateNode) and item.state.is_any_state:
                    return  # Already exists

            # Create visual node in upper left corner
            node = StateNode(any_state, view=self)
            node.setPos(-50, -50)  # Upper left corner
            node.update_appearance()
            
            # Connect signals
            node.create_transition_requested.connect(
                lambda: self.start_transition_creation(node)
            )
            node.clicked_for_transition.connect(
                lambda: self.complete_transition(node)
            )

            self.scene.addItem(node)

    def on_selection_changed(self):
        if not self.inspector:
            return

        selected = self.scene.selectedItems()
        if selected:
            self.inspector.inspect(selected[0])
        else:
            self.inspector.clear()

    def mousePressEvent(self, event):
        # Get all items at that position
        scene_pos = self.mapToScene(event.pos())
        items_at_pos = self.scene.items(scene_pos)

        # Filter only StateNode
        state_nodes = [item for item in items_at_pos if isinstance(item, StateNode)]
        item = state_nodes[0] if state_nodes else None

        # If we're creating transition
        if self.creating_transition:
            if item:
                # Left click on valid target
                if event.button() == Qt.LeftButton:
                    self.create_transition(self.transition_source, item)
                    self.end_transition_creation()
                    return
            elif event.button() == Qt.LeftButton:
                # Left click outside valid state = cancel
                self.end_transition_creation()
                return

        super().mousePressEvent(event)

    def transition_exists(self, source_node, target_node):
        for transition in self.fsm.transitions:
            if transition.from_state == source_node.state and transition.to_state == target_node.state:
                return True

        return False

    def mouseMoveEvent(self, event):
        # If we're creating transition, update temporary line
        if self.creating_transition and self.transition_source and self.temp_line:
            scene_pos = self.mapToScene(event.pos())
            # Get center of source state
            source_pos = self.transition_source.scenePos()
            source_center = source_pos + self.transition_source.rect().center()

            # Update line
            self.temp_line.setLine(
                source_center.x(),
                source_center.y(),
                scene_pos.x(),
                scene_pos.y()
            )

        super().mouseMoveEvent(event)

    def keyPressEvent(self, event):
        # Escape cancels transition creation
        if event.key() == Qt.Key_Escape and self.creating_transition:
            self.end_transition_creation()
            return

        # Delete / Backspace: delete selected items
        if event.key() in (Qt.Key_Delete, Qt.Key_Backspace):
            selected = list(self.scene.selectedItems())
            for it in selected:
                if isinstance(it, StateNode):
                    self.delete_state(it)
                elif isinstance(it, TransitionEdge):
                    self.delete_edge(it)
            return

        super().keyPressEvent(event)

    def create_transition(self, source_node, target_node):
        from commands import CreateTransitionCommand

        # Don't allow transitions to ANY_STATE
        if target_node.state.is_any_state:
            from PySide6.QtWidgets import QMessageBox
            QMessageBox.warning(self, "Invalid Transition",
                              "Cannot create transitions to ANY_STATE. You can only create transitions FROM ANY_STATE.")
            return

        # Don't allow transitions from or to global_state
        if source_node.state.is_global_state or target_node.state.is_global_state:
            from PySide6.QtWidgets import QMessageBox
            QMessageBox.warning(
                self,
                "Invalid Transition",
                "Cannot create transitions from or to a Global State. "
                "Global States only execute actions per tick."
            )
            return

        if self.transition_exists(source_node, target_node):
            return

        # Create command
        command = CreateTransitionCommand(self.fsm, self, source_node, target_node)

        # Execute through command_manager
        if self.command_manager:
            self.command_manager.execute(command)
            if self.on_command_executed:
                self.on_command_executed()
        else:
            command.execute()

        # Notify that there are changes
        if self.on_change_callback:
            self.on_change_callback()

    def _create_transition_impl(self, source_node, target_node):
        """Internal implementation of transition creation (without commands)"""
        transition = Transition(source_node.state, target_node.state)
        self.fsm.add_transition(transition)

        edge = TransitionEdge(source_node, target_node, transition)
        source_node.add_edge(edge)
        target_node.add_edge(edge)

        self.scene.addItem(edge)
        return edge

    def start_transition_creation(self, source_node):
        """Starts the transition creation process"""
        # First, clean up any existing temp line
        if self.temp_line:
            self.scene.removeItem(self.temp_line)
            self.temp_line = None

        self.transition_source = source_node
        self.creating_transition = True

        # Change color to yellow
        source_node.setBrush(Qt.yellow)

        # Create temporary line
        source_pos = source_node.scenePos()
        source_center = source_pos + source_node.rect().center()

        self.temp_line = QGraphicsLineItem()
        pen = QPen(QColor(255, 0, 0, 200))
        pen.setWidth(2)
        pen.setStyle(Qt.DashLine)
        self.temp_line.setPen(pen)
        self.temp_line.setLine(
            source_center.x(),
            source_center.y(),
            source_center.x(),
            source_center.y()
        )
        # Make line not intercept clicks
        self.temp_line.setAcceptedMouseButtons(Qt.NoButton)
        # Set z-value above states
        self.temp_line.setZValue(1)
        self.scene.addItem(self.temp_line)

    def end_transition_creation(self):
        """Ends the transition creation process"""
        if self.transition_source:
            # Restore original state color
            self.transition_source.update_appearance()

        if self.temp_line:
            self.scene.removeItem(self.temp_line)
            self.temp_line = None

        self.transition_source = None
        self.creating_transition = False

    def complete_transition(self, target_node):
        """Completes transition when clicking on target node"""
        if not self.creating_transition or not self.transition_source:
            return
        
        if target_node != self.transition_source:
            self.create_transition(self.transition_source, target_node)
        
        self.end_transition_creation()

    def contextMenuEvent(self, event):
        item = self.itemAt(event.pos())

        # Only show menu if there's no node under cursor
        if item and isinstance(item, StateNode):
            return

        menu = QMenu()
        create_state_action = menu.addAction("Create new state")
        create_entry_action = menu.addAction("Create Entry Point")
        create_global_action = menu.addAction("Create Global State")
        
        action = menu.exec(event.globalPos())
        
        if action == create_state_action:
            scene_pos = self.mapToScene(event.pos())
            self.create_state_at(scene_pos.x(), scene_pos.y())
        elif action == create_entry_action:
            scene_pos = self.mapToScene(event.pos())
            self.create_entry_point_at(scene_pos.x(), scene_pos.y())
        elif action == create_global_action:
            scene_pos = self.mapToScene(event.pos())
            self.create_global_state_at(scene_pos.x(), scene_pos.y())

    def create_state_at(self, x, y):
        from commands import CreateStateCommand

        # Create command
        command = CreateStateCommand(self.fsm, self, x, y, "normal")

        # Execute through command_manager
        if self.command_manager:
            self.command_manager.execute(command)
            # Notify that command was executed
            if self.on_command_executed:
                self.on_command_executed()
        else:
            # Fallback if no command_manager
            command.execute()

        # Notify that there are changes
        if self.on_change_callback:
            self.on_change_callback()

    def _create_state_at_impl(self, x, y, state_type="normal"):
        """Internal implementation of state creation (without commands)"""
        # Generate unique name for state based on type
        existing_states = {state.id for state in self.fsm.states}

        if state_type == "global":
            prefix = "Global_State_"
            counter = 1
            while f"{prefix}{counter}" in existing_states:
                counter += 1
            state_name = f"{prefix}{counter}"
            new_state = State(state_name, is_global_state=True)
        elif state_type == "entry":
            prefix = "State_"
            counter = 1
            while f"{prefix}{counter}" in existing_states:
                counter += 1
            state_name = f"{prefix}{counter}"
            new_state = State(state_name, is_entry_point=True)
            # If there's a previous entry point, deactivate it
            for state in self.fsm.states:
                state.is_entry_point = False
        else:
            prefix = "State_"
            counter = 1
            while f"{prefix}{counter}" in existing_states:
                counter += 1
            state_name = f"{prefix}{counter}"
            new_state = State(state_name)

        self.fsm.add_state(new_state)

        # Create visual node (pass reference to view)
        node = StateNode(new_state, view=self)
        node.setPos(x, y)
        node.update_appearance()

        # Connect signals
        node.create_transition_requested.connect(
            lambda: self.start_transition_creation(node)
        )
        node.clicked_for_transition.connect(
            lambda: self.complete_transition(node)
        )

        self.scene.addItem(node)

        # If entry point, update appearance of other nodes
        if state_type == "entry":
            for item in self.scene.items():
                if isinstance(item, StateNode) and item != node:
                    item.update_appearance()

        return new_state, node

    def create_global_state_at(self, x, y):
        """Creates a global state without transitions at specified position"""
        from commands import CreateStateCommand

        # Crear comando
        command = CreateStateCommand(self.fsm, self, x, y, "global")

        # Execute through command_manager
        if self.command_manager:
            self.command_manager.execute(command)
            if self.on_command_executed:
                self.on_command_executed()
        else:
            command.execute()

        # Notificar que hay cambios
        if self.on_change_callback:
            self.on_change_callback()

    def create_entry_point_at(self, x, y):
        """Creates a new entry point at specified position"""
        from commands import CreateStateCommand

        # Crear comando
        command = CreateStateCommand(self.fsm, self, x, y, "entry")

        # Execute through command_manager
        if self.command_manager:
            self.command_manager.execute(command)
            if self.on_command_executed:
                self.on_command_executed()
        else:
            command.execute()

        # Notificar que hay cambios
        if self.on_change_callback:
            self.on_change_callback()

    def delete_state(self, node):
        """Deletes a state, its edges and associated transitions from model and scene."""
        from commands import DeleteStateCommand

        # Don't allow deleting any_state
        if node.state.is_any_state:
            from PySide6.QtWidgets import QMessageBox
            QMessageBox.warning(self, "Cannot delete",
                              "ANY_STATE cannot be deleted. It's essential for global transitions.")
            return

        # Create command
        command = DeleteStateCommand(self.fsm, node, self)

        # Execute through command_manager
        if self.command_manager:
            self.command_manager.execute(command)
            if self.on_command_executed:
                self.on_command_executed()
        else:
            command.execute()

        # If entry point was deleted, show warning
        if node.state.is_entry_point:
            from PySide6.QtWidgets import QMessageBox
            QMessageBox.warning(self, "Entry Point Deleted",
                              "The Entry Point has been deleted. The FSM now has no entry point.")

        # Notify that there are changes
        if self.on_change_callback:
            self.on_change_callback()

    def _delete_state_impl(self, node):
        """Internal implementation of state deletion (without commands)"""
        # Delete connected edges
        for edge in list(node.edges):
            # Remove reference in source/target nodes
            try:
                if edge in edge.source.edges:
                    edge.source.edges.remove(edge)
            except Exception:
                pass
            try:
                if edge in edge.target.edges:
                    edge.target.edges.remove(edge)
            except Exception:
                pass

            # Delete transition from model
            try:
                if edge.transition in self.fsm.transitions:
                    self.fsm.transitions.remove(edge.transition)
            except Exception:
                pass

            # Delete associated arrow if exists
            try:
                if hasattr(edge, 'arrow') and edge.arrow and edge.arrow.scene():
                    self.scene.removeItem(edge.arrow)
            except Exception:
                pass

            # Delete edge from scene
            try:
                if edge.scene():
                    self.scene.removeItem(edge)
            except Exception:
                pass

        # Delete node from scene
        try:
            if node.scene():
                self.scene.removeItem(node)
        except Exception:
            pass

        # Delete state from model
        try:
            if node.state in self.fsm.states:
                self.fsm.states.remove(node.state)
        except Exception:
            pass

    def delete_edge(self, edge):
        """Deletes an edge/transition individually."""
        from commands import DeleteTransitionCommand

        # Create command
        command = DeleteTransitionCommand(self.fsm, self, edge)

        # Execute through command_manager
        if self.command_manager:
            self.command_manager.execute(command)
            if self.on_command_executed:
                self.on_command_executed()
        else:
            command.execute()

        # Notify that there are changes
        if self.on_change_callback:
            self.on_change_callback()

    def _delete_edge_impl(self, edge):
        """Internal implementation of transition deletion (without commands)"""
        # Remove references in nodes
        try:
            if edge in edge.source.edges:
                edge.source.edges.remove(edge)
        except Exception:
            pass
        try:
            if edge in edge.target.edges:
                edge.target.edges.remove(edge)
        except Exception:
            pass

        # Delete transition from model
        try:
            if edge.transition in self.fsm.transitions:
                self.fsm.transitions.remove(edge.transition)
        except Exception:
            pass

        # Delete associated arrow if exists
        try:
            if hasattr(edge, 'arrow') and edge.arrow and edge.arrow.scene():
                self.scene.removeItem(edge.arrow)
        except Exception:
            pass

        # Delete edge from scene
        try:
            if edge.scene():
                self.scene.removeItem(edge)
        except Exception:
            pass
