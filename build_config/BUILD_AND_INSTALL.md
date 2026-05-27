# FSM Editor - Build and Installation Guide

This guide explains how to build the FSM Editor into a Windows executable and set up file associations for `.fsmproj` files.

## Prerequisites

Before building the executable, ensure you have:

1. **Python 3.7+** installed
2. **Dependencies installed**:
   ```bash
   pip install -r requirements.txt
   ```

## Method 1: Automatic Setup (Recommended)

### Step 1: Build Executable

Run the setup script from the project directory (go to the root directory):

```bash
cd path\to\tfg-aleix-python
python setup.py
```

Or directly:

```bash
python setup.py
```

This will:
- Build the executable using PyInstaller
- Create `FSMEditor.exe` in the `dist/` folder
- Automatically register file associations

### Step 2: Done!

The executable is ready to use. You can now:
- Run `FSMEditor.exe` directly
- Double-click `.fsmproj` files to open them

---

## Method 2: Manual Setup

### Step 1: Build Executable

Run PyInstaller manually:

```bash
PyInstaller --name=FSMEditor ^
    --onefile ^
    --windowed ^
    --add-data data:data ^
    --add-data model:model ^
    --add-data editor:editor ^
    --add-data commands:commands ^
    --add-data persistence:persistence ^
    --add-data export:export ^
    main.py
```

This creates `dist/FSMEditor.exe`.

### Step 2: Register File Association

#### Option A: Using Batch Script (Easiest)

1. **Run as Administrator**: Right-click `build_config/register_fsmproj.bat` and select "Run as Administrator"
2. The script will automatically register `.fsmproj` files

#### Option B: Manual Registry Edit

1. Open the `build_config/register_fsmproj.reg` file with a text editor
2. Replace `C:\path\to\FSMEditor.exe` with the actual path to your executable (e.g., `C:\Users\aleix\Desktop\Uni\TFG\tfg-aleix-python\dist\FSMEditor.exe`)
3. Save the file
4. Double-click it to apply the registry changes
5. Click "Yes" when prompted about modifying the registry

#### Option C: PowerShell Script

```powershell
$exe_path = "C:\path\to\FSMEditor.exe"

# Register file extension
reg add "HKCR\.fsmproj" /ve /d "FSMProjectFile" /f
reg add "HKCR\.fsmproj" /v "Content Type" /d "application/x-fsmproj" /f

# Register program
reg add "HKCR\FSMProjectFile" /ve /d "FSM Project File" /f
reg add "HKCR\FSMProjectFile\DefaultIcon" /ve /d "$exe_path,0" /f
reg add "HKCR\FSMProjectFile\shell\open\command" /ve /d "`"$exe_path`" `"%1`"" /f

Write-Host "File association registered successfully!"
```

---

## Using the Executable

### Method 1: Direct Execution
```bash
FSMEditor.exe
```

### Method 2: Open a Project File
```bash
FSMEditor.exe "C:\path\to\your\project.fsmproj"
```

### Method 3: Double-Click (After File Association)
Simply double-click any `.fsmproj` file in Windows Explorer

---

## Troubleshooting

### "PyInstaller not found" Error
```bash
pip install pyinstaller
```

### File Association Not Working
1. Ensure you ran the registration script **as Administrator**
2. Try the `register_fsmproj.bat` script instead of manual registry edit
3. Check that the executable path is correct (no spaces in path recommended)

### Executable Won't Start
1. Ensure all dependencies are installed: `pip install -r requirements.txt`
2. Try running from command line to see error messages
3. Check that PyInstaller included all data folders properly

### "Failed to Register File Association"
1. Right-click `register_fsmproj.bat` → "Run as Administrator"
2. Or manually use Registry Editor (regedit) to add the entries

### Missing Data Folders in Executable
Edit `setup.py` and ensure all required data folders are listed in the `--add-data` parameter.

---

## Project Structure

The executable includes:
- `main.py` - Entry point
- `editor/` - GUI components
- `model/` - FSM data structures
- `commands/` - Undo/Redo system
- `persistence/` - File I/O
- `data/` - Action and condition registries
- `export/` - Export functionality

---

## Next Steps

After building the executable:

1. **Create Shortcuts** (Optional)
   - Create desktop shortcuts to `.fsmproj` files for quick access

2. **Distribute** (Optional)
   - The `dist/FSMEditor.exe` can be distributed to other Windows machines
   - They don't need Python installed - it's all bundled in the executable

3. **Updates**
   - To build a new version, modify your code and run `setup.py` again
   - The new executable replaces the old one

---

## Notes

- The executable is self-contained and doesn't require Python to be installed
- File associations are stored in the Windows registry (HKEY_CLASSES_ROOT)
- Only one version of the executable should be active (replace old ones)
- To uninstall file associations, delete the registry entries for `FSMProjectFile`

For more information about PyInstaller, see: https://pyinstaller.org/
