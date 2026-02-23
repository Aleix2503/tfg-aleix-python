from PySide6.QtWidgets import QGraphicsView, QGraphicsScene
from PySide6.QtGui import QPainter
from PySide6.QtCore import Qt

from editor.edge_item import TransitionEdge
from model.transition import Transition
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

        self.transition_source = None  # 👈 estado origen

    def on_selection_changed(self):
        if not self.inspector:
            return

        selected = self.scene.selectedItems()
        if selected:
            self.inspector.inspect(selected[0])
        else:
            self.inspector.clear()

    def mousePressEvent(self, event):
        item = self.itemAt(event.pos())

        # Click derecho → marcar origen
        if event.button() == Qt.RightButton and isinstance(item, StateNode):
            self.transition_source = item
            item.setBrush(Qt.yellow)
            return

        # Click izquierdo → crear transición
        if (
            event.button() == Qt.LeftButton
            and self.transition_source
            and isinstance(item, StateNode)
            and item != self.transition_source
        ):
            self.create_transition(self.transition_source, item)
            self.transition_source.setBrush(Qt.lightGray)
            self.transition_source = None
            return

        super().mousePressEvent(event)

    def create_transition(self, source_node, target_node):
        transition = Transition(
            source_node.state,
            target_node.state
        )

        self.fsm.add_transition(transition)

        edge = TransitionEdge(source_node, target_node, transition)
        source_node.add_edge(edge)
        target_node.add_edge(edge)

        self.scene.addItem(edge)
