import sys
from PySide6.QtWidgets import QApplication

from editor.window import MainWindow
from model.fsm import FSM
from persistence.project_loader import load_project

app = QApplication(sys.argv)

# Create initial FSM
fsm = FSM("FSM")

# Window
window = MainWindow(fsm)

# If a file was passed as an argument, load it
if len(sys.argv) > 1:
    file_path = sys.argv[1]
    try:
        # Clear scene
        window.graph.scene.clear()

        # Load project
        fsm = load_project(file_path, window.graph.scene)
        window.fsm = fsm
        window.graph.fsm = fsm
        window.current_file_path = file_path
        window._update_window_title()
        window.command_manager.clear()
        window._update_undo_redo_state()
    except Exception as e:
        pass

window.show()
sys.exit(app.exec())