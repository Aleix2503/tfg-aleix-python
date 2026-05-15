import sys
from PySide6.QtWidgets import QApplication

from editor.window import MainWindow
from model.fsm import FSM
from persistence.project_loader import load_project

app = QApplication(sys.argv)

# Crear FSM inicial
fsm = FSM("FSM")

# Ventana
window = MainWindow(fsm)

# Si se pasó un archivo como argumento, cargarlo
if len(sys.argv) > 1:
    file_path = sys.argv[1]
    try:
        # Limpiar escena
        window.graph.scene.clear()

        # Cargar proyecto
        fsm = load_project(file_path, window.graph.scene)
        window.fsm = fsm
        window.graph.fsm = fsm
        window.current_file_path = file_path
        window._update_window_title()
        window.command_manager.clear()
        window._update_undo_redo_state()

        print(f"Archivo cargado: {file_path}")
    except Exception as e:
        print(f"Error al cargar el archivo: {e}")

window.show()
sys.exit(app.exec())