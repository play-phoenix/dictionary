#!/bin/bash

# Dictionary App Installer for KDE Plasma

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"

echo "Installing Dictionary App..."

# Check if files exist
if [ ! -f "$SCRIPT_DIR/dictionary.py" ] || [ ! -f "$SCRIPT_DIR/dictionary.desktop" ]; then
    echo "ERROR: dictionary.py or dictionary.desktop not found!"
    exit 1
fi

# Copy Python script to /usr/local/bin
echo "Installing Python script..."
sudo cp "$SCRIPT_DIR/dictionary.py" /usr/local/bin/dictionary.py
sudo chmod +x /usr/local/bin/dictionary.py

# Copy desktop file to applications directory
echo "Installing desktop file..."
mkdir -p ~/.local/share/applications
cp "$SCRIPT_DIR/dictionary.desktop" ~/.local/share/applications/dictionary.desktop

echo ""
echo "Hiding games from app menu by creating local overrides..."
echo ""

# Paths to search for games (Includes Flatpaks now)
SEARCH_DIRS=(
    "/usr/share/applications"
    "/var/lib/flatpak/exports/share/applications"
    "$HOME/.local/share/flatpak/exports/share/applications"
    "$HOME/.local/share/applications"
)

for DIR in "${SEARCH_DIRS[@]}"; do
    if [ -d "$DIR" ]; then
        for desktop_file in "$DIR"/*.desktop; do
            if [ -f "$desktop_file" ]; then
                # Case insensitive search for Game category
                if grep -qi "Categories=.*Game" "$desktop_file"; then
                    filename=$(basename "$desktop_file")
                    local_override="$HOME/.local/share/applications/$filename"
                    
                    # If it's already a local file, modify it directly
                    if [ "$DIR" == "$HOME/.local/share/applications" ]; then
                        if ! grep -q "NoDisplay=" "$desktop_file"; then
                            sed -i '/\[Desktop Entry\]/a NoDisplay=true' "$desktop_file"
                            echo "  ✓ Hidden local app: $filename"
                        fi
                    else
                        # If it's a system/flatpak app, create a local override
                        if [ ! -f "$local_override" ]; then
                            cp "$desktop_file" "$local_override"
                            sed -i '/\[Desktop Entry\]/a NoDisplay=true' "$local_override"
                            echo "  ✓ Overridden & Hidden: $filename"
                        elif ! grep -q "NoDisplay=" "$local_override"; then
                            sed -i '/\[Desktop Entry\]/a NoDisplay=true' "$local_override"
                            echo "  ✓ Hidden existing override: $filename"
                        fi
                    fi
                fi
            fi
        done
    fi
done

# Refresh KDE application menu
echo ""
echo "Refreshing application menu..."
kbuildsycoca6 > /dev/null 2>&1

echo "✅ Installation complete!"
