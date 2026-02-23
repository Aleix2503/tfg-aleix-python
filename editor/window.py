from PySide6.QtWidgets import QMainWindow, QWidget, QHBoxLayout, QFileDialog, QPushButton, QVBoxLayout
from .graph_view import GraphView
from .inspector import Inspector
import json

class MainWindow(QMainWindow):
    def __init__(self, fsm):
        super().__init__()

        self.fsm = fsm 

        self.setWindowTitle("FSM Visual Editor")
        self.resize(1100, 600)

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

        self.export_button = QPushButton("Export JSON")
        self.export_button.clicked.connect(self.export_json)

        v_layout.addWidget(self.graph, 3)
        v_layout.addWidget(self.export_button)

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

