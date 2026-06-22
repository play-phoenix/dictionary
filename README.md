# Dictionary - Hidden Games Launcher

A hidden games launcher for KDE Plasma that disguises itself as a Dictionary utility app.

## Features

- **Appears as a Dictionary app** in the Utilities section of your app menu
- **Password-protected games access** - Enter the secret password to see all games
- **Auto-detects games** - Automatically finds and displays all installed games
- **One-click launch** - Click any game to launch it
- **Games hidden from menu** - Games are removed from the regular app menu and only accessible through this app

## Installation

1. Clone or download this repository
2. Run the installation script:
   ```bash
   chmod +x install.sh
   ./install.sh
   ```

3. Refresh your app menu (or restart KDE Plasma)

## Usage

1. Open the app menu (Windows key)
2. Find "Dictionary" in Utilities
3. Type the secret password: `AZHfhszmh#786_abbas007_4252`
4. Press Enter
5. All your games will appear in a grid
6. Click any game to launch it

## How It Works

- The app reads `.desktop` files from your applications directories
- It scans for entries marked with `Categories=Game` or `Categories=Games`
- All game `.desktop` files are marked with `NoDisplay=true` so they don't appear in the regular app menu
- The Dictionary app bypasses this and displays them in a password-protected interface

## Technical Details

- Written in Python 3 with PyQt6
- Uses `.desktop` file format for app detection
- Supports custom icons for each game
- Auto-hides duplicates
- Scans multiple application directories:
  - `~/.local/share/applications`
  - `/usr/share/applications`
  - `/usr/local/share/applications`

## Password

The default password is: `AZHfhszmh#786_abbas007_4252`

You can modify it by editing the `PASSWORD` variable in `dictionary.py`

## Uninstall

To restore games to your app menu:
1. Remove the NoDisplay entries from game `.desktop` files
2. Delete the Dictionary app: `rm ~/.local/share/applications/dictionary.desktop`
