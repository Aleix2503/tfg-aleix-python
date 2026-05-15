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

    def is_self_transition(self):
        """Detecta si es una auto-transición (misma fuente y destino)"""
        return self.source == self.target

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

        # Crear camino según tipo de transición
        path = QPainterPath()
        path.moveTo(p1)

        # Detectar si es auto-transición
        if self.is_self_transition():
            # Dibujar un arco circular para la auto-transición
            rect = self.source.sceneBoundingRect()
            # Crear un arco que sale del nodo y vuelve
            radius = 60

            # Punto de salida (arriba del nodo)
            exit_point = QPointF(p1.x(), p1.y() - rect.height() / 2 - 10)

            # Crear el arco
            arc_rect = QPointF(p1.x() - radius, p1.y() - radius - rect.height() / 2 - 10)

            path.arcTo(arc_rect.x(), arc_rect.y(), radius * 2, radius * 2, 90, -180)

            # Dibujar flecha en el final del arco
            arrow_end = QPointF(p1.x(), p1.y() - rect.height() / 2 - 10)
            self.draw_self_transition_arrow(path, arrow_end, p1)
        else:
            # Detectar si hay transición inversa
            has_reverse = self.has_reverse_transition()

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

            self.draw_arrow(p1, p2, has_reverse)

        self.setPath(path)

    def draw_self_transition_arrow(self, path, arrow_pos, node_center):
        """Dibuja una flecha para auto-transiciones"""
        # Eliminar flecha anterior si existe
        if self.arrow and self.arrow.scene():
            self.arrow.scene().removeItem(self.arrow)

        # Para auto-transición, la flecha sale hacia abajo
        # Dirección: de arriba hacia abajo
        direction_x = 0
        direction_y = 1

        # Punto donde empieza la flecha
        arrow_start_x = arrow_pos.x()
        arrow_start_y = arrow_pos.y() + 15

        # Perpendicular para las alas de la flecha
        px = -direction_y
        py = direction_x

        # Puntos de la flecha
        p1 = QPointF(arrow_start_x, arrow_start_y)
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
