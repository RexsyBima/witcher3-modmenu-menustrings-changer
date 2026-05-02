# Witcher 3 Mod Menu Changer

⚠️ **Work In Progress (WIP) - GUI Development Learning Project**

> 🧑‍🎓 This branch is currently under active development. The author is learning **PySide6 GUI application development** and experimenting with Qt widgets, dialogs, form layouts, and event-driven programming.

This project combines:
- A functional CLI tool for editing Witcher 3 mod menu configuration XML files
- An experimental PySide6 GUI with interactive dialog forms
- Learning notes on Qt signals/slots, validation, and widget styling

## Quick Guide - Current State

### CLI Mode (Functional)
This repository contains a fully working command-line tool that:
- Modifies display names of mod menu categories in Witcher 3 config XML files
- Categorizes mod settings under sections like:
  - Alchemy & Equipment, Camera, Characters, Combat, Gameplay, Quests & Adventures, User Interface, Visuals & Graphics, Miscellaneous
- Automatically backs up original files to `backup/` folder with timestamps

### PySide6 GUI Mode (Learning Project)
The `main.py` now includes:
- Interactive configuration dialog on startup
- Form inputs for game directory path (required) and mode selection dropdown
- Validation logic with warning messages
- Styled submit button with hover effects

## What It Does

This tool modifies the display names of mod menu categories in your
Witcher 3 configuration files. It allows you to categorize mod settings
under different menu sections like
([defined by Community Patch - Menu Strings](https://www.nexusmods.com/witcher3/mods/3650)):

- Alchemy & Equipment
- Camera
- Characters
- Combat
- Gameplay
- Quests & Adventures
- User Interface
- Visuals & Graphics
- Miscellaneous

## Setup (No Python Required!)

This project uses [uv](https://github.com/astral-sh/uv), a fast Python
package manager. You don't need to install Python separately.

### Install uv

**Windows (PowerShell):**

```powershell
powershell -ExecutionPolicy ByPass -c "irm https://astral.sh/uv/install.ps1 | iex"
```

**macOS / Linux:**

```bash
curl -LsSf https://astral.sh/uv/install.sh | sh
```

### Run the Tool

1. Clone or download this repository
2. Open a terminal in the project folder
3. Run:

```bash
uv sync
source .venv/bin/activate && w3mc
```

```fish
uv sync
source .venv/bin/activate.fish && w3mc
```

That's it! `uv` will automatically set up Python and install dependencies
for you.

## Usage

### PySide6 GUI Application (Learning Project)
Run with GUI dialog:

```bash
uv sync && source .venv/bin/activate && python main.py
```

On startup, a configuration dialog appears:
1. Enter your Witcher 3 game folder path
2. Select mode: Manual / Auto / Silent
3. Click Submit
4. Main app window opens after form is filled and validated

### CLI Tool (Alternative Mode)
For command-line usage, see [src/witcher3_modmenu_changer/__init__.py](src/witcher3_modmenu_changer/__init__.py).
   path (e.g., `C:\Games\The Witcher 3` or `/path/to/The Witcher 3`)

2. Select the XML file you want to edit from the list of available mod
   config files

3. Choose which category menu you want the mod settings to appear under

4. The tool will backup the original file to the `backup/` folder with a
   timestamp and modify the XML

## Configuration

- Config file: `.witcher3_modmenu_config.json` (stores your game path)
- Backups: `backup/` folder (automatically created)

## How It Works

The tool parses the selected XML file, finds all `<Group>` elements, and
modifies their `displayName` attribute from `Mods.xxx` to
`Mods.{category}.xxx`, placing the mod settings under the chosen menu
category in the game's mod menu.

## Learning Topics (PySide6 GUI Development)

This project explores:
- **`QDialog`** and **`QFormLayout`** for creating form-based dialogs
- **`QLineEdit`** and **`QComboBox`** widgets for user input
- **Validation logic** using `QMessageBox.warning()` and field checks
- **Custom styling** with `QSS` (Qt Style Sheets) on buttons, inputs, dropdowns
- **Signals/slots** connection: `button.clicked.connect(slot_fn)`
- **Dynamic widget retrieval**: `self.findChild(QLineEdit).text()`
- **Event handling** and form submission flow

## Backup

Every time you edit a file, the original is automatically backed up to
the `backup/` folder with a timestamp
(format: `filename.YYYY-MM-DD_HH-MM-SS.bak`).

---

## Learning Resources (PySide6)

Check out official PySide6 documentation for:
- [`QDialog`](https://doc.qt.io/qt-6/qdialog.html) - Dialog windows and form handling
- [`QFormLayout`](https://doc.qt.io/qt-6/qformlayout.html) - Form-based layouts
- [`QLineEdit`](https://doc.qt.io/qt-6/qlineedit.html) - Single-line text input
- [`QComboBox`](https://doc.qt.io/qt-6/qcombobox.html) - Dropdown selections
- [`QPushButton`](https://doc.qt.io/qt-6/qpushbutton.html) - Buttons and signals
- [Signals & Slots](https://doc.qt.io/qt-6/signalsandslots.html) - Event-driven programming
- [Qt Style Sheets (QSS)](https://doc.qt.io/qt-6/stylesheet.html) - Custom widget styling
