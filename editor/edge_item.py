from PySide6.QtWidgets import QGraphicsLineItem
from PySide6.QtGui import QPen
from PySide6.QtCore import Qt

class TransitionEdge(QGraphicsLineItem):
    def __init__(self, source_node, target_node, transition):
        super().__init__()

        self.source = source_node
        self.target = target_node
        self.transition = transition

        pen = QPen(Qt.black, 2)
        self.setPen(pen)

        self.setZValue(-1)

        self.setFlags(
            QGraphicsLineItem.ItemIsSelectable
        )

        self.update_position()

    def update_position(self):
        p1 = self.source.sceneBoundingRect().center()
        p2 = self.target.sceneBoundingRect().center()
        self.setLine(p1.x(), p1.y(), p2.x(), p2.y())
