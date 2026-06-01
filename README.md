# FSM Editor Framework

A visual, user-friendly framework for creating and editing Finite State Machines (FSMs) with a PySide6-based GUI.

## Quick Start

### 1. Install Dependencies

```bash
pip install -r requirements.txt
```

### 2. Run the Application

```bash
python main.py
```

### 3. Build an Executable

```bash
python setup.py
```

The executable will be created in the `dist/` folder.

## Features

- **Visual FSM Editor**: Drag-and-drop interface for creating states and transitions
- **State Types**: Normal states, Entry Points, Global States, and ANY_STATE
- **Actions**: Configure Enter, Tick, and Exit actions for states
- **Conditions**: Build simple and logical conditions for transitions
- **Undo/Redo**: Full command history with Ctrl+Z and Ctrl+Shift+Z
- **Save & Load**: Projects saved as `.fsmproj` files in JSON format
- **File Association**: Automatic `.fsmproj` file registration on Windows
- **Autocomplete**: Variable and action suggestions as you type

## Project Structure

```
tfg-aleix-python/
├── main.py                 # Entry point
├── setup.py               # Build script for executables
├── requirements.txt       # Python dependencies
├── MANUAL.md              # Complete user manual
├── README.md              # This file
├── model/                 # Core FSM logic
├── editor/                # Visual editor components
├── persistence/           # Save/Load functionality
├── commands/              # Undo/Redo system
├── data/                  # Predefined registries
└── export/                # Export functionality
```

## System Requirements

- Python 3.8 or higher
- Windows operating system
- 200 MB free disk space

## Documentation

For complete documentation on:
- **Setup and Installation**: See [MANUAL.md - Part I](MANUAL.md#part-i-setup-and-installation)
- **Using the Editor**: See [MANUAL.md - Part II](MANUAL.md#part-ii-visual-framework-guide)

## Key Commands

| Command | Shortcut |
|---------|----------|
| New FSM | Ctrl+N |
| Save | Ctrl+S |
| Save As | Ctrl+Shift+S |
| Load | Ctrl+O |
| Export JSON | Ctrl+E |
| Undo | Ctrl+Z |
| Redo | Ctrl+Shift+Z |

## State Types

1. **Normal State** (Gray): Regular states with Enter, Tick, Exit actions
2. **Entry Point** (Green): Starting state of the FSM
3. **Global State** (Blue): Executes every frame regardless of current state
4. **ANY_STATE** (Magenta): System state for global transitions

## Creating Your First FSM

1. Launch the application
2. Right-click on the canvas and create states
3. Set one state as the Entry Point (green)
4. Create transitions by right-clicking a state and selecting "Create transition"
5. Add conditions to transitions
6. Add actions to states
7. Save your project with Ctrl+S

## Troubleshooting

For common issues and solutions, refer to the **Troubleshooting** section in [MANUAL.md](MANUAL.md#12-support-and-troubleshooting).

## License

This project is part of a university thesis (TFG - Trabajo de Fin de Grado).

## Support

For detailed information on all features and usage, see the complete [MANUAL.md](MANUAL.md).
