from abc import ABC, abstractmethod


class Command(ABC):
    """Base class for all commands"""

    @abstractmethod
    def execute(self):
        """Executes the command"""
        pass

    @abstractmethod
    def undo(self):
        """Undoes the command"""
        pass


class CommandManager:
    """Command manager for Undo/Redo"""

    def __init__(self):
        self.undo_stack = []
        self.redo_stack = []

    def execute(self, command):
        """Executes a command and adds it to the undo stack"""
        command.execute()
        self.undo_stack.append(command)
        # Clear redo stack when a new command is executed
        self.redo_stack.clear()

    def undo(self):
        """Undoes the last command"""
        if not self.can_undo():
            return

        command = self.undo_stack.pop()
        command.undo()
        self.redo_stack.append(command)

    def redo(self):
        """Redoes the last undone command"""
        if not self.can_redo():
            return

        command = self.redo_stack.pop()
        command.execute()
        self.undo_stack.append(command)

    def can_undo(self):
        """Returns True if there are commands to undo"""
        return len(self.undo_stack) > 0

    def can_redo(self):
        """Returns True if there are commands to redo"""
        return len(self.redo_stack) > 0

    def clear(self):
        """Clears the stacks"""
        self.undo_stack.clear()
        self.redo_stack.clear()
