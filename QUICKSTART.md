# FSM Editor - Quick Start Guide

Get up and running with the FSM Editor in 5 minutes!

## Installation (1 minute)

### Step 1: Install Python Dependencies
```bash
pip install -r requirements.txt
```

### Step 2: Run the Application
```bash
python main.py
```

The FSM Editor window should open. You're ready to create FSMs!

---

## Creating Your First FSM (4 minutes)

### Step 1: Create States (1 minute)

1. **Right-click** in the empty canvas area
2. Select **"Create new state"** → A gray state appears
3. Repeat to create 3 states total (you'll have: State_1, State_2, State_3)

### Step 2: Set Entry Point (30 seconds)

1. **Right-click** on State_1
2. Select **"Set as Entry Point"** → State_1 turns green
3. The green state shows where your FSM starts

### Step 3: Create Transitions (2 minutes)

1. **Right-click** on State_1 (green)
2. Select **"Create transition"**
3. **Click on State_2** → A transition arrow appears
4. Repeat: Create transition from State_2 → State_3
5. Create one more: State_3 → State_1 (creates a loop)

Your FSM now has this flow:
```
State_1 (Entry) → State_2 → State_3 → State_1 (loop)
```

### Step 4: Save Your Project (30 seconds)

1. Press **Ctrl+S**
2. Choose a location and enter a filename (e.g., `my_fsm.fsmproj`)
3. Click **Save**

Congratulations! You've created and saved your first FSM! 🎉

---

## Next Steps

### Learn More About:

- **States**: Read about Normal States, Entry Points, Global States, and ANY_STATE
  - See: [MANUAL.md - Section 2: State Types](MANUAL.md#2-state-types)

- **Transitions**: Add conditions to make them more interesting
  - See: [MANUAL.md - Section 5: Creating Transitions](MANUAL.md#5-creating-transitions)

- **Actions**: Make states do something when entered/exited
  - See: [MANUAL.md - Section 6: Actions](MANUAL.md#6-actions)

- **Conditions**: Control when transitions execute
  - See: [MANUAL.md - Section 7: Conditions](MANUAL.md#7-conditions)

### Complete Guide

Read the full [MANUAL.md](MANUAL.md) for comprehensive documentation.

---

## Common Tasks

### Rename a State
1. Click the state to select it
2. In the Inspector panel (right), change "State Name"
3. Done!

### Add an Action to a State
1. Click the state
2. In Inspector, find the "Enter", "Tick", or "Exit" section
3. Click the **"+"** button
4. Choose an action from the list
5. Configure parameters if needed

### Add a Condition to a Transition
1. Click the transition (arrow)
2. In Inspector, click "Add Condition"
3. Choose a variable (e.g., `health`)
4. Choose an operator (e.g., `<`)
5. Enter a value (e.g., `30`)
6. Done! Now this transition only executes when health < 30

---

## Keyboard Shortcuts

**Most Important:**
- `Ctrl+N` - New FSM
- `Ctrl+S` - Save
- `Ctrl+Z` - Undo
- `Ctrl+O` - Open existing FSM

**All Shortcuts:**
| Key | Action |
|-----|--------|
| Ctrl+N | New FSM |
| Ctrl+S | Save FSM |
| Ctrl+Shift+S | Save As |
| Ctrl+O | Open FSM |
| Ctrl+E | Export JSON |
| Ctrl+Z | Undo |
| Ctrl+Shift+Z | Redo |

---

## Tips for Success

✅ **DO:**
- Save your work frequently (Ctrl+S)
- Use descriptive state names (Idle, Running, Attacking, Dead)
- Test transitions with different conditions
- Use Global States for logic that always runs
- Experiment with Undo (Ctrl+Z) - you can't break anything!

❌ **DON'T:**
- Delete the Entry Point without setting a new one
- Try to create transitions TO ANY_STATE (only FROM)
- Add Enter/Exit actions to Global States (only Tick allowed)
- Forget to set an Entry Point

---

## Building an Executable

When you're ready to share or distribute your FSM Editor:

```bash
python setup.py
```

This creates `dist/FSMEditor.exe` that can run on any Windows PC without Python installed.

See [MANUAL.md - Section 4: Building an Executable](MANUAL.md#4-building-an-executable) for details.

---

## Need Help?

1. **First Time?** Read this file (you're here!)
2. **Want Details?** See [MANUAL.md](MANUAL.md)
3. **Have Questions?** Check the [Troubleshooting Section](MANUAL.md#12-support-and-troubleshooting)

---

## What's Next?

Now that you understand the basics:

1. **Create a realistic FSM** for a game character or AI system
2. **Add complex conditions** combining multiple variables
3. **Design multi-state behaviors** with Enter, Tick, and Exit actions
4. **Build complete game state machines** (Menu → Playing → Paused → GameOver)
5. **Export your FSM as JSON** for use in other systems

Happy FSM designing! 🚀
