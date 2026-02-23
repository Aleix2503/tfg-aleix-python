from PySide6.QtWidgets import QGraphicsRectItem, QGraphicsTextItem
from PySide6.QtCore import Qt

class StateNode(QGraphicsRectItem):
    def __init__(self, state):
        super().__init__(0, 0, 120, 50)

        self.state = state
        self.edges = []

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

    def itemChange(self, change, value):
        if change == QGraphicsRectItem.ItemPositionHasChanged:  
            for edge in self.edges:
                edge.update_position()

        return super().itemChange(change, value)
