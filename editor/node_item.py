from PySide6.QtWidgets import QGraphicsRectItem, QGraphicsTextItem, QMenu, QGraphicsEllipseItem
from PySide6.QtCore import Qt, Signal, QObject, QPointF
from PySide6.QtGui import QPen, QColor, QBrush

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

        # Dibujar indicador de entry point si es necesario
        self.update_appearance()

        self.setFlags(
            QGraphicsRectItem.ItemIsMovable |
            QGraphicsRectItem.ItemIsSelectable |
            QGraphicsRectItem.ItemSendsGeometryChanges
        )

        # Set z-order: states appear below transition lines
        self.setZValue(0)

    def update_appearance(self):
        """Updates node appearance based on whether it's entry point, any state or global state"""
        if self.state.is_any_state:
            # Any state color
            self.setBrush(Qt.darkMagenta)
            self.text.setPlainText("ANY")
            if hasattr(self, 'entry_indicator'):
                self.entry_indicator.hide()
        elif self.state.is_global_state:
            self.setBrush(QColor(70, 130, 180))
            self.text.setPlainText(self.state.id)
            if hasattr(self, 'entry_indicator'):
                self.entry_indicator.hide()
        elif self.state.is_entry_point:
            self.setBrush(Qt.green)
            self.text.setPlainText(self.state.id)
            # Create or show entry point indicator
            if not hasattr(self, 'entry_indicator'):
                self.entry_indicator = QGraphicsEllipseItem(self)
                self.entry_indicator.setRect(-15, 10, 10, 10)
                self.entry_indicator.setBrush(QBrush(QColor(0, 200, 0)))
                self.entry_indicator.setPen(QPen(Qt.darkGreen))
            else:
                self.entry_indicator.show()
        else:
            self.setBrush(Qt.lightGray)
            self.text.setPlainText(self.state.id)
            if hasattr(self, 'entry_indicator'):
                self.entry_indicator.hide()

    def add_edge(self, edge):
        self.edges.append(edge)

    def mousePressEvent(self, event):
        if event.button() == Qt.RightButton:
            self.show_context_menu(event)
            return
        
        # If we are creating transition y es click izquierdo
        if self.view and self.view.creating_transition and event.button() == Qt.LeftButton:
            self.clicked_for_transition.emit()
            return
        
        super().mousePressEvent(event)

    def show_context_menu(self, event):
        menu = QMenu()
        if not self.state.is_global_state:
            create_transition_action = menu.addAction("Create transition")
        else:
            create_transition_action = None

        # Option to set as entry point (only if not any_state and not global_state)
        if not self.state.is_any_state and not self.state.is_global_state:
            if self.state.is_entry_point:
                entry_action = menu.addAction("✓ Is Entry Point")
                entry_action.setEnabled(False)
            else:
                entry_action = menu.addAction("Set as Entry Point")
        else:
            entry_action = None
        
        # Option to delete (only if not any_state)
        if not self.state.is_any_state:
            delete_action = menu.addAction("Delete state")
        else:
            delete_action = None
        
        action = menu.exec(event.screenPos())
        
        if action == create_transition_action:
            self.create_transition_requested.emit()
        elif action == entry_action and not self.state.is_entry_point:
            self.set_as_entry_point()
        elif action == delete_action:
            # Ask the view to delete this node
            if self.view:
                self.view.delete_state(self)

    def set_as_entry_point(self):
        """Sets this state as entry point"""
        if self.view and self.view.fsm:
            # Update in the model
            self.view.fsm.set_entry_point(self.state)

            # Update appearance of all nodes
            for item in self.view.scene.items():
                if isinstance(item, StateNode):
                    item.update_appearance()

    def itemChange(self, change, value):
        if change == QGraphicsRectItem.ItemPositionHasChanged:
            for edge in self.edges:
                edge.update_position()

        return super().itemChange(change, value)

    def contextMenuEvent(self, event):
        # Context menu is handled by mousePressEvent
        pass
