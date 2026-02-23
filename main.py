import sys
from PySide6.QtWidgets import QApplication

from editor.window import MainWindow
from editor.node_item import StateNode
from model.fsm import FSM
from model.state import State

app = QApplication(sys.argv)

# FSM de prueba
fsm = FSM("TestFSM")

idle = State("Idle")
move = State("Move")
attack = State("Attack")

fsm.add_state(idle)
fsm.add_state(move)
fsm.add_state(attack)

# Ventana
window = MainWindow(fsm)

# Nodos visuales
node_idle = StateNode(idle)
node_move = StateNode(move)
node_attack = StateNode(attack)

node_idle.setPos(100, 250)
node_move.setPos(300, 250)
node_attack.setPos(500, 250)

window.graph.scene.addItem(node_idle)
window.graph.scene.addItem(node_move)
window.graph.scene.addItem(node_attack)

window.show()
sys.exit(app.exec())