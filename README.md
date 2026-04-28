# Witcher 3 Mod Menu Changer

A CLI tool for editing Witcher 3 mod menu configuration XML files.

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

1. On first run, you'll be prompted to enter your Witcher 3 game folder
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

## Backup

Every time you edit a file, the original is automatically backed up to
the `backup/` folder with a timestamp
(format: `filename.YYYY-MM-DD_HH-MM-SS.bak`).
