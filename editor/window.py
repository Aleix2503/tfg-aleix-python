from PySide6.QtWidgets import QMainWindow, QWidget, QHBoxLayout, QFileDialog, QVBoxLayout
from PySide6.QtGui import QAction
from .graph_view import GraphView
from .inspector import Inspector
import json
from persistence.project_serializer import save_project
from persistence.project_loader import load_project
from model.fsm import FSM

class MainWindow(QMainWindow):
    def __init__(self, fsm):
        super().__init__()

        self.fsm = fsm 

        self.setWindowTitle("FSM Visual Editor")
        self.resize(1100, 600)


        # ─────────────────────────────────────
        # MENU BAR
        # ─────────────────────────────────────

        menu_bar = self.menuBar()

        # Menú File
        file_menu = menu_bar.addMenu("File")

        # Actions
        new_fsm_action = QAction("New FSM", self)
        save_fsm_action = QAction("Save FSM", self)
        load_fsm_action = QAction("Load FSM", self)
        export_json_action = QAction("Export JSON", self)

        # Shortcuts
        new_fsm_action.setShortcut("Ctrl+N")
        save_fsm_action.setShortcut("Ctrl+S")
        load_fsm_action.setShortcut("Ctrl+O")
        export_json_action.setShortcut("Ctrl+E")

        # Añadir acciones al menú
        file_menu.addAction(new_fsm_action)
        file_menu.addAction(save_fsm_action)
        file_menu.addAction(load_fsm_action)
        file_menu.addSeparator()
        file_menu.addAction(export_json_action)

        # Conectar acciones
        new_fsm_action.triggered.connect(self.new_fsm)
        save_fsm_action.triggered.connect(self.save_fsm)
        load_fsm_action.triggered.connect(self.load_fsm)
        export_json_action.triggered.connect(self.export_json)



        central = QWidget()
        self.setCentralWidget(central)

        #Layout principal
        layout = QHBoxLayout()
        central.setLayout(layout)

        #Layout secundario para botón de exportar
        v_layout = QVBoxLayout()

        self.inspector = Inspector()
        self.graph = GraphView(
            inspector=self.inspector,
            fsm=self.fsm
        )

        v_layout.addWidget(self.graph, 3)

        layout.addLayout(v_layout, 3)
        layout.addWidget(self.inspector, 1)

    
    def export_json(self):
        if not self.fsm:
            return

        path, _ = QFileDialog.getSaveFileName(
            self,
            "Export FSM",
            "",
            "JSON Files (*.json)"
        )

        if not path:
            return

        data = self.fsm.to_dict()

        with open(path, "w", encoding="utf-8") as f:
            json.dump(data, f, indent=4)

        print("FSM exported to:", path)

    def new_fsm(self):
        print("NEW FSM")

        # Cancelar creación de transición si estaba activa
        if self.graph.creating_transition:
            self.graph.end_transition_creation()

        # Limpiar escena visual
        self.graph.scene.clear()

        # Crear nueva FSM vacía
        self.fsm = FSM("NewFSM")

        # Reasignar FSM al GraphView
        self.graph.fsm = self.fsm

        # Limpiar inspector
        self.inspector.clear()

        print("New FSM created")

    def save_fsm(self):
        path, _ = QFileDialog.getSaveFileName(
            self,
            "Save FSM Project",
            "",
            "FSM Project (*.fsmproj)"
        )

        if not path:
            return

        # Añadir extensión si falta
        if not path.endswith(".fsmproj"):
            path += ".fsmproj"

        save_project(
            self.fsm,
            self.graph.scene,
            path
        )

    def load_fsm(self):
        path, _ = QFileDialog.getOpenFileName(
            self,
            "Load FSM Project",
            "",
            "FSM Project (*.fsmproj)"
        )

        if not path:
            return

        # Limpiar escena actual
        self.graph.scene.clear()

        # Cargar FSM
        self.fsm = load_project(
            path,
            self.graph.scene
        )

        # Reasignar referencia
        self.graph.fsm = self.fsm

        print("FSM loaded:", path)