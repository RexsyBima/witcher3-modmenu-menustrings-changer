# Witcher 3 Mod Menu Changer - Installation & Setup Guide

This guide covers **non-uv** installation methods using standard Python tooling (venv + pip) for general use. The program is designed to work with any modern Python 3.x distribution.

## Prerequisites

### Minimum Requirements

- **Python**: 3.9 or higher
- **Operating System**: Windows, macOS, or Linux
- **Witcher 3**: Installed on your system

---

## Quick Start Installation

### Step 1: Install Python

**Windows:**

```powershell
# From Microsoft Store or python.org installer
# Select "Add Python to PATH" during installation
python --version  # Should show Python 3.9+
```

**macOS / Linux:**

```bash
# Using Homebrew
brew install python@3.11

# Or via system package manager (Ubuntu/Debian):
sudo apt update && sudo apt install python3 python3-pip python3-venv

# Verify Python installation
python3 --version  # Should show Python 3.9+
```

NOTE: for other linux distro that dont use brew and apt may need to
install python with their own package manager

### Step 2: Clone or Download the Project

```bash
# Git clone (recommended)
git clone https://github.com/RexsyBima/witcher3-modmenu-menustrings-changer.git
cd witcher3-modmenu-changer

# Or download zip file and extract to project folder
```

### Step 3: Create Virtual Environment

Create an isolated Python environment to avoid conflicts with system packages:

```bash
# Linux/macOS
python3 -m venv .venv
source .venv/bin/activate

# Windows (PowerShell)
python -m venv .venv
.venv\Scripts\Activate.ps1

# Windows (Command Prompt)
.venv\Scripts\activate.bat
```

### Step 4: Install Dependencies

Install all required Python packages:

```bash
pip install PySide6 lxml requests beautifulsoup4
```

**Optional - Additional tools:**

```bash
pip install lxml lxml_html_clean
```

### Step 5: Verify Installation

Test that everything is working:

```bash
python -c "import PySide6; import lxml; print('✓ All dependencies installed successfully')"
```

---

## Running the Application

### Method 1: GUI Mode (Recommended for Beginners)

Start the graphical interface:

```bash
# Linux/macOS/Windows
python main.py
```

On startup, you will be prompted to:

1. Select your Witcher 3 installation folder
2. Choose a mode (Manual/Auto/Silent)
3. Submit to launch the main application

### Method 2: CLI Tool Mode

Use the command-line interface directly:

```bash
# Install as module (optional, for easier CLI access)
pip install -e .

# Run from project folder
python -m src.witcher3_modmenu_changer /path/to/your/witcher3
```

### Method 3: Direct Script Execution

Run individual scripts without installing:

```bash
# GUI application
python main.py

# CLI tool (from project root)
python -m src.witcher3_modmenu_changer
```

---

## Witcher 3 Setup Guide

### Finding Your Witcher 3 Installation Location

**Windows:**

- Default: `C:\Program Files\The Witcher 3\` or `C:\Games\The Witcher 3\`
- Steam: `%LOCALAPPDATA%\Steam\steamapps\common\The Witcher 3\`
- GOG: `%USERPROFILE%\GOG Games\The Witcher 3\`

**Linux:**

- Default: `/home/username/Games/The Witcher 3\`
- Custom: Wherever you installed it via Steam/GOG/CD key

### Required File Structure

The tool looks for these files in your Witcher 3 directory:

```
Witcher 3/
├── bin/
│   └── witcher3.exe          # (Windows) Game executable
├── data/
│   └── mods/                  # Mod configuration folder
│       ├── config.ini         # Main config file
│       └── ...                # Other mod files
```

### Backing Up Your Data (Recommended)

Before modifying any mod menus, create manual backups:

```bash
# Windows - Copy entire mods folder
robocopy "C:\Games\The Witcher 3\data\mods" "C:\Games\The Witcher 3\data\mods-backup" /MIR

# Linux/macOS
cp -r "/path/to/witcher3/data/mods" "/path/to/backup/"
```

---

## Configuration Files

### Automatic Config (`.witcher3_modmenu_config.json`)

On first run, the application automatically creates a config file storing your game path:

```json
{
  "game_dir": "/home/user/Games/The Witcher 3",
  "last_category_index": 0,
  "selected_mod": null
}
```

**Location:** Same directory as `main.py`

### Manual Configuration

To change the config file location or restore a backup:

1. Close the application
2. Navigate to your project folder
3. Edit `.witcher3_modmenu_config.json` directly
4. Update `"game_dir"` path as needed

---

## Troubleshooting

### "Module not found" Errors

Ensure virtual environment is activated:

```bash
# Check if activate script exists (Linux/macOS)
ls -la .venv/bin/activate

# Check if activate script exists (Windows)
dir .venv\Scripts\activate*

# Reactivate if needed
source .venv/bin/activate   # Linux/macOS
.venv\Scripts\Activate.ps1  # Windows PowerShell
.venv\Scripts\activate.bat  # Windows CMD
```

### Missing PySide6

Verify installation:

```bash
pip show PySide6

# If not installed, reinstall with verbose output
pip install --verbose PySide6 lxml requests beautifulsoup4
```

### GUI Not Appearing (Linux/X11)

For headless servers or X11 forwarding issues, use CLI mode instead:

```bash
python -m src.witcher3_modmenu_changer /path/to/witcher3
```

### Permission Errors on macOS

```bash
# Grant Python network access (if needed)
sudo sysctl -w net.inet.tcp.mssclamping=0

# Or use Python from Homebrew with correct permissions
brew install python@3.11
python3.11 main.py
```

### Invalid Game Directory Error

If the application cannot validate your Witcher 3 installation:

1. Ensure XML files exist in the `mods` folder:

   ```bash
   # Linux/macOS
   ls "/path/to/witcher3/data/mods/config.ini"
   
   # Windows
   dir "C:\Games\The Witcher 3\data\mods\*.xml"
   ```

2. Use an exact path (no relative paths like `./` or `../`)
3. Ensure the game is not currently running (some files may be locked)

---

## Uninstallation & Cleanup

### Remove the Application

```bash
# Deactivate virtual environment
deactivate              # Linux/macOS/PowerShell
.venv\Scripts\deactivate.bat  # Windows CMD

# Delete project folder
rm -rf /path/to/witcher3-modmenu-changer   # Linux/macOS
rmdir /s /p "C:\path\to\witcher3-modmenu-changer"  # Windows

# Optionally remove config files from home directory
rm ~/.config/witcher3_modmenu_config.json   # If stored in home
```

### Clean Python Cache

```bash
# Remove compiled Python files
rm -rf .venv/__pycache__
find . -name "*.pyc" -delete

# Or start fresh
rm -rf .venv && python3 -m venv .venv
pip install PySide6 lxml requests beautifulsoup4
```

---

## Performance Notes

### Memory Usage

- **GUI Mode**: ~50-100 MB (PySide6 overhead)
- **CLI Mode**: ~20-40 MB
- Both modes require minimal RAM (< 512 MB)

### Disk Space

- Application: ~3-5 MB installed files
- Runtime cache: Negligible
- Backups: Depends on number of mods edited

### Recommended Systems

| Component | Minimum | Recommended |
|-----------|---------|-------------|
| Python | 3.9 | 3.10+ |
| RAM | 2 GB | 4+ GB |
| Disk | 50 MB free | SSD preferred |
| GUI Display | Any modern GPU | Any display adapter |

---

## Support & Contributing

### Issue Reporting

When reporting issues, include:

- Python version (`python --version`)
- Operating system and architecture
- Full error traceback if available
- Witcher 3 installation location

### Documentation

- This HOWTO guide
- Main README.md for project overview
- Source code comments in `src/` directory

### Code Quality

The application follows these conventions:

- Type hints for all functions
- PEP 8 coding style
- PySide6 widget hierarchy (avoiding `QApplication.instance()` where possible)
- Qt signal/slot pattern for event handling

---

## Quick Reference Card

```bash
# Install everything without uv
python3 -m venv .venv && source .venv/bin/activate
pip install PySide6 lxml requests beautifulsoup4

# Run GUI application
python main.py

# Run CLI tool directly
python -m src.witcher3_modmenu_changer /path/to/witcher3

# Check installed packages
pip list

# Update dependencies
pip install --upgrade PySide6 lxml requests beautifulsoup4

# Deactivate virtual environment
deactivate
```

---

## License

This project is a work in progress for educational purposes. See the main README.md for licensing information and attribution details.
