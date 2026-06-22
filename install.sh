#!/bin/bash

# Dictionary App Installer for KDE Plasma

echo "Installing Dictionary App..."

# Copy Python script to /usr/local/bin
sudo cp dictionary.py /usr/local/bin/dictionary.py
sudo chmod +x /usr/local/bin/dictionary.py

# Copy desktop file to applications directory
mkdir -p ~/.local/share/applications
cp dictionary.desktop ~/.local/share/applications/dictionary.desktop

# Hide all games from the app menu by adding NoDisplay=true
echo "Hiding games from app menu..."
for desktop_file in ~/.local/share/applications/*.desktop /usr/share/applications/*.desktop; do
    if [ -f "$desktop_file" ]; then
        if grep -q "Categories=.*Game" "$desktop_file"; then
            # Check if already has NoDisplay
            if ! grep -q "NoDisplay=" "$desktop_file"; then
                echo "Hiding: $desktop_file"
                sed -i '/\[Desktop Entry\]/a NoDisplay=true' "$desktop_file"
            fi
        fi
    fi
done

# Also hide system games directories
for desktop_file in /usr/share/applications/*.desktop; do
    if [ -f "$desktop_file" ]; then
        if grep -q "Categories=.*Game" "$desktop_file"; then
            # Copy to local and mark as NoDisplay
            filename=$(basename "$desktop_file")
            cp "$desktop_file" ~/.local/share/applications/"$filename"
            if ! grep -q "NoDisplay=" ~/.local/share/applications/"$filename"; then
                sed -i '/\[Desktop Entry\]/a NoDisplay=true' ~/.local/share/applications/"$filename"
            fi
        fi
    fi
done

echo "Installation complete!"
echo "The Dictionary app is now in your application menu."
echo "Games are hidden - access them by opening Dictionary and entering the password."
