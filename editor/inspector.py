from PySide6.QtWidgets import (
    QWidget, QVBoxLayout, QLabel, QListWidget,
    QPushButton, QHBoxLayout, QInputDialog, QTableWidget, 
    QTableWidgetItem, QLineEdit, QComboBox
)

from editor.node_item import StateNode
from editor.edge_item import TransitionEdge
from model.action import Action
from model.condition import VariableCondition


class Inspector(QWidget):
    def __init__(self):
        super().__init__()

        self.current_state = None
        self.current_node = None
        self.current_action = None
        self.current_transition = None

        self.layout = QVBoxLayout(self)
        self.title = QLabel("Inspector")
        self.layout.addWidget(self.title)

        # --- ENTER ---
        self.layout.addWidget(QLabel("Enter"))
        self.enter_list = QListWidget()
        self.layout.addWidget(self.enter_list)

        enter_buttons = QHBoxLayout()
        self.enter_add = QPushButton("+")
        self.enter_remove = QPushButton("-")
        enter_buttons.addWidget(self.enter_add)
        enter_buttons.addWidget(self.enter_remove)
        self.layout.addLayout(enter_buttons)

        # --- TICK ---
        self.layout.addWidget(QLabel("Tick"))
        self.tick_list = QListWidget()
        self.layout.addWidget(self.tick_list)

        tick_buttons = QHBoxLayout()
        self.tick_add = QPushButton("+")
        self.tick_remove = QPushButton("–")
        tick_buttons.addWidget(self.tick_add)
        tick_buttons.addWidget(self.tick_remove)
        self.layout.addLayout(tick_buttons)

        # --- EXIT ---
        self.layout.addWidget(QLabel("Exit"))
        self.exit_list = QListWidget()
        self.layout.addWidget(self.exit_list)

        exit_buttons = QHBoxLayout()
        self.exit_add = QPushButton("+")
        self.exit_remove = QPushButton("–")
        exit_buttons.addWidget(self.exit_add)
        exit_buttons.addWidget(self.exit_remove)
        self.layout.addLayout(exit_buttons)

        # ─────────────────────────────────────
        # PARÁMETROS
        # ─────────────────────────────────────

        self.layout.addWidget(QLabel("Action Parameters"))

        self.params_table = QTableWidget(0, 2)
        self.params_table.setHorizontalHeaderLabels(["Key", "Value"])
        self.layout.addWidget(self.params_table)

        self.param_add = QPushButton("+ Param")
        self.param_remove = QPushButton("- Param")
        self.layout.addLayout(self._row(self.param_add, self.param_remove))

        # ─────────────────────────────────────
        # CONEXIONES
        # ─────────────────────────────────────

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

        self.param_add.clicked.connect(self.add_param)
        self.param_remove.clicked.connect(self.remove_param)
        self.params_table.itemChanged.connect(self.on_param_changed)

        # ─────────────────────────────────────
        # CONDICIÓN DE TRANSICIÓN
        # ─────────────────────────────────────

        self.layout.addWidget(QLabel("Transition Condition"))

        self.cond_type = QComboBox()
        self.cond_type.addItems(["VARIABLE"])
        self.layout.addWidget(self.cond_type)

        self.cond_var = QLineEdit()
        self.cond_var.setPlaceholderText("Variable name")
        self.layout.addWidget(self.cond_var)

        self.cond_op = QComboBox()
        self.cond_op.addItems(["==", "!=", "<", ">", "<=", ">="])
        self.layout.addWidget(self.cond_op)

        self.cond_value = QLineEdit()
        self.cond_value.setPlaceholderText("Value")
        self.layout.addWidget(self.cond_value)

        self.cond_save = QPushButton("Save Condition")
        self.layout.addWidget(self.cond_save)

        self.cond_save.clicked.connect(self.save_transition_condition)


    # ------------------------

    # ─────────────────────────────────────
    # UTIL
    # ─────────────────────────────────────

    def _row(self, *widgets):
        row = QHBoxLayout()
        for w in widgets:
            row.addWidget(w)
        return row
    
    # ─────────────────────────────────────
    # ESTADO
    # ─────────────────────────────────────

    def clear(self):
        self.current_state = None
        self.title.setText("Inspector")
        self.enter_list.clear()
        self.tick_list.clear()
        self.exit_list.clear()
        self.current_action = None
        self.params_table.setRowCount(0)


    def inspect(self, item):
        self.clear()

        if isinstance(item, StateNode):
            self.inspect_state(item)

        elif isinstance(item, TransitionEdge):
            self.inspect_transition(item)

    def inspect_state(self, node):
        self.current_node = node
        self.current_state = node.state

        self.title.setText(f"State: {node.state.id}")

        self.enter_list.clear()
        self.tick_list.clear()
        self.exit_list.clear()

        for a in node.state.enter:
            self.enter_list.addItem(str(a))
        for a in node.state.tick:
            self.tick_list.addItem(str(a))
        for a in node.state.exit:
            self.exit_list.addItem(str(a))

    # ------------------------
    # ACCIONES
    # ------------------------

    def add_action(self, phase):
        if not self.current_state:
            return

        name, ok = QInputDialog.getText(
            self, "Nueva acción", "Nombre de la acción:"
        )

        if not ok or not name:
            return

        action = Action(name)

        action_list = getattr(self.current_state, phase)
        action_list.append(action)

        self.refresh()

    def remove_action(self, phase):
        if not self.current_state:
            return

        list_widget = getattr(self, f"{phase}_list")
        row = list_widget.currentRow()

        # 🔥 CLAVE: comprobar selección válida
        if row < 0:
            return

        actions = getattr(self.current_state, phase)

        if row >= len(actions):
            return

        actions.pop(row)
        self.params_table.setRowCount(0)
        self.refresh()

    def select_action(self, phase, item):
        index = getattr(self, f"{phase}_list").row(item)
        self.current_action = getattr(self.current_state, phase)[index]

        self.show_action_params()

    def refresh(self):
        if self.current_node:
            self.inspect_state(self.current_node)

    # ─────────────────────────────────────
    # PARÁMETROS
    # ─────────────────────────────────────

    def show_action_params(self):
        self.params_table.blockSignals(True)
        self.params_table.setRowCount(0)

        if not self.current_action:
            self.params_table.blockSignals(False)
            return

        for k, v in self.current_action.params.items():
            row = self.params_table.rowCount()
            self.params_table.insertRow(row)
            self.params_table.setItem(row, 0, QTableWidgetItem(k))
            self.params_table.setItem(row, 1, QTableWidgetItem(str(v)))

        self.params_table.blockSignals(False)

    def add_param(self):
        if not self.current_action:
            return

        self.params_table.blockSignals(True)

        row = self.params_table.rowCount()
        self.params_table.insertRow(row)
        self.params_table.setItem(row, 0, QTableWidgetItem("key"))
        self.params_table.setItem(row, 1, QTableWidgetItem("value"))

        self.params_table.blockSignals(False)

        self._sync_params_from_table()

    def remove_param(self):
        row = self.params_table.currentRow()
        if row < 0:
            return

        self.params_table.removeRow(row)
        self._sync_params_from_table()

    def on_param_changed(self, _):
        self._sync_params_from_table()

    def _sync_params_from_table(self):
        if not self.current_action:
            return

        self.current_action.params = {
            self.params_table.item(r, 0).text():
            self.params_table.item(r, 1).text()
            for r in range(self.params_table.rowCount())
            if self.params_table.item(r, 0)
        }

    # ─────────────────────────────────────
    # TRANSICIÓN
    # ─────────────────────────────────────
    def inspect_transition(self, edge):
        self.current_transition = edge.transition
        self.current_state = None
        self.current_action = None

        self.title.setText(
            f"Transition: {edge.transition.from_state.id} → {edge.transition.to_state.id}"
        )

        self.show_transition_condition()

    def show_transition_condition(self):
        cond = self.current_transition.condition

        if not cond:
            self.cond_var.clear()
            self.cond_value.clear()
            self.cond_op.setCurrentIndex(0)
            return

        # VARIABLE
        self.cond_var.setText(cond.name)
        self.cond_op.setCurrentText(cond.operator)
        self.cond_value.setText(str(cond.value))

    def save_transition_condition(self):
        if not self.current_transition:
            return

        if not self.cond_var.text() or not self.cond_value.text():
            return

        self.current_transition.condition = VariableCondition(
            self.cond_var.text(),
            self.cond_op.currentText(),
            self.cond_value.text()
        )

        print("Condition saved:", self.current_transition.condition.to_dict())