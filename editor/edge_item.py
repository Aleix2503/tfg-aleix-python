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

        # Z-order: lines should be above states (states default to 0)
        self.setZValue(1)

        self.setFlags(
            QGraphicsPathItem.ItemIsSelectable
        )

        # Update position first to set the path
        self.update_position()

        # If we're added to a scene, draw the arrow immediately
        # Otherwise, the arrow will be drawn when the path is set
        self._ensure_arrow_drawn()

    def _ensure_arrow_drawn(self):
        """Asegura que la flecha se dibuje incluso si aún no se ha añadido a la escena"""
        if self.arrow is None:
            # Trigger arrow drawing by re-calling update_position logic
            if self.is_self_transition():
                source_rect = self.source.sceneBoundingRect()
                p1_center = source_rect.center()
                exit_point = QPointF(p1_center.x(), p1_center.y() - source_rect.height() / 2 - 10)
                self.draw_self_transition_arrow(self.path(), exit_point, p1_center)
            else:
                source_rect = self.source.sceneBoundingRect()
                target_rect = self.target.sceneBoundingRect()
                p1_center = source_rect.center()
                p2_center = target_rect.center()

                p1 = self._get_state_intersection(p2_center, p1_center, source_rect.width(), source_rect.height())
                p2 = self._get_state_intersection(p1_center, p2_center, target_rect.width(), target_rect.height())

                has_reverse = self.has_reverse_transition()
                self.draw_arrow(p1, p2, has_reverse)

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
        source_rect = self.source.sceneBoundingRect()
        target_rect = self.target.sceneBoundingRect()

        p1_center = source_rect.center()
        p2_center = target_rect.center()

        # Crear camino según tipo de transición
        path = QPainterPath()

        # Detectar si es auto-transición
        if self.is_self_transition():
            # Dibujar un arco circular para la auto-transición
            # El punto de salida es en el borde superior del nodo
            rect = self.source.sceneBoundingRect()
            exit_point = QPointF(p1_center.x(), p1_center.y() - rect.height() / 2 - 10)

            # Comenzar desde el borde del estado
            path.moveTo(exit_point)

            # Crear un arco que sale del nodo y vuelve
            radius = 60
            arc_rect = QPointF(p1_center.x() - radius, p1_center.y() - radius - rect.height() / 2 - 10)
            path.arcTo(arc_rect.x(), arc_rect.y(), radius * 2, radius * 2, 90, -180)

            # Dibujar flecha en el final del arco
            arrow_end = QPointF(p1_center.x(), p1_center.y() - rect.height() / 2 - 10)
            self.draw_self_transition_arrow(path, arrow_end, p1_center)
        else:
            # Detectar si hay transición inversa
            has_reverse = self.has_reverse_transition()

            # Calcular puntos de intersección en los bordes
            p1 = self._get_state_intersection(p2_center, p1_center, source_rect.width(), source_rect.height())
            p2 = self._get_state_intersection(p1_center, p2_center, target_rect.width(), target_rect.height())

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

            self.draw_arrow(p1, p2, has_reverse)

        self.setPath(path)

    def _get_state_intersection(self, center, target_center, rect_width, rect_height):
        """Calcula el punto de intersección entre la línea y el borde del rectángulo del estado"""
        dx = target_center.x() - center.x()
        dy = target_center.y() - center.y()

        if dx == 0 and dy == 0:
            return target_center

        # Calcular distancia
        distance = math.sqrt(dx * dx + dy * dy)

        # Normalizar dirección
        dx_norm = dx / distance
        dy_norm = dy / distance

        # El estado es un rectángulo, calcular el punto donde la línea toca el borde
        # Usar la mitad del ancho y altura del rectángulo
        hw = rect_width / 2
        hh = rect_height / 2

        # Encontrar el parámetro t donde la línea intersecta el rectángulo
        # Basarse en cuál borde se toca primero
        if dx_norm != 0:
            t_x = hw / abs(dx_norm)
        else:
            t_x = float('inf')

        if dy_norm != 0:
            t_y = hh / abs(dy_norm)
        else:
            t_y = float('inf')

        t = min(t_x, t_y)

        # Punto de intersección
        intersection = QPointF(
            target_center.x() - dx_norm * t,
            target_center.y() - dy_norm * t
        )

        return intersection

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
        # Arrow should appear above states, same level as transition lines
        self.arrow.setZValue(1)

        # Agregar a la escena - usar la escena del nodo source como fallback
        scene = self.scene()
        if not scene and self.source.scene():
            scene = self.source.scene()

        if scene:
            scene.addItem(self.arrow)

    def draw_arrow(self, start, end, curved=False):
        """Dibuja una flecha al final de la línea, posicionada en el borde del estado destino"""
        # Eliminar flecha anterior si existe
        if self.arrow and self.arrow.scene():
            self.arrow.scene().removeItem(self.arrow)

        # Obtener el rectángulo del target
        target_rect = self.target.sceneBoundingRect()
        target_center = target_rect.center()
        target_width = target_rect.width()
        target_height = target_rect.height()

        # Calcular el punto de intersección con el borde del estado
        arrow_end = self._get_state_intersection(start, target_center, target_width, target_height)

        # Calcular dirección
        dx = arrow_end.x() - start.x()
        dy = arrow_end.y() - start.y()
        length = math.sqrt(dx*dx + dy*dy)

        if length == 0:
            return

        # Normalizar
        dx /= length
        dy /= length

        # Punto donde empieza la flecha (20 píxeles antes del punto de intersección)
        arrow_start_x = arrow_end.x() - dx * 20
        arrow_start_y = arrow_end.y() - dy * 20

        # Perpendicular para las alas de la flecha
        px = -dy
        py = dx

        # Puntos de la flecha
        p1 = arrow_end
        p2 = QPointF(arrow_start_x + px * 8, arrow_start_y + py * 8)
        p3 = QPointF(arrow_start_x - px * 8, arrow_start_y - py * 8)

        # Crear polígono y dibujarlo
        polygon = QPolygonF([p1, p2, p3])
        self.arrow = QGraphicsPolygonItem(polygon)
        self.arrow.setBrush(Qt.black)
        self.arrow.setPen(QPen(Qt.black, 1))
        # Arrow should appear above states, same level as transition lines
        self.arrow.setZValue(1)

        # Agregar a la escena - usar la escena del nodo source como fallback
        scene = self.scene()
        if not scene and self.source.scene():
            scene = self.source.scene()

        if scene:
            scene.addItem(self.arrow)
