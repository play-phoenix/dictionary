#!/bin/bash

# Dictionary App Installer for KDE Plasma

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"

echo "Installing Dictionary App..."
echo "Script directory: $SCRIPT_DIR"
echo ""

# Check if files exist
if [ ! -f "$SCRIPT_DIR/dictionary.py" ] || [ ! -f "$SCRIPT_DIR/dictionary.desktop" ]; then
    echo "ERROR: dictionary.py or dictionary.desktop not found!"
    echo "Make sure you're running this script from the dictionary repository directory."
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
echo "Hiding games from app menu..."
echo ""

# Hide games in user's local applications
echo "Processing user applications..."
for desktop_file in ~/.local/share/applications/*.desktop; do
    if [ -f "$desktop_file" ]; then
        if grep -q "Categories=.*Game" "$desktop_file"; then
            if ! grep -q "NoDisplay=" "$desktop_file"; then
                echo "  ✓ $(basename "$desktop_file")"
                sed -i '/\[Desktop Entry\]/a NoDisplay=true' "$desktop_file"
            fi
        fi
    fi
done

# Hide games in system applications
echo ""
echo "Processing system applications (needs sudo)..."
for desktop_file in /usr/share/applications/*.desktop; do
    if [ -f "$desktop_file" ]; then
        if grep -q "Categories=.*Game" "$desktop_file"; then
            filename=$(basename "$desktop_file")
            echo "  ✓ $filename"
            
            # Use sudo to copy and modify
            sudo bash -c "
                if ! grep -q 'NoDisplay=' '$desktop_file'; then
                    sed -i '/\[Desktop Entry\]/a NoDisplay=true' '$desktop_file'
                fi
            "
        fi
    fi
done

# Refresh KDE application menu
echo ""
echo "Refreshing application menu..."
kbuildsycoca6 > /dev/null 2>&1

echo ""
echo "✅ Installation complete!"
echo ""
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo "The Dictionary app is now installed!"
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo ""
echo "To use it:"
echo "  1. Press Windows key"
echo "  2. Search for 'Dictionary'"
echo "  3. Open it"
echo "  4. Type password: AZHfhszmh#786_abbas007_4252"
echo "  5. Press Enter to see all games"
echo ""
