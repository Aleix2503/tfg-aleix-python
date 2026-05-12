from PySide6.QtWidgets import QGraphicsRectItem, QGraphicsTextItem, QMenu
from PySide6.QtCore import Qt, Signal, QObject

class StateNode(QGraphicsRectItem, QObject):
    create_transition_requested = Signal()
    clicked_for_transition = Signal()
    
    def __init__(self, state, view=None):
        QGraphicsRectItem.__init__(self, 0, 0, 120, 50)
        QObject.__init__(self)

        self.state = state
        self.edges = []
        self.view = view

        self.text = QGraphicsTextItem(state.id, self)
        self.text.setPos(10, 10)

        self.setBrush(Qt.lightGray)

        self.setFlags(
            QGraphicsRectItem.ItemIsMovable |
            QGraphicsRectItem.ItemIsSelectable |
            QGraphicsRectItem.ItemSendsGeometryChanges  
        )

    def add_edge(self, edge):
        self.edges.append(edge)

    def mousePressEvent(self, event):
        if event.button() == Qt.RightButton:
            self.show_context_menu(event)
            return
        
        # Si estamos creando transición y es click izquierdo
        if self.view and self.view.creating_transition and event.button() == Qt.LeftButton:
            self.clicked_for_transition.emit()
            return
        
        super().mousePressEvent(event)

    def show_context_menu(self, event):
        menu = QMenu()
        create_transition_action = menu.addAction("Crear transición")
        delete_action = menu.addAction("Eliminar estado")
        
        action = menu.exec(event.screenPos())
        
        if action == create_transition_action:
            self.create_transition_requested.emit()
        elif action == delete_action:
            # Pedir a la vista que elimine este nodo
            if self.view:
                self.view.delete_state(self)

    def itemChange(self, change, value):
        if change == QGraphicsRectItem.ItemPositionHasChanged:  
            for edge in self.edges:
                edge.update_position()

        return super().itemChange(change, value)

    def contextMenuEvent(self, event):
        menu = QMenu()
        create_transition_action = menu.addAction("Crear transición")
        delete_action = menu.addAction("Eliminar estado")
        
        action = menu.exec(event.screenPos())
        
        if action == create_transition_action:
            self.create_transition_requested.emit()
        elif action == delete_action:
            if self.view:
                self.view.delete_state(self)
