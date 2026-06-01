from PySide6.QtWidgets import QMainWindow, QWidget, QHBoxLayout, QFileDialog, QVBoxLayout, QMessageBox
from PySide6.QtGui import QAction
from .graph_view import GraphView
from .inspector import Inspector
import json
from persistence.project_serializer import save_project
from persistence.project_loader import load_project
from model.fsm import FSM
from commands import CommandManager

class MainWindow(QMainWindow):
    def __init__(self, fsm):
        super().__init__()

        self.fsm = fsm
        self.is_modified = False
        self.current_file_path = None  # Para rastrear el archivo actual
        self.command_manager = CommandManager()  # Gestor de Undo/Redo

        self._update_window_title()  # Inicializar con título correcto
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
        save_fsm_as_action = QAction("Save FSM As...", self)
        load_fsm_action = QAction("Load FSM", self)
        export_json_action = QAction("Export JSON", self)

        # Shortcuts
        new_fsm_action.setShortcut("Ctrl+N")
        save_fsm_action.setShortcut("Ctrl+S")
        save_fsm_as_action.setShortcut("Ctrl+Shift+S")
        load_fsm_action.setShortcut("Ctrl+O")
        export_json_action.setShortcut("Ctrl+E")

        # Añadir acciones al menú
        file_menu.addAction(new_fsm_action)
        file_menu.addAction(save_fsm_action)
        file_menu.addAction(save_fsm_as_action)
        file_menu.addAction(load_fsm_action)
        file_menu.addSeparator()
        file_menu.addAction(export_json_action)

        # Conectar acciones
        new_fsm_action.triggered.connect(self.new_fsm)
        save_fsm_action.triggered.connect(self.save_fsm)
        save_fsm_as_action.triggered.connect(self.save_fsm_as)
        load_fsm_action.triggered.connect(self.load_fsm)
        export_json_action.triggered.connect(self.export_json)

        # ─────────────────────────────────────
        # MENU EDIT
        # ─────────────────────────────────────

        edit_menu = menu_bar.addMenu("Edit")

        # Actions
        undo_action = QAction("Undo", self)
        redo_action = QAction("Redo", self)

        # Shortcuts
        undo_action.setShortcut("Ctrl+Z")
        redo_action.setShortcut("Ctrl+Shift+Z")

        # Añadir acciones al menú
        edit_menu.addAction(undo_action)
        edit_menu.addAction(redo_action)

        # Conectar acciones
        undo_action.triggered.connect(self.undo)
        redo_action.triggered.connect(self.redo)

        # Guardar referencias para habilitar/deshabilitar
        self.undo_action = undo_action
        self.redo_action = redo_action
        self._update_undo_redo_state()

        central = QWidget()
        self.setCentralWidget(central)

        #Layout principal
        layout = QHBoxLayout()
        layout.setContentsMargins(0, 0, 0, 0)
        central.setLayout(layout)

        #Layout secundario para botón de exportar
        v_layout = QVBoxLayout()

        self.inspector = Inspector(on_change_callback=self.mark_modified)
        # Clear inspector at startup so it shows empty
        self.inspector.clear()

        self.graph = GraphView(
            inspector=self.inspector,
            fsm=self.fsm,
            on_change_callback=self.mark_modified,
            command_manager=self.command_manager,
            on_command_executed=self._update_undo_redo_state
        )

        v_layout.addWidget(self.graph, 3)
        v_layout.addStretch()

        layout.addLayout(v_layout, 3)
        layout.addWidget(self.inspector, 1)

        # Conectar cambios en el inspector y graph para detectar modificaciones
        self._connect_change_signals()

    def _connect_change_signals(self):
        """Conecta señales de cambio para detectar modificaciones"""
        # Cuando se selecciona un elemento, se pueden hacer cambios
        # Por ahora, confiaremos en que el usuario marca los cambios manualmente
        # pero podemos extender esto si es necesario
        pass

    def undo(self):
        """Deshace la última acción"""
        self.command_manager.undo()
        self._update_undo_redo_state()
        self.mark_modified()

    def redo(self):
        """Rehace la última acción deshecha"""
        self.command_manager.redo()
        self._update_undo_redo_state()
        self.mark_modified()

    def _update_undo_redo_state(self):
        """Actualiza el estado de los botones Undo/Redo"""
        self.undo_action.setEnabled(self.command_manager.can_undo())
        self.redo_action.setEnabled(self.command_manager.can_redo())

    def mark_modified(self):
        """Marca el proyecto como modificado"""
        if not self.is_modified:
            self.is_modified = True
            self._update_window_title()

    def mark_saved(self):
        """Marca el proyecto como guardado"""
        self.is_modified = False
        self._update_window_title()
        # Limpiar el historial de undo/redo al guardar (opcional)
        # self.command_manager.clear()

    def _update_window_title(self):
        """Actualiza el título de la ventana con el indicador de cambios"""
        if self.current_file_path:
            import os
            filename = os.path.basename(self.current_file_path)
            # Remover extensión .fsmproj
            if filename.endswith(".fsmproj"):
                filename = filename[:-8]
            title = f"FSM - {filename}"
        else:
            title = "FSM - Untitled"

        if self.is_modified:
            title += "*"

        self.setWindowTitle(title)

    def closeEvent(self, event):
        """Previene cerrar sin guardar si hay cambios"""
        if self.is_modified:
            reply = QMessageBox.question(
                self,
                "Cambios sin guardar",
                "Hay cambios sin guardar. ¿Deseas guardarlos antes de cerrar?",
                QMessageBox.Save | QMessageBox.Discard | QMessageBox.Cancel
            )

            if reply == QMessageBox.Save:
                self.save_fsm()
                if self.is_modified:  # Si no se guardó (usuario canceló), no cerrar
                    event.ignore()
                else:
                    event.accept()
            elif reply == QMessageBox.Discard:
                event.accept()
            else:  # Cancel
                event.ignore()
        else:
            event.accept()

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

        # Crear el nodo visual del ANY_STATE
        self.graph.setup_any_state()

        # Limpiar inspector
        self.inspector.clear()

        # Resetear estado de modificación
        self.current_file_path = None
        self.mark_saved()  # Nuevo proyecto sin cambios

        # Limpiar historial de undo/redo
        self.command_manager.clear()
        self._update_undo_redo_state()

        print("New FSM created")

    def save_fsm(self):
        """Guarda el proyecto actual. Si no tiene ruta, abre diálogo"""
        if self.current_file_path:
            # Guardar directamente en el archivo actual
            self._save_to_path(self.current_file_path)
        else:
            # Si no hay ruta, abrir diálogo "Guardar Como"
            self.save_fsm_as()

    def save_fsm_as(self):
        """Abre diálogo para guardar con un nuevo nombre/ubicación"""
        path, _ = QFileDialog.getSaveFileName(
            self,
            "Save FSM Project As",
            "",
            "FSM Project (*.fsmproj)"
        )

        if not path:
            return

        # Añadir extensión si falta
        if not path.endswith(".fsmproj"):
            path += ".fsmproj"

        self._save_to_path(path)

    def _save_to_path(self, path):
        """Guarda el proyecto en la ruta especificada"""
        save_project(
            self.fsm,
            self.graph.scene,
            path
        )

        # Actualizar estado
        self.current_file_path = path
        self.mark_saved()
        print(f"FSM saved to: {path}")

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

        # Limpiar inspector
        self.inspector.clear()

        # Actualizar estado
        self.current_file_path = path
        self.mark_saved()  # Proyecto recién cargado, sin cambios

        # Limpiar historial de undo/redo
        self.command_manager.clear()
        self._update_undo_redo_state()

        print("FSM loaded:", path)