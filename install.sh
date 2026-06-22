#!/bin/bash

# Dictionary App Installer for KDE Plasma

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"

echo "Installing Dictionary App..."
echo "Script directory: $SCRIPT_DIR"

# Copy Python script to /usr/local/bin
echo "Copying Python script..."
sudo cp "$SCRIPT_DIR/dictionary.py" /usr/local/bin/dictionary.py
sudo chmod +x /usr/local/bin/dictionary.py

# Copy desktop file to applications directory
echo "Copying desktop file..."
mkdir -p ~/.local/share/applications
cp "$SCRIPT_DIR/dictionary.desktop" ~/.local/share/applications/dictionary.desktop

# Hide all games from the app menu by adding NoDisplay=true
echo "Hiding games from app menu..."

# Hide games in user's local applications
for desktop_file in ~/.local/share/applications/*.desktop; do
    if [ -f "$desktop_file" ]; then
        if grep -q "Categories=.*Game" "$desktop_file"; then
            # Check if already has NoDisplay
            if ! grep -q "NoDisplay=" "$desktop_file"; then
                echo "Hiding: $(basename "$desktop_file")"
                sed -i '/\[Desktop Entry\]/a NoDisplay=true' "$desktop_file"
            fi
        fi
    fi
done

# Hide games in system applications (needs sudo)
echo "Hiding system games..."
for desktop_file in /usr/share/applications/*.desktop; do
    if [ -f "$desktop_file" ]; then
        if grep -q "Categories=.*Game" "$desktop_file"; then
            filename=$(basename "$desktop_file")
            # Copy to local if not already there
            if [ ! -f ~/.local/share/applications/"$filename" ]; then
                sudo cp "$desktop_file" ~/.local/share/applications/"$filename"
                sudo chown $(whoami):$(whoami) ~/.local/share/applications/"$filename"
            fi
            # Add NoDisplay to local copy
            if ! grep -q "NoDisplay=" ~/.local/share/applications/"$filename"; then
                sed -i '/\[Desktop Entry\]/a NoDisplay=true' ~/.local/share/applications/"$filename"
            fi
        fi
    fi
done

# Refresh KDE application menu
kbuildsycoca6 > /dev/null 2>&1

echo ""
echo "✓ Installation complete!"
echo ""
echo "The Dictionary app is now in your application menu."
echo "Games are hidden - access them by:"
echo "  1. Press Windows key"
echo "  2. Search 'Dictionary'"
echo "  3. Open it"
echo "  4. Enter password: AZHfhszmh#786_abbas007_4252"
echo "  5. Press Enter to see all games"
