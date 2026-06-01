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
        """Ensures the arrow is drawn even if not yet added to scene"""
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
        """Detects if this is a self-transition (same source and target)"""
        return self.source == self.target

    def has_reverse_transition(self):
        """Detects if there is a transition in the reverse direction"""
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

        # Create path based on transition type
        path = QPainterPath()

        # Detect if it's a self-transition
        if self.is_self_transition():
            # Draw a circular arc for self-transition
            # Exit point at the top edge of the node
            rect = self.source.sceneBoundingRect()
            exit_point = QPointF(p1_center.x(), p1_center.y() - rect.height() / 2 - 10)

            # Start from the state edge
            path.moveTo(exit_point)

            # Create an arc that goes out and comes back
            radius = 60
            arc_rect = QPointF(p1_center.x() - radius, p1_center.y() - radius - rect.height() / 2 - 10)
            path.arcTo(arc_rect.x(), arc_rect.y(), radius * 2, radius * 2, 90, -180)

            # Draw arrow at the end of the arc
            arrow_end = QPointF(p1_center.x(), p1_center.y() - rect.height() / 2 - 10)
            self.draw_self_transition_arrow(path, arrow_end, p1_center)
        else:
            # Check if there is a reverse transition
            has_reverse = self.has_reverse_transition()

            # Calculate intersection points at state edges
            p1 = self._get_state_intersection(p2_center, p1_center, source_rect.width(), source_rect.height())
            p2 = self._get_state_intersection(p1_center, p2_center, target_rect.width(), target_rect.height())

            path.moveTo(p1)

            if has_reverse:
                # Create a curve (arc)
                # Calculate control point for the curve
                dx = p2.x() - p1.x()
                dy = p2.y() - p1.y()

                # Perpendicular to the vector
                perp_x = -dy
                perp_y = dx
                length = math.sqrt(perp_x*perp_x + perp_y*perp_y)

                if length > 0:
                    perp_x /= length
                    perp_y /= length

                # Offset control point
                offset = 30
                control_x = (p1.x() + p2.x()) / 2 + perp_x * offset
                control_y = (p1.y() + p2.y()) / 2 + perp_y * offset

                path.quadTo(control_x, control_y, p2.x(), p2.y())
            else:
                # Straight line
                path.lineTo(p2.x(), p2.y())

            self.draw_arrow(p1, p2, has_reverse)

        self.setPath(path)

    def _get_state_intersection(self, center, target_center, rect_width, rect_height):
        """Calculates the intersection point between the line and state rectangle edge"""
        dx = target_center.x() - center.x()
        dy = target_center.y() - center.y()

        if dx == 0 and dy == 0:
            return target_center

        # Calculate distance
        distance = math.sqrt(dx * dx + dy * dy)

        # Normalize direction
        dx_norm = dx / distance
        dy_norm = dy / distance

        # State is a rectangle, calculate where the line touches the edge
        # Use half the width and height of the rectangle
        hw = rect_width / 2
        hh = rect_height / 2

        # Find parameter t where the line intersects the rectangle
        # Check which edge is touched first
        if dx_norm != 0:
            t_x = hw / abs(dx_norm)
        else:
            t_x = float('inf')

        if dy_norm != 0:
            t_y = hh / abs(dy_norm)
        else:
            t_y = float('inf')

        t = min(t_x, t_y)

        # Intersection point
        intersection = QPointF(
            target_center.x() - dx_norm * t,
            target_center.y() - dy_norm * t
        )

        return intersection

    def draw_self_transition_arrow(self, path, arrow_pos, node_center):
        """Draws an arrow for self-transitions"""
        # Remove previous arrow if exists
        if self.arrow and self.arrow.scene():
            self.arrow.scene().removeItem(self.arrow)

        # For self-transition, arrow points downward
        # Direction: top to bottom
        direction_x = 0
        direction_y = 1

        # Point where arrow starts
        arrow_start_x = arrow_pos.x()
        arrow_start_y = arrow_pos.y() + 15

        # Perpendicular for arrow wings
        px = -direction_y
        py = direction_x

        # Arrow points
        p1 = QPointF(arrow_start_x, arrow_start_y)
        p2 = QPointF(arrow_start_x + px * 8, arrow_start_y + py * 8)
        p3 = QPointF(arrow_start_x - px * 8, arrow_start_y - py * 8)

        # Create and draw polygon
        polygon = QPolygonF([p1, p2, p3])
        self.arrow = QGraphicsPolygonItem(polygon)
        self.arrow.setBrush(Qt.black)
        self.arrow.setPen(QPen(Qt.black, 1))
        # Arrow should appear above states, same level as transition lines
        self.arrow.setZValue(1)

        # Add to scene - use source node's scene as fallback
        scene = self.scene()
        if not scene and self.source.scene():
            scene = self.source.scene()

        if scene:
            scene.addItem(self.arrow)

    def draw_arrow(self, start, end, curved=False):
        """Draws an arrow at the end of the line, positioned at target state edge"""
        # Remove previous arrow if exists
        if self.arrow and self.arrow.scene():
            self.arrow.scene().removeItem(self.arrow)

        # Get target rectangle
        target_rect = self.target.sceneBoundingRect()
        target_center = target_rect.center()
        target_width = target_rect.width()
        target_height = target_rect.height()

        # Calculate intersection point with state edge
        arrow_end = self._get_state_intersection(start, target_center, target_width, target_height)

        # Calculate direction
        dx = arrow_end.x() - start.x()
        dy = arrow_end.y() - start.y()
        length = math.sqrt(dx*dx + dy*dy)

        if length == 0:
            return

        # Normalize
        dx /= length
        dy /= length

        # Point where arrow starts (20 pixels before intersection point)
        arrow_start_x = arrow_end.x() - dx * 20
        arrow_start_y = arrow_end.y() - dy * 20

        # Perpendicular for arrow wings
        px = -dy
        py = dx

        # Arrow points
        p1 = arrow_end
        p2 = QPointF(arrow_start_x + px * 8, arrow_start_y + py * 8)
        p3 = QPointF(arrow_start_x - px * 8, arrow_start_y - py * 8)

        # Create and draw polygon
        polygon = QPolygonF([p1, p2, p3])
        self.arrow = QGraphicsPolygonItem(polygon)
        self.arrow.setBrush(Qt.black)
        self.arrow.setPen(QPen(Qt.black, 1))
        # Arrow should appear above states, same level as transition lines
        self.arrow.setZValue(1)

        # Add to scene - use source node's scene as fallback
        scene = self.scene()
        if not scene and self.source.scene():
            scene = self.source.scene()

        if scene:
            scene.addItem(self.arrow)
