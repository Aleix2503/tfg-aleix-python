from PySide6.QtWidgets import QGraphicsPathItem, QGraphicsPolygonItem
from PySide6.QtGui import QPen, QPolygonF, QPainterPath
from PySide6.QtCore import Qt, QPointF
import math

class TransitionEdge(QGraphicsPathItem):
    def __init__(self, source_node, target_node, transition):
        super().__init__()

        self.source = source_node
        self.target = target_node
        self.transition = transition
        
        self.arrow = None

        pen = QPen(Qt.black, 2)
        self.setPen(pen)

        self.setZValue(-1)

        self.setFlags(
            QGraphicsPathItem.ItemIsSelectable
        )

        self.update_position()

    def has_reverse_transition(self):
        """Detecta si existe una transición en dirección inversa"""
        for trans in self.source.edges:
            if hasattr(trans, 'target') and trans.target == self.source and \
               hasattr(trans, 'source') and trans.source == self.target:
                return True
        return False

    def update_position(self):
        p1 = self.source.sceneBoundingRect().center()
        p2 = self.target.sceneBoundingRect().center()
        
        # Detectar si hay transición inversa
        has_reverse = self.has_reverse_transition()
        
        # Crear camino (línea recta o curva)
        path = QPainterPath()
        path.moveTo(p1)
        
        if has_reverse:
            # Hacer una curva (arco)
            # Calcular punto de control para la curva
            dx = p2.x() - p1.x()
            dy = p2.y() - p1.y()
            
            # Perpendicular al vector
            perp_x = -dy
            perp_y = dx
            length = math.sqrt(perp_x*perp_x + perp_y*perp_y)
            
            if length > 0:
                perp_x /= length
                perp_y /= length
            
            # Punto de control desplazado
            offset = 30
            control_x = (p1.x() + p2.x()) / 2 + perp_x * offset
            control_y = (p1.y() + p2.y()) / 2 + perp_y * offset
            
            path.quadTo(control_x, control_y, p2.x(), p2.y())
        else:
            # Línea recta
            path.lineTo(p2.x(), p2.y())
        
        self.setPath(path)
        
        # Dibujar flecha
        self.draw_arrow(p1, p2, has_reverse)

    def draw_arrow(self, start, end, curved=False):
        """Dibuja una flecha al final de la línea"""
        # Eliminar flecha anterior si existe
        if self.arrow and self.arrow.scene():
            self.arrow.scene().removeItem(self.arrow)
        
        # Calcular dirección
        dx = end.x() - start.x()
        dy = end.y() - start.y()
        length = math.sqrt(dx*dx + dy*dy)
        
        if length == 0:
            return
        
        # Normalizar
        dx /= length
        dy /= length
        
        # Punto donde empieza la flecha (20 píxeles antes del target)
        arrow_start_x = end.x() - dx * 20
        arrow_start_y = end.y() - dy * 20
        
        # Perpendicular para las alas de la flecha
        px = -dy
        py = dx
        
        # Puntos de la flecha
        p1 = QPointF(end.x(), end.y())
        p2 = QPointF(arrow_start_x + px * 8, arrow_start_y + py * 8)
        p3 = QPointF(arrow_start_x - px * 8, arrow_start_y - py * 8)
        
        # Crear polígono y dibujarlo
        polygon = QPolygonF([p1, p2, p3])
        self.arrow = QGraphicsPolygonItem(polygon)
        self.arrow.setBrush(Qt.black)
        self.arrow.setPen(QPen(Qt.black, 1))
        self.arrow.setZValue(0)
        
        # Agregar a la escena
        if self.scene():
            self.scene().addItem(self.arrow)
