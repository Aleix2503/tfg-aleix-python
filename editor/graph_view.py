from PySide6.QtWidgets import QGraphicsView, QGraphicsScene, QMenu, QGraphicsLineItem
from PySide6.QtGui import QPainter, QPen, QColor
from PySide6.QtCore import Qt

from editor.edge_item import TransitionEdge
from model.transition import Transition
from model.state import State
from editor.node_item import StateNode

class GraphView(QGraphicsView):
    def __init__(self, inspector=None, fsm=None):
        super().__init__()

        self.inspector = inspector
        self.fsm = fsm

        self.scene = QGraphicsScene()
        self.setScene(self.scene)
        self.setRenderHint(QPainter.Antialiasing)

        self.scene.selectionChanged.connect(self.on_selection_changed)

        # Estado para crear transiciones
        self.transition_source = None
        self.temp_line = None
        self.creating_transition = False
        
        self.setFocusPolicy(Qt.StrongFocus)
        
        # Crear el nodo visual del any_state
        if self.fsm:
            self.setup_any_state()

    def setup_any_state(self):
        """Crea el nodo visual del any_state en la esquina superior izquierda"""
        if not self.fsm:
            return
        
        any_state = self.fsm.get_any_state()
        if any_state:
            # Verificar si ya existe el nodo visual
            for item in self.scene.items():
                if isinstance(item, StateNode) and item.state.is_any_state:
                    return  # Ya existe
            
            # Crear nodo visual en la esquina superior izquierda
            node = StateNode(any_state, view=self)
            node.setPos(-50, -50)  # Esquina superior izquierda
            node.update_appearance()
            
            # Conectar señales
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
        # Obtener todos los items en esa posición
        scene_pos = self.mapToScene(event.pos())
        items_at_pos = self.scene.items(scene_pos)
        
        # Filtrar solo StateNode
        state_nodes = [item for item in items_at_pos if isinstance(item, StateNode)]
        item = state_nodes[0] if state_nodes else None

        # Si estamos creando transición
        if self.creating_transition:
            if item:
                # Click izquierdo en destino válido
                if event.button() == Qt.LeftButton:
                    self.create_transition(self.transition_source, item)
                    self.end_transition_creation()
                    return
            elif event.button() == Qt.LeftButton:
                # Click izquierdo fuera de estado válido = cancelar
                self.end_transition_creation()
                return

        super().mousePressEvent(event)

    def transition_exists(self, source_node, target_node):
        for transition in self.fsm.transitions:
            if transition.from_state == source_node.state and transition.to_state == target_node.state:
                return True

        return False

    def mouseMoveEvent(self, event):
        # Si estamos creando transición, actualizar la línea temporal
        if self.creating_transition and self.transition_source and self.temp_line:
            scene_pos = self.mapToScene(event.pos())
            # Obtener el centro del estado origen
            source_pos = self.transition_source.scenePos()
            source_center = source_pos + self.transition_source.rect().center()
            
            # Actualizar la línea
            self.temp_line.setLine(
                source_center.x(),
                source_center.y(),
                scene_pos.x(),
                scene_pos.y()
            )

        super().mouseMoveEvent(event)

    def keyPressEvent(self, event):
        # Escape cancela la creación de transición
        if event.key() == Qt.Key_Escape and self.creating_transition:
            self.end_transition_creation()
            return

        # Suprimir / Delete: eliminar items seleccionados
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
        if source_node == target_node:
            return
        
        # No permitir transiciones hacia ANY_STATE
        if target_node.state.is_any_state:
            from PySide6.QtWidgets import QMessageBox
            QMessageBox.warning(self, "Transición Inválida", 
                              "No se pueden crear transiciones hacia ANY_STATE. Solo puedes crear transiciones DESDE ANY_STATE.")
            return

        if self.transition_exists(source_node, target_node):
            print(
                f"Transition already exists: "
                f"{source_node.state.id} -> {target_node.state.id}"
            )
            return

        transition = Transition(
            source_node.state,
            target_node.state
        )

        self.fsm.add_transition(transition)

        edge = TransitionEdge(source_node, target_node, transition)
        source_node.add_edge(edge)
        target_node.add_edge(edge)

        self.scene.addItem(edge)

    def start_transition_creation(self, source_node):
        """Inicia el proceso de crear una transición"""
        self.transition_source = source_node
        self.creating_transition = True
        
        # Cambiar color a amarillo
        source_node.setBrush(Qt.yellow)
        
        # Crear línea temporal
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
        # Hacer que la línea no intercepte clicks
        self.temp_line.setAcceptedMouseButtons(Qt.NoButton)
        self.scene.addItem(self.temp_line)

    def end_transition_creation(self):
        """Termina el proceso de crear una transición"""
        if self.transition_source:
            self.transition_source.setBrush(Qt.lightGray)
        
        if self.temp_line:
            self.scene.removeItem(self.temp_line)
            self.temp_line = None
        
        self.transition_source = None
        self.creating_transition = False

    def complete_transition(self, target_node):
        """Completa la transición al hacer click en el nodo destino"""
        if not self.creating_transition or not self.transition_source:
            return
        
        if target_node != self.transition_source:
            self.create_transition(self.transition_source, target_node)
        
        self.end_transition_creation()

    def contextMenuEvent(self, event):
        item = self.itemAt(event.pos())
        
        # Solo mostrar menú si no hay un nodo bajo el cursor
        if item and isinstance(item, StateNode):
            return
        
        menu = QMenu()
        create_state_action = menu.addAction("Crear nuevo estado")
        create_entry_action = menu.addAction("Crear Entry Point")
        
        action = menu.exec(event.globalPos())
        
        if action == create_state_action:
            scene_pos = self.mapToScene(event.pos())
            self.create_state_at(scene_pos.x(), scene_pos.y())
        elif action == create_entry_action:
            scene_pos = self.mapToScene(event.pos())
            self.create_entry_point_at(scene_pos.x(), scene_pos.y())

    def create_state_at(self, x, y):
        # Generar nombre único para el estado
        existing_states = {state.id for state in self.fsm.states}
        counter = 1
        while f"State_{counter}" in existing_states:
            counter += 1
        
        state_name = f"State_{counter}"
        
        # Crear estado en el modelo
        new_state = State(state_name)
        self.fsm.add_state(new_state)
        
        # Crear nodo visual (pasar referencia a la vista)
        node = StateNode(new_state, view=self)
        node.setPos(x, y)
        node.update_appearance()
        
        # Conectar señales
        node.create_transition_requested.connect(
            lambda: self.start_transition_creation(node)
        )
        node.clicked_for_transition.connect(
            lambda: self.complete_transition(node)
        )
        
        self.scene.addItem(node)

    def create_entry_point_at(self, x, y):
        """Crea un nuevo entry point en la posición especificada"""
        # Generar nombre único para el estado
        existing_states = {state.id for state in self.fsm.states}
        counter = 1
        while f"State_{counter}" in existing_states:
            counter += 1
        
        state_name = f"State_{counter}"
        
        # Crear estado como entry point
        new_state = State(state_name, is_entry_point=True)
        
        # Si hay un entry point anterior, desactivarlo
        for state in self.fsm.states:
            state.is_entry_point = False
        
        self.fsm.add_state(new_state)
        
        # Crear nodo visual
        node = StateNode(new_state, view=self)
        node.setPos(x, y)
        node.update_appearance()
        
        # Conectar señales
        node.create_transition_requested.connect(
            lambda: self.start_transition_creation(node)
        )
        node.clicked_for_transition.connect(
            lambda: self.complete_transition(node)
        )
        
        self.scene.addItem(node)
        
        # Actualizar apariencia de otros nodos
        for item in self.scene.items():
            if isinstance(item, StateNode) and item != node:
                item.update_appearance()

    def delete_state(self, node):
        """Elimina un estado, sus aristas y las transiciones asociadas del modelo y la escena."""
        # No permitir eliminar any_state
        if node.state.is_any_state:
            from PySide6.QtWidgets import QMessageBox
            QMessageBox.warning(self, "No se puede eliminar", 
                              "El ANY_STATE no se puede eliminar. Es fundamental para transiciones globales.")
            return
        
        # Verificar si se está eliminando el entry point
        is_deleting_entry_point = node.state.is_entry_point
        
        # Eliminar aristas conectadas
        for edge in list(node.edges):
            # Quitar referencia en nodos fuente/target
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

            # Eliminar la transición del modelo
            try:
                if edge.transition in self.fsm.transitions:
                    self.fsm.transitions.remove(edge.transition)
            except Exception:
                pass

            # Eliminar la flecha asociada si existe
            try:
                if hasattr(edge, 'arrow') and edge.arrow and edge.arrow.scene():
                    self.scene.removeItem(edge.arrow)
            except Exception:
                pass

            # Eliminar la arista de la escena
            try:
                if edge.scene():
                    self.scene.removeItem(edge)
            except Exception:
                pass

        # Eliminar el nodo de la escena
        try:
            if node.scene():
                self.scene.removeItem(node)
        except Exception:
            pass

        # Eliminar el estado del modelo
        try:
            if node.state in self.fsm.states:
                self.fsm.states.remove(node.state)
        except Exception:
            pass
        
        # Si se eliminó el entry point, mostrar advertencia
        if is_deleting_entry_point:
            from PySide6.QtWidgets import QMessageBox
            QMessageBox.warning(self, "Entry Point Eliminado", 
                              "El Entry Point ha sido eliminado. La FSM ahora no tiene punto de entrada.")

    def delete_edge(self, edge):
        """Elimina una arista/transition individualmente."""
        # Quitar referencias en nodos
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

        # Eliminar la transición del modelo
        try:
            if edge.transition in self.fsm.transitions:
                self.fsm.transitions.remove(edge.transition)
        except Exception:
            pass

        # Eliminar la flecha asociada si existe
        try:
            if hasattr(edge, 'arrow') and edge.arrow and edge.arrow.scene():
                self.scene.removeItem(edge.arrow)
        except Exception:
            pass

        # Eliminar la arista de la escena
        try:
            if edge.scene():
                self.scene.removeItem(edge)
        except Exception:
            pass
