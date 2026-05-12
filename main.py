import sys
from PySide6.QtWidgets import QApplication

from editor.window import MainWindow
from model.fsm import FSM

app = QApplication(sys.argv)

# FSM
fsm = FSM("FSM")

# Ventana
window = MainWindow(fsm)
window.show()
sys.exit(app.exec())