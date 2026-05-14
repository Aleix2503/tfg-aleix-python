from abc import ABC, abstractmethod


class Command(ABC):
    """Clase base para todos los comandos"""

    @abstractmethod
    def execute(self):
        """Ejecuta el comando"""
        pass

    @abstractmethod
    def undo(self):
        """Deshace el comando"""
        pass


class CommandManager:
    """Gestor de comandos para Undo/Redo"""

    def __init__(self):
        self.undo_stack = []
        self.redo_stack = []

    def execute(self, command):
        """Ejecuta un comando y lo añade al stack de undo"""
        command.execute()
        self.undo_stack.append(command)
        # Limpiar redo stack cuando se ejecuta un comando nuevo
        self.redo_stack.clear()

    def undo(self):
        """Deshace el último comando"""
        if not self.can_undo():
            return

        command = self.undo_stack.pop()
        command.undo()
        self.redo_stack.append(command)

    def redo(self):
        """Rehace el último comando deshecho"""
        if not self.can_redo():
            return

        command = self.redo_stack.pop()
        command.execute()
        self.undo_stack.append(command)

    def can_undo(self):
        """Retorna True si hay comandos para deshacer"""
        return len(self.undo_stack) > 0

    def can_redo(self):
        """Retorna True si hay comandos para rehacer"""
        return len(self.redo_stack) > 0

    def clear(self):
        """Limpia los stacks"""
        self.undo_stack.clear()
        self.redo_stack.clear()
