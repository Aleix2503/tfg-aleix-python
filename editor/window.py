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
        self.current_file_path = None  # Track current file
        self.command_manager = CommandManager()  # Undo/Redo manager

        self._update_window_title()  # Initialize with correct title
        self.resize(1100, 600)


        # ─────────────────────────────────────
        # MENU BAR
        # ─────────────────────────────────────

        menu_bar = self.menuBar()

        # File Menu
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

        # Add actions to menu
        file_menu.addAction(new_fsm_action)
        file_menu.addAction(save_fsm_action)
        file_menu.addAction(save_fsm_as_action)
        file_menu.addAction(load_fsm_action)
        file_menu.addSeparator()
        file_menu.addAction(export_json_action)

        # Connect actions
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

        # Add actions to menu
        edit_menu.addAction(undo_action)
        edit_menu.addAction(redo_action)

        # Connect actions
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

        # Secondary layout for export button
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

        # Connect changes in inspector and graph to detect modifications
        self._connect_change_signals()

    def _connect_change_signals(self):
        """Connects change signals to detect modifications"""
        # When an element is selected, changes can be made
        # For now, we rely on user manually marking changes
        # but we can extend this if needed
        pass

    def undo(self):
        """Undoes the last action"""
        self.command_manager.undo()
        self._update_undo_redo_state()
        self.mark_modified()

    def redo(self):
        """Redoes the last undone action"""
        self.command_manager.redo()
        self._update_undo_redo_state()
        self.mark_modified()

    def _update_undo_redo_state(self):
        """Updates the state of Undo/Redo buttons"""
        self.undo_action.setEnabled(self.command_manager.can_undo())
        self.redo_action.setEnabled(self.command_manager.can_redo())

    def mark_modified(self):
        """Marks the project as modified"""
        if not self.is_modified:
            self.is_modified = True
            self._update_window_title()

    def mark_saved(self):
        """Marks the project as saved"""
        self.is_modified = False
        self._update_window_title()
        # Clear undo/redo history when saving (opcional)
        # self.command_manager.clear()

    def _update_window_title(self):
        """Updates the window title with the modification indicator"""
        if self.current_file_path:
            import os
            filename = os.path.basename(self.current_file_path)
            # Remove .fsmproj extension
            if filename.endswith(".fsmproj"):
                filename = filename[:-8]
            title = f"FSM - {filename}"
        else:
            title = "FSM - Untitled"

        if self.is_modified:
            title += "*"

        self.setWindowTitle(title)

    def closeEvent(self, event):
        """Prevents closing without saving if there are changes"""
        if self.is_modified:
            reply = QMessageBox.question(
                self,
                "Unsaved changes",
                "There are unsaved changes. Do you want to save them before closing?",
                QMessageBox.Save | QMessageBox.Discard | QMessageBox.Cancel
            )

            if reply == QMessageBox.Save:
                self.save_fsm()
                if self.is_modified:  # If not saved (user canceled), do not close
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

    def new_fsm(self):
        # Cancel transition creation if active
        if self.graph.creating_transition:
            self.graph.end_transition_creation()

        # Clear visual scene
        self.graph.scene.clear()

        # Create new empty FSM
        self.fsm = FSM("NewFSM")

        # Reassign FSM to GraphView
        self.graph.fsm = self.fsm

        # Create the visual node for ANY_STATE
        self.graph.setup_any_state()

        # Clear inspector
        self.inspector.clear()

        # Reset modification state
        self.current_file_path = None
        self.mark_saved()  # New project with no changes

        # Clear undo/redo history
        self.command_manager.clear()
        self._update_undo_redo_state()

    def save_fsm(self):
        """Saves current project. If no path, opens dialog"""
        if self.current_file_path:
            # Save directly to the current file
            self._save_to_path(self.current_file_path)
        else:
            # If no path, open "Save As" dialog
            self.save_fsm_as()

    def save_fsm_as(self):
        """Opens dialog to save with a new name/location"""
        path, _ = QFileDialog.getSaveFileName(
            self,
            "Save FSM Project As",
            "",
            "FSM Project (*.fsmproj)"
        )

        if not path:
            return

        # Add extension if missing
        if not path.endswith(".fsmproj"):
            path += ".fsmproj"

        self._save_to_path(path)

    def _save_to_path(self, path):
        """Saves the project at the specified path"""
        save_project(
            self.fsm,
            self.graph.scene,
            path
        )

        # Update state
        self.current_file_path = path
        self.mark_saved()

    def load_fsm(self):
        path, _ = QFileDialog.getOpenFileName(
            self,
            "Load FSM Project",
            "",
            "FSM Project (*.fsmproj)"
        )

        if not path:
            return

        # Clear current scene
        self.graph.scene.clear()

        # Load FSM
        self.fsm = load_project(
            path,
            self.graph.scene
        )

        # Reassign reference
        self.graph.fsm = self.fsm

        # Clear inspector
        self.inspector.clear()

        # Update state
        self.current_file_path = path
        self.mark_saved()  # Newly loaded project, no changes

        # Clear undo/redo history
        self.command_manager.clear()
        self._update_undo_redo_state()