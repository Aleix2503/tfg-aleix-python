from PySide6.QtWidgets import (
    QWidget, QVBoxLayout, QLabel, QListWidget,
    QPushButton, QHBoxLayout, QTableWidget, QSpinBox,
    QTableWidgetItem, QLineEdit, QComboBox, QCompleter,
    QDoubleSpinBox, QCheckBox, QScrollArea, QTreeWidget, QTreeWidgetItem
)
from PySide6.QtCore import Qt, QStringListModel

from editor.node_item import StateNode
from editor.edge_item import TransitionEdge
from model.action import Action
from model.condition import GenericCondition, LogicalCondition
from data.condition_registry import CONDITION_REGISTRY, ALL_CONDITIONS
from data.action_registry import ACTION_REGISTRY, ALL_ACTIONS
from data.variable_registry import VARIABLE_REGISTRY, ALL_VARIABLES


class Inspector(QWidget):
    def __init__(self, on_change_callback=None):
        super().__init__()

        self.current_state = None
        self.current_node = None
        self.current_action = None
        self.current_transition = None
        self.current_condition = None
        self.any_state_info_label = None  # Rastreador para el label del ANY_STATE
        self.global_state_info_label = None  # Rastreador para el label del Global State
        self.on_change_callback = on_change_callback  # Callback para notificar cambios

        # Main layout para el widget del Inspector
        main_layout = QVBoxLayout(self)
        main_layout.setContentsMargins(0, 0, 0, 0)
        
        # Crear un QScrollArea
        scroll_area = QScrollArea()
        scroll_area.setWidgetResizable(True)
        scroll_area.setStyleSheet("QScrollArea { border: none; }")
        
        # Crear widget contenedor para el contenido scrolleable
        scroll_content = QWidget()
        self.layout = QVBoxLayout(scroll_content)
        
        # Add container widget to QScrollArea
        scroll_area.setWidget(scroll_content)
        
        # Add QScrollArea to main layout
        main_layout.addWidget(scroll_area)
        
        self.title = QLabel("Inspector")
        self.title.hide()
        self.layout.addWidget(self.title)
        
        # Store widget groups by section
        self.state_widgets = []
        self.transition_widgets = []
        self.action_param_widgets = []  # Widgets that are only shown when an action is selected

        # ─────────────────────────────────────
        # SECTION: STATE (STATE)
        # ─────────────────────────────────────

        # --- STATE NAME ---
        self.state_name_label = QLabel("State Name")
        self.layout.addWidget(self.state_name_label)
        self.state_widgets.append(self.state_name_label)
        
        self.state_name_input = QLineEdit()
        self.state_name_input.setPlaceholderText("Enter state name")
        self.layout.addWidget(self.state_name_input)
        self.state_name_input.textChanged.connect(self.on_state_name_changed)
        self.state_widgets.append(self.state_name_input)

        # --- ENTER ---
        self.enter_label = QLabel("Enter")
        self.layout.addWidget(self.enter_label)
        self.state_widgets.append(self.enter_label)
        
        self.enter_list = QListWidget()
        self.enter_list.setMinimumHeight(100)
        self.enter_list.setMaximumHeight(100)
        self.layout.addWidget(self.enter_list)
        self.state_widgets.append(self.enter_list)

        enter_buttons = QHBoxLayout()
        self.enter_add = QPushButton("+")
        self.enter_remove = QPushButton("-")
        enter_buttons.addWidget(self.enter_add)
        enter_buttons.addWidget(self.enter_remove)
        self.layout.addLayout(enter_buttons)
        self.state_widgets.append(enter_buttons)

        # --- TICK ---
        self.tick_label = QLabel("Tick")
        self.layout.addWidget(self.tick_label)
        self.state_widgets.append(self.tick_label)
        
        self.tick_list = QListWidget()
        self.tick_list.setMinimumHeight(100)
        self.tick_list.setMaximumHeight(100)
        self.layout.addWidget(self.tick_list)
        self.state_widgets.append(self.tick_list)

        tick_buttons = QHBoxLayout()
        self.tick_add = QPushButton("+")
        self.tick_remove = QPushButton("–")
        tick_buttons.addWidget(self.tick_add)
        tick_buttons.addWidget(self.tick_remove)
        self.layout.addLayout(tick_buttons)
        self.state_widgets.append(tick_buttons)

        # --- EXIT ---
        self.exit_label = QLabel("Exit")
        self.layout.addWidget(self.exit_label)
        self.state_widgets.append(self.exit_label)
        
        self.exit_list = QListWidget()
        self.exit_list.setMinimumHeight(100)
        self.exit_list.setMaximumHeight(100)
        self.layout.addWidget(self.exit_list)
        self.state_widgets.append(self.exit_list)

        exit_buttons = QHBoxLayout()
        self.exit_add = QPushButton("+")
        self.exit_remove = QPushButton("–")
        exit_buttons.addWidget(self.exit_add)
        exit_buttons.addWidget(self.exit_remove)
        self.layout.addLayout(exit_buttons)
        self.state_widgets.append(exit_buttons)

        # --- ACTION NAME ---
        self.action_name_label = QLabel("Action Name")
        self.layout.addWidget(self.action_name_label)
        self.state_widgets.append(self.action_name_label)

        self.action_name_input = QLineEdit()
        self.layout.addWidget(self.action_name_input)
        self.state_widgets.append(self.action_name_input)

        # Completer
        self.completer = QCompleter(ALL_ACTIONS)
        self.completer.setCaseSensitivity(Qt.CaseInsensitive)
        self.completer.setFilterMode(Qt.MatchContains)
        self.action_name_input.setCompleter(self.completer)

        self.action_save = QPushButton("Save Action")
        self.layout.addWidget(self.action_save)
        self.action_save.clicked.connect(self.save_action_name)
        self.action_save.clicked.connect(self._notify_change)
        self.state_widgets.append(self.action_save)

        # --- ACTION PARAMETERS ---
        self.action_params_label = QLabel("Action Parameters")
        self.layout.addWidget(self.action_params_label)
        self.action_param_widgets.append(self.action_params_label)

        # Parameters table
        self.params_table = QTableWidget()
        self.params_table.setColumnCount(2)
        self.params_table.setHorizontalHeaderLabels(["Name", "Value"])
        self.params_table.setMinimumHeight(150)
        self.params_table.setMaximumHeight(150)
        self.layout.addWidget(self.params_table)
        self.action_param_widgets.append(self.params_table)

        # Buttons to add/delete parameters
        param_buttons = QHBoxLayout()
        self.param_add = QPushButton("+ Param")
        self.param_remove = QPushButton("- Param")
        param_buttons.addWidget(self.param_add)
        param_buttons.addWidget(self.param_remove)
        self.layout.addLayout(param_buttons)
        self.action_param_widgets.append(param_buttons)

        self.param_add.clicked.connect(self.add_param)
        self.param_remove.clicked.connect(self.remove_param)

        # Flag to track if table is connected
        self.params_table_connected = True
        self.params_table.itemChanged.connect(self.on_param_table_changed)

        # Layout of auto-generated parameters
        self.params_layout = QVBoxLayout()
        self.layout.addLayout(self.params_layout)
        self.action_param_widgets.append(self.params_layout)
        self.param_widgets = {}

        # ─────────────────────────────────────
        # SECTION: TRANSITION (TRANSITION)
        # ─────────────────────────────────────

        self.cond_label = QLabel("Transition Condition Tree")
        self.layout.addWidget(self.cond_label)
        self.transition_widgets.append(self.cond_label)

        self.condition_tree = QTreeWidget()
        self.condition_tree.setHeaderLabels(["Condition"])
        self.condition_tree.setMinimumHeight(180)
        self.layout.addWidget(self.condition_tree)
        self.transition_widgets.append(self.condition_tree)

        condition_buttons = QHBoxLayout()

        self.set_root_simple_btn = QPushButton("Root Simple")
        self.set_root_and_btn = QPushButton("Root AND")
        self.set_root_or_btn = QPushButton("Root OR")
        self.set_root_not_btn = QPushButton("Root NOT")

        condition_buttons.addWidget(self.set_root_simple_btn)
        condition_buttons.addWidget(self.set_root_and_btn)
        condition_buttons.addWidget(self.set_root_or_btn)
        condition_buttons.addWidget(self.set_root_not_btn)

        self.layout.addLayout(condition_buttons)
        self.transition_widgets.append(condition_buttons)

        child_buttons = QHBoxLayout()

        self.add_simple_child_btn = QPushButton("+ Simple Child")
        self.add_and_child_btn = QPushButton("+ AND Child")
        self.add_or_child_btn = QPushButton("+ OR Child")
        self.remove_condition_btn = QPushButton("- Remove")

        child_buttons.addWidget(self.add_simple_child_btn)
        child_buttons.addWidget(self.add_and_child_btn)
        child_buttons.addWidget(self.add_or_child_btn)
        child_buttons.addWidget(self.remove_condition_btn)

        self.layout.addLayout(child_buttons)
        self.transition_widgets.append(child_buttons)

        self.cond_edit_label = QLabel("Edit Simple Condition")
        self.layout.addWidget(self.cond_edit_label)
        self.transition_widgets.append(self.cond_edit_label)

        self.cond_type = QComboBox()
        self.cond_type.addItems(ALL_CONDITIONS)
        self.layout.addWidget(self.cond_type)
        self.transition_widgets.append(self.cond_type)

        self.condition_params_layout = QVBoxLayout()
        self.layout.addLayout(self.condition_params_layout)
        self.transition_widgets.append(self.condition_params_layout)

        self.cond_save = QPushButton("Save Simple Condition")
        self.layout.addWidget(self.cond_save)
        self.transition_widgets.append(self.cond_save)

        self.condition_param_widgets = {}
        
        # Agregar stretch al final para que el contenido no se expanda
        self.layout.addStretch()
        
        # Ocultar todas las secciones inicialmente
        self._hide_all_sections()

        # ─────────────────────────────────────
        # CONEXIONES (al final del __init__)
        # ─────────────────────────────────────

        self.set_root_simple_btn.clicked.connect(self.set_root_simple_condition)
        self.set_root_and_btn.clicked.connect(lambda: self.set_root_logical_condition("AND"))
        self.set_root_or_btn.clicked.connect(lambda: self.set_root_logical_condition("OR"))
        self.set_root_not_btn.clicked.connect(lambda: self.set_root_logical_condition("NOT"))

        self.add_simple_child_btn.clicked.connect(self.add_simple_child_condition)
        self.add_and_child_btn.clicked.connect(lambda: self.add_logical_child_condition("AND"))
        self.add_or_child_btn.clicked.connect(lambda: self.add_logical_child_condition("OR"))

        self.remove_condition_btn.clicked.connect(self.remove_selected_condition)
        self.condition_tree.itemClicked.connect(self.select_condition_tree_item)

        self.cond_type.currentTextChanged.connect(self.generate_params_for_condition)
        self.cond_save.clicked.connect(self.save_simple_condition)

        
        self.enter_add.clicked.connect(lambda: self.add_action("enter"))
        self.enter_remove.clicked.connect(lambda: self.remove_action("enter"))
        self.tick_add.clicked.connect(lambda: self.add_action("tick"))
        self.tick_remove.clicked.connect(lambda: self.remove_action("tick"))
        self.exit_add.clicked.connect(lambda: self.add_action("exit"))
        self.exit_remove.clicked.connect(lambda: self.remove_action("exit"))

        self.enter_list.itemClicked.connect(
            lambda item: self.select_action("enter", item)
        )
        self.tick_list.itemClicked.connect(
            lambda item: self.select_action("tick", item)
        )
        self.exit_list.itemClicked.connect(
            lambda item: self.select_action("exit", item)
        )

        # Flag to track if table is connected
        self.params_table_connected = True
        self.params_table.itemChanged.connect(self.on_param_table_changed)

    def _hide_all_sections(self):
        for widget in self.state_widgets:
            if isinstance(widget, (QHBoxLayout, QVBoxLayout)):
                for i in range(widget.count()):
                    item = widget.itemAt(i)
                    if item.widget():
                        item.widget().hide()
            elif hasattr(widget, "hide"):
                widget.hide()

        for widget in self.transition_widgets:
            if isinstance(widget, (QHBoxLayout, QVBoxLayout)):
                for i in range(widget.count()):
                    item = widget.itemAt(i)
                    if item.widget():
                        item.widget().hide()
            elif hasattr(widget, "hide"):
                widget.hide()

        self.title.hide()

    def _show_state_section(self):
        """Shows the state section"""

        self._hide_all_sections()
        self.title.show()

        for widget in self.state_widgets:
            if isinstance(widget, (QHBoxLayout, QVBoxLayout)):
                for i in range(widget.count()):
                    item = widget.itemAt(i)
                    if item.widget():
                        item.widget().show()
            elif hasattr(widget, "show"):
                widget.show()

    def _show_transition_section(self):
        """Shows the transition section"""

        self._hide_all_sections()
        self.title.show()

        for widget in self.transition_widgets:
            if isinstance(widget, (QHBoxLayout, QVBoxLayout)):
                for i in range(widget.count()):
                    item = widget.itemAt(i)
                    if item.widget():
                        item.widget().show()
            elif hasattr(widget, "show"):
                widget.show()

    def _hide_action_params(self):
        """Hides the action parameters"""
        for widget in self.action_param_widgets:
            if isinstance(widget, QHBoxLayout) or isinstance(widget, QVBoxLayout):
                for i in range(widget.count()):
                    item = widget.itemAt(i)
                    if item.widget():
                        item.widget().hide()
            elif isinstance(widget, (QLabel, QTableWidget, QPushButton)):
                widget.hide()

    def _show_action_params(self):
        """Shows the action parameters"""
        for widget in self.action_param_widgets:
            if isinstance(widget, QHBoxLayout) or isinstance(widget, QVBoxLayout):
                for i in range(widget.count()):
                    item = widget.itemAt(i)
                    if item.widget():
                        item.widget().show()
            elif isinstance(widget, (QLabel, QTableWidget, QPushButton)):
                widget.show()


    # ------------------------

    # ─────────────────────────────────────
    # UTIL
    # ─────────────────────────────────────

    # ─────────────────────────────────────
    # ESTADO
    # ─────────────────────────────────────

    def clear(self):
        self.current_state = None
        self.current_node = None
        self.current_transition = None
        self.current_condition = None
        self.current_action = None
        
        # Clear ANY_STATE label if it exists
        if self.any_state_info_label is not None:
            self.layout.removeWidget(self.any_state_info_label)
            self.any_state_info_label.deleteLater()
            self.any_state_info_label = None
        if self.global_state_info_label is not None:
            self.layout.removeWidget(self.global_state_info_label)
            self.global_state_info_label.deleteLater()
            self.global_state_info_label = None
        
        self.enter_list.clear()
        self.tick_list.clear()
        self.exit_list.clear()
        self.state_name_input.clear()
        self.action_name_input.clear()
        self.condition_tree.clear()
        self.cond_type.setCurrentIndex(0)
        self.clear_layout(self.condition_params_layout)
        self.condition_param_widgets = {}
        self.params_table.setRowCount(0)
        self.clear_layout(self.params_layout)
        self._hide_action_params()
        self._hide_all_sections()


    def inspect(self, item):
        self.clear()

        if isinstance(item, StateNode):
            self.inspect_state(item)

        elif isinstance(item, TransitionEdge):
            self.inspect_transition(item)

    def inspect_state(self, node):
        self.current_node = node
        self.current_state = node.state
        
        # Limpiar label del ANY_STATE anterior si existe
        if self.any_state_info_label is not None:
            self.layout.removeWidget(self.any_state_info_label)
            self.any_state_info_label.deleteLater()
            self.any_state_info_label = None
        
        # Limpiar label del Global State anterior si existe
        if self.global_state_info_label is not None:
            self.layout.removeWidget(self.global_state_info_label)
            self.global_state_info_label.deleteLater()
            self.global_state_info_label = None

        # Si es ANY_STATE, mostrar mensaje especial
        if node.state.is_any_state:
            self.title.setText("ANY_STATE")
            self.title.show()
            # Hide all other sections
            self._hide_all_sections()
            
            # Show informational label
            self.any_state_info_label = QLabel("ANY_STATE: Global transitions that can be executed from any state.")
            self.any_state_info_label.setWordWrap(True)
            self.layout.insertWidget(1, self.any_state_info_label)
            return

        self.title.setText(f"State: {node.state.id}")
        
        # Show state section
        self._show_state_section()

        if node.state.is_global_state:
            self.global_state_info_label = QLabel(
                "Global State: can only have actions in Tick. Does not allow incoming or outgoing transitions."
            )
            self.global_state_info_label.setWordWrap(True)
            self.layout.insertWidget(1, self.global_state_info_label)

            # Ocultar secciones que no aplican
            self.enter_label.hide()
            self.enter_list.hide()
            self.enter_add.hide()
            self.enter_remove.hide()
            self.exit_label.hide()
            self.exit_list.hide()
            self.exit_add.hide()
            self.exit_remove.hide()

        # Mostrar campo de nombre
        self.state_name_input.blockSignals(True)
        self.state_name_input.setText(node.state.id)
        self.state_name_input.blockSignals(False)

        self.enter_list.clear()
        self.tick_list.clear()
        self.exit_list.clear()

        if not node.state.is_global_state:
            for a in node.state.enter:
                self.enter_list.addItem(str(a))
        
        for a in node.state.tick:
            self.tick_list.addItem(str(a))
        
        if not node.state.is_global_state:
            for a in node.state.exit:
                self.exit_list.addItem(str(a))

    def on_state_name_changed(self):
        if not self.current_state or not self.current_node:
            return

        new_name = self.state_name_input.text().strip()

        if not new_name:
            return

        # Actualizar el estado
        self.current_state.id = new_name

        # Actualizar el nodo visual
        self.current_node.text.setPlainText(new_name)

        # Update title
        self.title.setText(f"State: {new_name}")

    # ------------------------
    # ACCIONES
    # ------------------------

    def add_action(self, phase):
        if not self.current_state:
            return
        
        # Do not allow adding Enter/Exit to global states
        if self.current_state.is_global_state and phase in ("enter", "exit"):
            from PySide6.QtWidgets import QMessageBox
            QMessageBox.warning(
                self,
                "Action not allowed",
                "Global States can only have actions in Tick."
            )
            return

        action = Action("NewAction")

        action_list = getattr(self.current_state, phase)
        action_list.append(action)

        self.refresh()

    def remove_action(self, phase):
        if not self.current_state:
            return
        
        # No permitir eliminar Enter/Exit de global states
        if self.current_state.is_global_state and phase in ("enter", "exit"):
            return

        list_widget = getattr(self, f"{phase}_list")
        row = list_widget.currentRow()

        # 🔥 KEY: check valid selection
        if row < 0:
            return

        actions = getattr(self.current_state, phase)

        if row >= len(actions):
            return

        actions.pop(row)
        # self.params_table.setRowCount(0)
        self.refresh()

    def select_action(self, phase, item):
        index = getattr(self, f"{phase}_list").row(item)
        self.current_action = getattr(self.current_state, phase)[index]

        if not self.current_action:
            self.clear_layout(self.params_layout)
            self._hide_action_params()
            return

        # Mostrar nombre en el input
        self.action_name_input.blockSignals(True)
        self.action_name_input.setText(self.current_action.name)
        self.action_name_input.blockSignals(False)

        # Show parameters
        self._show_action_params()

        # Generate auto-widgets first
        self.generate_params_for_action(self.current_action.name)

        # Load parameters in table AFTER generating widgets
        self.refresh_params_table()

    def refresh(self):
        if self.current_node:
            node = self.current_node  # Guardar referencia antes de limpiar
            self.clear()
            self.inspect_state(node)

    def save_action_name(self):
        if not self.current_action:
            return

        name = self.action_name_input.text().strip()

        if not name:
            return

        self.current_action.name = name

        # Synchronize FIRST predefined parameters from widgets
        if self.param_widgets:
            self.sync_params_from_widgets()

        # THEN synchronize custom parameters from table
        self.sync_params_from_table()

        # Generar widgets tipados
        self.generate_params_for_action(name)

        self.refresh()

    # ─────────────────────────────────────
    # PARAMETERS
    # ─────────────────────────────────────

    def get_predefined_params(self, action_name):
        """Gets the predefined parameters of an action from the registry"""
        for category in ACTION_REGISTRY.values():
            if action_name in category:
                return category[action_name]
        return {}

    def generate_params_for_action(self, action_name):
        # Clear previous layout
        self.clear_layout(self.params_layout)

        self.param_widgets = {}

        # Get predefined parameters
        predefined_params = self.get_predefined_params(action_name)

        if predefined_params:
            # There are predefined parameters
            for param_name, param_type in predefined_params.items():
                row = QHBoxLayout()
                label = QLabel(param_name)
                row.addWidget(label)

                # Create widget based on type
                if param_type == "int":
                    widget = QSpinBox()
                    widget.setRange(-999999, 999999)
                    widget.valueChanged.connect(self.sync_params_from_widgets)

                elif param_type == "float":
                    widget = QDoubleSpinBox()
                    widget.setRange(-999999.0, 999999.0)
                    widget.setDecimals(3)
                    widget.valueChanged.connect(self.sync_params_from_widgets)

                elif param_type == "bool":
                    widget = QCheckBox()
                    widget.stateChanged.connect(self.sync_params_from_widgets)

                else:  # string por defecto
                    widget = QLineEdit()
                    widget.textChanged.connect(self.sync_params_from_widgets)

                # Rellenar con valores existentes si existen
                existing_value = None
                if self.current_action:
                    # Buscar en lista nueva
                    if isinstance(self.current_action.params, list):
                        for p in self.current_action.params:
                            if p.get("key") == param_name:
                                existing_value = p.get("value")
                                break
                    # O en diccionario antiguo
                    elif isinstance(self.current_action.params, dict) and param_name in self.current_action.params:
                        existing_value = self.current_action.params[param_name]

                if existing_value is not None:
                    if isinstance(widget, QSpinBox):
                        widget.blockSignals(True)
                        widget.setValue(int(existing_value))
                        widget.blockSignals(False)
                    elif isinstance(widget, QDoubleSpinBox):
                        widget.blockSignals(True)
                        widget.setValue(float(existing_value))
                        widget.blockSignals(False)
                    elif isinstance(widget, QCheckBox):
                        widget.blockSignals(True)
                        widget.setChecked(bool(existing_value))
                        widget.blockSignals(False)
                    elif isinstance(widget, QLineEdit):
                        widget.blockSignals(True)
                        widget.setText(str(existing_value))
                        widget.blockSignals(False)

                row.addWidget(widget)
                self.params_layout.addLayout(row)

                self.param_widgets[param_name] = widget

    def sync_params_from_widgets(self):
        if not self.current_action:
            return

        params = []

        for name, widget in self.param_widgets.items():
            value = None

            if isinstance(widget, QSpinBox):
                value = widget.value()

            elif isinstance(widget, QDoubleSpinBox):
                value = widget.value()

            elif isinstance(widget, QCheckBox):
                value = widget.isChecked()

            elif isinstance(widget, QLineEdit):
                value = widget.text()

            if value is not None:
                params.append({"key": name, "value": str(value)})

        self.current_action.params = params

    def clear_layout(self, layout):
        while layout.count():
            item = layout.takeAt(0)

            if item.widget():
                item.widget().deleteLater()

            elif item.layout():
                self.clear_layout(item.layout())

    # ─────────────────────────────────────
    # PARAMETERS PERSONALIZADOS
    # ─────────────────────────────────────

    def add_param(self):
        """Adds an empty row to the parameters table"""
        if not self.current_action:
            return

        row = self.params_table.rowCount()
        self.params_table.insertRow(row)
        self.params_table.setItem(row, 0, QTableWidgetItem("param_name"))
        self.params_table.setItem(row, 1, QTableWidgetItem("value"))

    def remove_param(self):
        """Removes the selected row from the parameters table"""
        if not self.current_action:
            return

        row = self.params_table.currentRow()
        if row < 0:
            return

        self.params_table.removeRow(row)
        self.sync_params_from_table()

    def on_param_table_changed(self, item):
        """Executes when something changes in the parameters table"""
        self.sync_params_from_table()
        self._notify_change()

    def _notify_change(self):
        """Notifies that there were changes"""
        if self.on_change_callback:
            self.on_change_callback()

    def sync_params_from_table(self):
        """Syncs custom parameters from the table to the current action"""
        if not self.current_action:
            return

        # Get predefined parameters
        predefined_params = self.get_predefined_params(self.current_action.name)

        # Keep existing predefined parameters (convert to list if necessary)
        if isinstance(self.current_action.params, dict):
            # Convert old dictionary to new list
            params = [{"key": k, "value": v} for k, v in self.current_action.params.items() if k in predefined_params]
        else:
            # Already a list, keep predefined parameters
            params = [p for p in self.current_action.params if p.get("key") in predefined_params]

        # Add custom parameters from the table
        for row in range(self.params_table.rowCount()):
            name_item = self.params_table.item(row, 0)
            value_item = self.params_table.item(row, 1)

            if name_item and value_item:
                name = name_item.text().strip()
                value = value_item.text().strip()

                if name and name not in predefined_params:  # Only add if not predefined
                    params.append({"key": name, "value": value})

        self.current_action.params = params

    def refresh_params_table(self):
        """Reloads the parameters table with current data (only custom parameters)"""
        self.params_table.blockSignals(True)
        self.params_table.setRowCount(0)

        if self.current_action and self.current_action.params:
            # Get predefined parameters for this action
            predefined_params = self.get_predefined_params(self.current_action.name)

            # Convert to list if old dictionary
            params = self.current_action.params
            if isinstance(params, dict):
                params = [{"key": k, "value": v} for k, v in params.items()]

            # Show only parameters that are NOT predefined
            for param in params:
                param_name = param.get("key") if isinstance(param, dict) else param
                param_value = param.get("value") if isinstance(param, dict) else ""

                if param_name not in predefined_params:
                    row = self.params_table.rowCount()
                    self.params_table.insertRow(row)
                    self.params_table.setItem(row, 0, QTableWidgetItem(param_name))
                    self.params_table.setItem(row, 1, QTableWidgetItem(str(param_value)))

        self.params_table.blockSignals(False)

    # ─────────────────────────────────────
    # TRANSITION
    # ─────────────────────────────────────

    def refresh_condition_tree(self):
        self.condition_tree.clear()

        if not self.current_transition or not self.current_transition.condition:
            return

        root_item = self.create_tree_item_from_condition(
            self.current_transition.condition,
            None
        )

        self.condition_tree.addTopLevelItem(root_item)
        self.condition_tree.expandAll()

    def create_tree_item_from_condition(self, condition, parent_condition):
        item = QTreeWidgetItem()
        item.setText(0, self.condition_to_text(condition))

        item.condition_ref = condition
        item.parent_condition_ref = parent_condition

        if isinstance(condition, LogicalCondition):
            for child in condition.conditions:
                child_item = self.create_tree_item_from_condition(child, condition)
                item.addChild(child_item)

        return item

    def condition_to_text(self, condition):
        if isinstance(condition, LogicalCondition):
            return condition.type

        if isinstance(condition, GenericCondition):
            return f"{condition.type} {condition.params}"

        return "UnknownCondition"
    
    def set_root_simple_condition(self):
        if not self.current_transition:
            return

        condition_type = self.cond_type.currentText()
        self.current_transition.condition = GenericCondition(condition_type, {})

        self.current_condition = self.current_transition.condition

        self.generate_params_for_condition(condition_type)
        self.refresh_condition_tree()

    def set_root_logical_condition(self, op):
        if not self.current_transition:
            return

        self.current_transition.condition = LogicalCondition(op, [])
        self.current_condition = self.current_transition.condition

        self.clear_layout(self.condition_params_layout)
        self.condition_param_widgets = {}

        self.refresh_condition_tree()

    def get_selected_condition_item(self):
        selected = self.condition_tree.selectedItems()
        if not selected:
            return None

        return selected[0]

    def add_simple_child_condition(self):
        item = self.get_selected_condition_item()

        if not item:
            return

        parent_condition = item.condition_ref

        if not isinstance(parent_condition, LogicalCondition):
            return

        condition_type = self.cond_type.currentText()
        new_condition = GenericCondition(condition_type, {})

        parent_condition.conditions.append(new_condition)
        self.current_condition = new_condition

        self.generate_params_for_condition(condition_type)
        self.refresh_condition_tree()

    def add_logical_child_condition(self, op):
        item = self.get_selected_condition_item()

        if not item:
            return

        parent_condition = item.condition_ref

        if not isinstance(parent_condition, LogicalCondition):
            return

        new_condition = LogicalCondition(op, [])
        parent_condition.conditions.append(new_condition)
        self.current_condition = new_condition

        self.clear_layout(self.condition_params_layout)
        self.condition_param_widgets = {}

        self.refresh_condition_tree()

    def select_condition_tree_item(self, item):
        self.current_condition = item.condition_ref

        if isinstance(self.current_condition, GenericCondition):
            self.cond_type.blockSignals(True)
            self.cond_type.setCurrentText(self.current_condition.type)
            self.cond_type.blockSignals(False)

            self.generate_params_for_condition(self.current_condition.type)
            self.populate_condition_params()

        else:
            self.clear_layout(self.condition_params_layout)
            self.condition_param_widgets = {}
    
    def generate_params_for_condition(self, condition_type):
        self.clear_layout(self.condition_params_layout)
        self.condition_param_widgets = {}

        for category in CONDITION_REGISTRY.values():
            if condition_type in category:
                params = category[condition_type]

                for param_name, param_type in params.items():
                    row = QHBoxLayout()
                    label = QLabel(param_name)
                    row.addWidget(label)

                    if param_type == "int":
                        widget = QSpinBox()
                        widget.setRange(-999999, 999999)

                    elif param_type == "float":
                        widget = QDoubleSpinBox()
                        widget.setRange(-999999.0, 999999.0)
                        widget.setDecimals(3)

                    elif param_type == "bool":
                        widget = QCheckBox()

                    elif param_type == "operator":
                        widget = QComboBox()
                        widget.addItems(["==", "!=", "<", ">", "<=", ">="])

                    else:
                        widget = QLineEdit()

                        # Autocompletado para variableName
                        if param_name == "variableName":
                            completer = QCompleter(ALL_VARIABLES)
                            completer.setCaseSensitivity(Qt.CaseInsensitive)
                            widget.setCompleter(completer)
                            widget.setPlaceholderText("E.g.: distanceToPlayer, health, isGrounded")

                    row.addWidget(widget)
                    self.condition_params_layout.addLayout(row)
                    self.condition_param_widgets[param_name] = widget

                break

    def populate_condition_params(self):
        if not isinstance(self.current_condition, GenericCondition):
            return

        params = self.current_condition.params

        for name, widget in self.condition_param_widgets.items():
            if name not in params:
                continue

            value = params[name]

            if isinstance(widget, QSpinBox):
                widget.setValue(int(value))

            elif isinstance(widget, QDoubleSpinBox):
                widget.setValue(float(value))

            elif isinstance(widget, QCheckBox):
                widget.setChecked(bool(value))

            elif isinstance(widget, QComboBox):
                widget.setCurrentText(str(value))

            elif isinstance(widget, QLineEdit):
                widget.setText(str(value))

    def save_simple_condition(self):
        if not isinstance(self.current_condition, GenericCondition):
            return

        condition_type = self.cond_type.currentText()
        params = {}

        for name, widget in self.condition_param_widgets.items():

            if isinstance(widget, QSpinBox):
                params[name] = widget.value()

            elif isinstance(widget, QDoubleSpinBox):
                params[name] = widget.value()

            elif isinstance(widget, QCheckBox):
                params[name] = widget.isChecked()

            elif isinstance(widget, QComboBox):
                params[name] = widget.currentText()

            elif isinstance(widget, QLineEdit):
                params[name] = widget.text()

        self.current_condition.type = condition_type
        self.current_condition.params = params

        self.refresh_condition_tree()
    
    def remove_selected_condition(self):
        item = self.get_selected_condition_item()

        if not item or not self.current_transition:
            return

        condition = item.condition_ref
        parent = item.parent_condition_ref

        # Si es root
        if parent is None:
            self.current_transition.condition = None
            self.current_condition = None
            self.refresh_condition_tree()
            return

        # Si es hija
        if isinstance(parent, LogicalCondition):
            if condition in parent.conditions:
                parent.conditions.remove(condition)

        self.current_condition = None
        self.refresh_condition_tree()

    def inspect_transition(self, edge):
        self.current_transition = edge.transition
        self.current_state = None
        self.current_action = None
        self.current_condition = None

        self.title.setText(
            f"Transition: {edge.transition.from_state.id} → {edge.transition.to_state.id}"
        )

        self._show_transition_section()
        self.refresh_condition_tree()