# FSM Editor Framework - User Manual

## Table of Contents

1. [Part I: Setup and Installation](#part-i-setup-and-installation)
2. [Part II: Visual Framework Guide](#part-ii-visual-framework-guide)

---

# PART I: Setup and Installation

## 1. System Requirements

Before you begin, ensure you have:

- **Python 3.8 or higher** installed on your system
- **Windows operating system** (currently optimized for Windows)
- At least **200 MB** of free disk space for dependencies and executable
- Administrator privileges (for executable installation and registry modifications)

## 2. Installation Steps

### 2.1 Clone or Download the Project

Download the FSM Editor Framework project to your desired location:

```bash
cd path/to/your/projects
git clone <repository-url>
cd tfg-aleix-python
```

### 2.2 Create a Virtual Environment (Recommended)

Creating a virtual environment isolates project dependencies from your system Python:

```bash
# Create virtual environment
python -m venv venv

# Activate virtual environment
# On Windows:
venv\Scripts\activate

# On macOS/Linux:
source venv/bin/activate
```

### 2.3 Install Dependencies

Install the required packages listed in `requirements.txt`:

```bash
pip install -r requirements.txt
```

**Required packages:**
- **PySide6**: Qt framework for building the graphical user interface
- **PyInstaller**: Tool to convert Python scripts into standalone executables

If you want to install packages individually:

```bash
pip install PySide6
pip install PyInstaller
```

### 2.4 Verify Installation

Test that everything is installed correctly:

```bash
python -c "import PySide6; print('PySide6 OK')"
python -c "import PyInstaller; print('PyInstaller OK')"
```

## 3. Running the Application

### 3.1 Running from Source (Development Mode)

To run the FSM Editor directly from Python source code:

```bash
python main.py
```

The application window will open, displaying an empty FSM editor ready for use.

### 3.2 Running with an Existing Project

To open a previously saved FSM project file (`.fsmproj`):

```bash
python main.py path/to/your/project.fsmproj
```

This will load the saved project directly into the editor.

## 4. Building an Executable

### 4.1 Using the Setup Script

The `setup.py` file automates the build process:

```bash
python setup.py
```

**What this script does:**
1. Uses PyInstaller to compile the Python code into an executable
2. Includes all necessary data folders (model, editor, persistence, etc.)
3. Creates a single-file executable: `FSMEditor.exe`
4. Registers the `.fsmproj` file extension with Windows
5. Places the executable in the `dist/` folder

### 4.2 Build Options

If you need to customize the build, you can run PyInstaller directly:

```bash
pyinstaller --name=FSMEditor ^
    --onefile ^
    --windowed ^
    --add-data="data:data" ^
    --add-data="model:model" ^
    --add-data="editor:editor" ^
    --add-data="commands:commands" ^
    --add-data="persistence:persistence" ^
    --add-data="export:export" ^
    main.py
```

**Explanation of flags:**
- `--name`: Name of the executable
- `--onefile`: Create a single executable file instead of a folder
- `--windowed`: Hide the console window (GUI application)
- `--add-data`: Include required folders in the executable

### 4.3 Locate the Executable

After a successful build:

```
dist/
└── FSMEditor.exe
```

The executable will be located in the `dist/` folder.

## 5. File Association Setup

### 5.1 Automatic Registration (Windows)

The `setup.py` script automatically registers `.fsmproj` files to open with FSM Editor. This allows you to:

- Double-click `.fsmproj` files to open them in the editor
- Right-click files and select "Open with" → FSM Editor

### 5.2 Manual Registration (if automatic fails)

If the automatic registration fails, follow these steps:

1. Open **Registry Editor** (press `Win + R`, type `regedit`, press Enter)
2. Navigate to: `HKEY_CURRENT_USER\Software\Microsoft\Windows\CurrentVersion\Explorer\FileExts\.fsmproj`
3. Create a key called `UserChoice` if it doesn't exist
4. Navigate to: `HKEY_CLASSES_ROOT\.fsmproj`
5. Set the default value to: `FSMProjectFile`
6. Create a subkey: `FSMProjectFile\DefaultIcon`
7. Set its value to: `C:\path\to\FSMEditor.exe,0`
8. Create: `FSMProjectFile\shell\open\command`
9. Set its value to: `"C:\path\to\FSMEditor.exe" "%%1"`

## 6. Project Structure

Understanding the project layout:

```
tfg-aleix-python/
├── main.py                      # Entry point - starts the application
├── setup.py                     # Build script for creating executables
├── requirements.txt             # Python dependencies
├── model/                       # Core FSM logic
│   ├── fsm.py                  # FSM class definition
│   ├── state.py                # State class definition
│   ├── transition.py           # Transition class definition
│   ├── action.py               # Action class definition
│   └── condition.py            # Condition logic
├── editor/                      # Visual editor components
│   ├── window.py               # Main application window
│   ├── graph_view.py           # Canvas for drawing FSM
│   ├── node_item.py            # Visual representation of states
│   ├── edge_item.py            # Visual representation of transitions
│   └── inspector.py            # Properties panel on the right
├── persistence/                # Save/Load functionality
│   ├── project_serializer.py   # Converting FSM to JSON
│   └── project_loader.py       # Loading FSM from JSON
├── commands/                    # Undo/Redo functionality
│   ├── command_manager.py      # Manages undo/redo history
│   └── commands.py             # Individual command classes
├── data/                        # Predefined registries
│   ├── action_registry.py      # Available actions
│   ├── condition_registry.py   # Available conditions
│   └── variable_registry.py    # Available variables
├── export/                      # Export functionality
│   └── json_exporter.py        # Export FSM to JSON
└── dist/                        # Generated executable location
    └── FSMEditor.exe           # Compiled executable
```

## 7. Troubleshooting

### 7.1 "PySide6 not found"

**Solution:**
```bash
pip install --upgrade PySide6
```

### 7.2 PyInstaller fails to build

**Solution:**
- Ensure PyInstaller is installed: `pip install --upgrade PyInstaller`
- Check that all folder paths in the `--add-data` flags exist
- Run as Administrator on Windows

### 7.3 File association not working

**Solution:**
- Run `setup.py` as Administrator
- Manually register the file extension using the Registry Editor (see Section 5.2)
- Restart Windows Explorer

### 7.4 "Cannot create transitions" error

**Solution:**
- Ensure you have an Entry Point state (green state)
- Check that the target state is not the ANY_STATE
- Global States cannot have incoming or outgoing transitions

### 7.5 Application crashes on startup

**Solution:**
- Check Python version: `python --version` (should be 3.8+)
- Reinstall dependencies: `pip install -r requirements.txt --force-reinstall`
- Check for corrupted project file if loading from a saved state

---

# PART II: Visual Framework Guide

## Overview

The FSM Editor is a visual tool for creating, editing, and managing Finite State Machines (FSMs). It provides an intuitive graphical interface where you can design state machines by dragging, dropping, and connecting states.

## 1. Main Interface Layout

### 1.1 Window Structure

```
┌─────────────────────────────────────────────────────┐
│  FSM - Untitled*                                    │
├─────────────────────────────────────────────────────┤
│ File  Edit                                          │
├─────────────────┬───────────────────────────────────┤
│                 │                                   │
│   Canvas Area   │                                   │
│   (Graph View)  │       Inspector Panel             │
│                 │       (Properties)                │
│                 │                                   │
└─────────────────┴───────────────────────────────────┘
```

### 1.2 Menu Bar

**File Menu:**
- **New FSM** (Ctrl+N): Create a new empty FSM
- **Save FSM** (Ctrl+S): Save the current project
- **Save FSM As...** (Ctrl+Shift+S): Save the project with a new name or location
- **Load FSM** (Ctrl+O): Open an existing `.fsmproj` file
- **Export JSON** (Ctrl+E): Export the FSM as JSON format

**Edit Menu:**
- **Undo** (Ctrl+Z): Undo the last action
- **Redo** (Ctrl+Shift+Z): Redo the last undone action

## 2. State Types

The framework supports four types of states:

### 2.1 Normal State (Light Gray)

**Purpose:** Regular states where you define Enter, Tick, and Exit actions.

**Characteristics:**
- Can have incoming and outgoing transitions
- Can have Enter, Tick, and Exit actions
- Multiple normal states can exist in one FSM
- Only one can be the Entry Point (green)

**Usage:** Use for most of your FSM logic

### 2.2 Entry Point State (Green)

**Purpose:** The initial state when the FSM starts execution.

**Characteristics:**
- Exactly one per FSM (cannot have more than one)
- Highlighted in green
- Has a small green indicator circle
- Has Enter, Tick, and Exit actions
- Can have incoming and outgoing transitions

**Usage:** Set this to the starting state of your FSM

### 2.3 Global State (Steel Blue)

**Purpose:** A special state that runs every frame in parallel with other states.

**Characteristics:**
- Can only have **Tick** actions (no Enter or Exit)
- Cannot have incoming or outgoing transitions
- Execution is independent of normal state transitions
- Useful for continuous checks (health monitoring, input processing)

**Usage:** For actions that must always run regardless of current state

### 2.4 ANY_STATE (Dark Magenta)

**Purpose:** Implicit transitions that can execute from any normal state.

**Characteristics:**
- System-created (automatically created with every FSM)
- Cannot be deleted
- Transitions FROM ANY_STATE are executed when conditions are met
- Useful for global transitions (e.g., "if dead, go to death state")
- Does not appear in the saved project JSON

**Usage:** Define global transitions that bypass normal state flow

## 3. Creating States

### 3.1 Creating a Normal State

1. **Right-click in an empty area** of the canvas
2. Select **"Create new state"**
3. A new gray state box will appear
4. The state is automatically named (State_1, State_2, etc.)

### 3.2 Creating an Entry Point

1. **Right-click in an empty area** of the canvas
2. Select **"Create Entry Point"**
3. A new green state will appear
4. Any existing Entry Point will automatically become a normal state

### 3.3 Creating a Global State

1. **Right-click in an empty area** of the canvas
2. Select **"Create Global State"**
3. A new blue state will appear
4. Named automatically (Global_State_1, Global_State_2, etc.)

## 4. Editing States

### 4.1 Renaming a State

1. **Select the state** by clicking on it
2. In the **Inspector Panel** (right side), modify the **"State Name"** field
3. The state name updates immediately on the canvas

### 4.2 Setting as Entry Point

1. **Right-click on a normal state**
2. Select **"Set as Entry Point"**
3. The state turns green and displays the entry indicator
4. Any previous Entry Point returns to normal gray color

### 4.3 Moving States

1. **Click and drag** a state to move it to a new position
2. All connected transitions update automatically
3. Position is saved when you save the project

### 4.4 Deleting a State

1. **Right-click on a state** (cannot delete ANY_STATE)
2. Select **"Delete state"**
3. All transitions connected to this state are also deleted
4. If you delete the Entry Point, the FSM will have no entry point (warning appears)

## 5. Creating Transitions

### 5.1 Creating a Simple Transition

1. **Right-click on the source state** (where the transition starts)
2. Select **"Create transition"**
3. A **dashed line** appears, following your cursor
4. **Click on the target state** (where the transition ends)
5. The transition is created as a solid arrow between the states

### 5.2 Self-Transitions (Loop)

1. **Right-click on a state**
2. Select **"Create transition"**
3. **Click on the same state** again
4. A curved arrow loop appears at the top of the state
5. Useful for states that can transition to themselves

### 5.3 Transition Rules

**What IS allowed:**
- Normal State → Normal State
- Normal State → ANY_STATE (transitioning FROM ANY_STATE)
- Entry Point → Any State
- ANY_STATE → Normal State
- Self-transitions on any normal state

**What IS NOT allowed:**
- Transitions TO ANY_STATE (cannot make a state transition INTO ANY_STATE)
- Transitions FROM or TO Global States
- Transitions involving ANY_STATE except as a source

**Error Messages:**
- "Invalid Transition: Cannot create transitions to ANY_STATE..."
- "Invalid Transition: Cannot create transitions from or to a Global State..."

### 5.4 Editing Transitions

Transitions are edited through the **Inspector Panel** when selected:

1. **Click on a transition** (the arrow line)
2. The Inspector shows "State: [source] → [target]"
3. Configure the **Condition** (when this transition executes)
4. View connected states and edit conditions

### 5.5 Deleting Transitions

1. **Right-click on a transition arrow**
2. Select **"Delete transition"** (or simply click and delete via commands)
3. Alternatively, delete the transition through the Inspector

## 6. Actions

States can execute actions in three phases:

### 6.1 Enter Actions

**When:** Executed once when entering the state
**Usage:** Initialize variables, play animations, start sounds

**Example actions:**
- SetPlayerAnimation("run")
- PlaySound("footsteps")
- ResetTimer()

### 6.2 Tick Actions

**When:** Executed every frame while in the state
**Usage:** Continuous state behavior, per-frame logic

**Example actions:**
- MoveTowards(target)
- CheckForEnemies()
- UpdateAnimationBlend()

### 6.3 Exit Actions

**When:** Executed once when leaving the state
**Usage:** Cleanup, reset variables, stop sounds

**Example actions:**
- StopAnimation()
- StopSound()
- SaveProgress()

### 6.4 Adding Actions to a State

1. **Select a state** by clicking on it
2. In the Inspector, find the **Enter**, **Tick**, or **Exit** section
3. Click the **"+"** button next to the action list
4. Select an **action name** from the available actions
5. Configure **parameters** if the action requires them

### 6.5 Action Parameters

**Predefined Parameters:**
- Automatically provided by the action
- Always included in the action
- Example: Action "SetAnimation" might have parameter "animationName"

**Custom Parameters:**
- Additional parameters you can add
- Click **"Add Parameter"** in the Parameters table
- Enter parameter name and value

**Parameter Types:**
- **String**: Text values (e.g., "run", "attack")
- **Number**: Numeric values (e.g., 5, 3.14)
- **Boolean**: True/False values

## 7. Conditions

Conditions determine when transitions execute. They evaluate to true or false.

### 7.1 Condition Types

**Simple Condition:**
- A single check: `VariableName operator value`
- Example: `health < 30` (if health is less than 30)
- Example: `hasTarget == true` (if has a target)

**Logical Condition:**
- Combines multiple conditions with AND/OR/NOT
- Example: `(health < 30) AND (hasTarget == true)`
- Example: `(isAlive == false) OR (health <= 0)`

### 7.2 Available Operators

**For Boolean Variables:**
- `==` (equals)
- `!=` (not equals)

**For Numeric Variables (float, int):**
- `==` (equals)
- `!=` (not equals)
- `>` (greater than)
- `>=` (greater than or equal)
- `<` (less than)
- `<=` (less than or equal)

### 7.3 Predefined Variables

**Movement:**
- `isGrounded`: Whether the character is on the ground
- `isJumping`: Whether the character is jumping
- `isFalling`: Whether the character is falling
- `isRunning`: Whether the character is running
- `velocity`: Current character velocity

**Combat:**
- `distanceToPlayer`: Distance to the player
- `distanceToTarget`: Distance to the current target
- `hasTarget`: Whether a target is assigned
- `canSeeTarget`: Whether the target is visible
- `health`: Current health
- `maxHealth`: Maximum health
- `isAlive`: Whether the character is alive

**State & Cooldowns:**
- `canAttack`: Whether attack is available
- `attackCooldown`: Remaining time on cooldown
- `stateTime`: Time spent in current state
- `lastSeenTime`: Time since target was last seen

**Status:**
- `isStunned`: Whether the character is stunned
- `isAttacking`: Whether an attack is being executed
- `ammo`: Available ammunition
- `mana`: Available mana or energy

### 7.4 Adding Conditions to Transitions

1. **Select a transition** by clicking on it
2. In the Inspector, find the **"Transition Condition Tree"** section
3. Click **"Add Condition"** to create a new condition
4. Choose **condition type** (Simple or Logical)
5. For **Simple Conditions:**
   - Select the **variable name** (will autocomplete)
   - Choose an **operator**
   - Enter a **value**
6. For **Logical Conditions:**
   - Select **AND/OR/NOT**
   - Add child conditions using the **"Add Condition"** button

### 7.5 Editing Conditions

1. **Right-click on a condition** in the tree
2. Options appear:
   - Edit the condition
   - Add a sub-condition (for logical conditions)
   - Delete the condition

## 8. Inspector Panel

The Inspector Panel on the right displays and allows editing of selected elements.

### 8.1 When No State is Selected

Shows "Inspector" title
Displays list of available sections
No editing options available

### 8.2 When a Normal State is Selected

**State Name:** Rename the state
**Enter Actions:** Add/remove Enter phase actions
**Tick Actions:** Add/remove Tick phase actions
**Exit Actions:** Add/remove Exit phase actions

### 8.3 When ANY_STATE is Selected

Shows informational text:
"ANY_STATE: Global transitions that can be executed from any state."

No direct editing (ANY_STATE is automatically managed)

### 8.4 When a Global State is Selected

Shows informational text:
"Global State: can only have actions in Tick. Does not allow incoming or outgoing transitions."

**Tick Actions:** Only Tick actions are available
Enter and Exit sections are hidden

### 8.5 When a Transition is Selected

**Source and Target States:** Shows which states are connected
**Transition Condition Tree:** View and edit the condition logic
- Add new conditions
- Remove conditions
- Edit condition details

## 9. File Management

### 9.1 Project File Format

FSM projects are saved as `.fsmproj` files in **JSON format**.

**File contains:**
- Project version information
- All states (except ANY_STATE, which is auto-generated)
- All transitions and their conditions
- All actions and parameters
- Visual information (node positions and zoom level)

### 9.2 Creating a New Project

1. Press **Ctrl+N** or **File → New FSM**
2. The canvas clears and a new FSM is created
3. ANY_STATE is automatically created
4. Inspector is reset to show no selection

### 9.3 Saving a Project

**First Time Save:**
1. Press **Ctrl+S** or **File → Save FSM**
2. A "Save As" dialog appears
3. Choose a location and filename
4. Click **Save**

**Subsequent Saves:**
1. Press **Ctrl+S** to save to the same location
2. Or use **Ctrl+Shift+S** to save with a new name

### 9.4 Loading a Project

**Method 1: From Menu**
1. Press **Ctrl+O** or **File → Load FSM**
2. Select a `.fsmproj` file
3. Click **Open**
4. The project loads with all states, transitions, and actions restored

**Method 2: From File Explorer**
1. Navigate to a `.fsmproj` file
2. Double-click it
3. FSM Editor launches with the project loaded

**Method 3: Command Line**
```bash
python main.py path/to/project.fsmproj
```

### 9.5 Exporting to JSON

To export the FSM in pure JSON format (for use in other tools):

1. Press **Ctrl+E** or **File → Export JSON**
2. Choose a location and filename
3. Click **Save**
4. A JSON file is created with the FSM structure

## 10. Tips and Best Practices

### 10.1 Organizing Your FSM

- **Group related states together** visually on the canvas
- **Use Global State** for continuous checks (health, input)
- **Use Entry Point** clearly to show where the FSM starts
- **Comment your transitions** with clear conditions

### 10.2 Naming Conventions

- **States:** Use descriptive names (Idle, Running, Attacking, Dead)
- **Actions:** Use verb-noun format (SetAnimation, PlaySound, ResetTimer)
- **Variables:** Use camelCase (healthPoints, distanceToTarget)
- **Conditions:** Make them readable (health < 30, hasTarget == true)

### 10.3 Debugging

- **Save frequently:** Use Ctrl+S to save your work
- **Use Undo/Redo:** Don't hesitate to experiment with Ctrl+Z
- **Check Entry Point:** Ensure you have exactly one Entry Point
- **Verify transitions:** Make sure transitions have clear conditions
- **Test conditions:** Verify that conditions make logical sense

### 10.4 Common Patterns

**Patrol to Chase Pattern:**
```
States: Patrol, Chase, Attack, Dead
Entry Point: Patrol
Conditions: 
  - Patrol → Chase: hasTarget == true
  - Chase → Patrol: hasTarget == false
  - Chase → Attack: distanceToTarget < 2
  - Any → Dead: health <= 0
```

**UI State Pattern:**
```
States: Menu, Settings, Playing, Paused
Entry Point: Menu
Conditions:
  - Menu → Playing: startGame == true
  - Playing → Paused: pauseGame == true
  - Paused → Playing: resumeGame == true
```

## 11. Keyboard Shortcuts

| Shortcut | Action |
|----------|--------|
| Ctrl+N | New FSM |
| Ctrl+S | Save FSM |
| Ctrl+Shift+S | Save FSM As |
| Ctrl+O | Load FSM |
| Ctrl+E | Export JSON |
| Ctrl+Z | Undo |
| Ctrl+Shift+Z | Redo |

## 12. Support and Troubleshooting

### 12.1 "Cannot create transitions to ANY_STATE"

**Cause:** You tried to create a transition that ends at ANY_STATE
**Solution:** 
- Transitions FROM ANY_STATE are allowed (global transitions)
- Transitions TO ANY_STATE are not allowed
- If you want a global transition, create it FROM ANY_STATE

### 12.2 "Cannot create transitions from or to Global State"

**Cause:** You tried to connect a Global State with a transition
**Solution:** 
- Global States cannot have incoming or outgoing transitions
- They execute independently every frame
- Use regular states for transition logic

### 12.3 Global State shows "Action not allowed" error

**Cause:** You tried to add Enter or Exit actions to a Global State
**Solution:** 
- Global States can only have Tick actions
- Remove Enter/Exit actions from the Global State
- Use a regular state if you need Enter/Exit actions

### 12.4 Project file won't load

**Cause:** The file might be corrupted or from an older version
**Solution:** 
- Check that the file is in valid JSON format
- Try creating a new FSM and manually recreating the states
- Ensure the file extension is `.fsmproj`

### 12.5 Changes are not being saved

**Cause:** You might have unsaved changes with the asterisk (*) in the title
**Solution:** 
- Press Ctrl+S to save
- Confirm the save dialog
- The asterisk should disappear from the window title

---

## Quick Start Guide

1. **Install:** `pip install -r requirements.txt`
2. **Run:** `python main.py`
3. **Create states:** Right-click canvas → Create new state
4. **Set Entry Point:** Right-click state → Set as Entry Point
5. **Add transitions:** Right-click state → Create transition → Click target state
6. **Add conditions:** Click transition → Configure Condition Tree in Inspector
7. **Add actions:** Click state → Add actions in Enter/Tick/Exit sections
8. **Save:** Ctrl+S and choose a filename

---

## Additional Resources

- **FSM Theory:** Finite State Machines are a fundamental pattern in game development and behavior systems
- **Best Practices:** Always define clear state transitions and use meaningful condition checks
- **Testing:** Save your FSM frequently and test transitions under different conditions

Enjoy creating your Finite State Machines with the FSM Editor Framework!
