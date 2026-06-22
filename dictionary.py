#!/usr/bin/env python3

import sys
import os
import subprocess
from pathlib import Path
from PyQt6.QtWidgets import (
    QApplication, QMainWindow, QWidget, QVBoxLayout, QHBoxLayout,
    QLabel, QLineEdit, QPushButton, QGridLayout, QScrollArea
)
from PyQt6.QtCore import Qt, QSize, QTimer
from PyQt6.QtGui import QFont, QIcon, QPixmap
import configparser

class DictionaryApp(QMainWindow):
    def __init__(self):
        super().__init__()
        self.PASSWORD = "AZHfhszmh#786_abbas007_4252"
        self.games = []
        self.clear_timer = QTimer()
        self.clear_timer.timeout.connect(self.clear_status)
        self.init_ui()
        self.load_games()
        
    def init_ui(self):
        self.setWindowTitle("Dictionary")
        self.setGeometry(100, 100, 700, 600)
        self.setWindowIcon(QIcon.fromTheme("accessories-dictionary"))
        
        main_widget = QWidget()
        self.setCentralWidget(main_widget)
        layout = QVBoxLayout(main_widget)
        layout.setSpacing(10)
        layout.setContentsMargins(15, 15, 15, 15)
        
        title = QLabel("Dictionary")
        title_font = QFont()
        title_font.setPointSize(18)
        title_font.setBold(True)
        title.setFont(title_font)
        layout.addWidget(title)
        
        instructions = QLabel("Enter word:")
        layout.addWidget(instructions)
        
        self.input_field = QLineEdit()
        self.input_field.setPlaceholderText("Type here...")
        self.input_field.returnPressed.connect(self.on_enter_pressed)
        self.input_field.setMinimumHeight(40)
        layout.addWidget(self.input_field)
        
        self.status_label = QLabel("")
        self.status_label.setStyleSheet("color: red;")
        layout.addWidget(self.status_label)
        
        self.games_container = QWidget()
        self.games_layout = QGridLayout(self.games_container)
        self.games_layout.setSpacing(10)
        
        self.scroll_area = QScrollArea()
        self.scroll_area.setWidget(self.games_container)
        self.scroll_area.setWidgetResizable(True)
        self.scroll_area.setVisible(False)
        layout.addWidget(self.scroll_area)
        
        layout.addStretch()
        
    def on_enter_pressed(self):
        password = self.input_field.text()
        
        if password == self.PASSWORD:
            self.input_field.clear()
            self.status_label.setText("")
            self.show_games()
        else:
            self.status_label.setText("Incorrect.")
            self.input_field.clear()
            self.clear_timer.start(5000)
            
    def clear_status(self):
        self.status_label.setText("")
        self.clear_timer.stop()
            
    def load_games(self):
        self.games = []
        
        # Added Flatpak directories to the search path
        desktop_dirs = [
            Path.home() / ".local/share/applications",
            Path("/usr/share/applications"),
            Path("/usr/local/share/applications"),
            Path("/var/lib/flatpak/exports/share/applications"),
            Path.home() / ".local/share/flatpak/exports/share/applications",
        ]
        
        for directory in desktop_dirs:
            if not directory.exists():
                continue
                
            for desktop_file in directory.glob("*.desktop"):
                try:
                    config = configparser.ConfigParser()
                    # strict=False allows parsing some malformed desktop files
                    config.read(desktop_file)
                    
                    if "Desktop Entry" not in config:
                        continue
                    
                    entry = config["Desktop Entry"]
                    categories = entry.get("Categories", "").split(";")
                    hidden = entry.get("Hidden", "false").lower() == "true"
                    
                    # Case insensitive check so "game" or "Games" both work
                    is_game = any(cat.lower() in ["game", "games"] for cat in categories)
                    
                    if is_game and not hidden:
                        name = entry.get("Name", "Unknown")
                        exec_cmd = entry.get("Exec", "")
                        icon = entry.get("Icon", "application-games")
                        
                        if exec_cmd:
                            self.games.append({
                                "name": name,
                                "exec": exec_cmd,
                                "icon": icon,
                                "desktop_file": str(desktop_file)
                            })
                except Exception:
                    pass
        
        seen = set()
        unique_games = []
        for game in self.games:
            if game["name"] not in seen:
                seen.add(game["name"])
                unique_games.append(game)
        self.games = unique_games
        
    def show_games(self):
        while self.games_layout.count():
            widget = self.games_layout.takeAt(0).widget()
            if widget:
                widget.deleteLater()
        
        if not self.games:
            no_games = QLabel("No games found")
            self.games_layout.addWidget(no_games, 0, 0)
        else:
            for idx, game in enumerate(self.games):
                button = QPushButton()
                button.setText(game["name"])
                button.setMinimumHeight(100)
                button.setMinimumWidth(120)
                
                try:
                    icon = QIcon.fromTheme(game["icon"])
                    if not icon.isNull():
                        button.setIcon(icon)
                        button.setIconSize(QSize(64, 64))
                except:
                    pass
                
                button.clicked.connect(lambda checked, g=game: self.launch_game(g))
                
                row = idx // 4
                col = idx % 4
                self.games_layout.addWidget(button, row, col)
        
        self.scroll_area.setVisible(True)
        
    def launch_game(self, game):
        try:
            exec_cmd = game["exec"]
            # Clean up exec command (remove %U, %F, etc.)
            exec_cmd = exec_cmd.split("%")[0].strip()
            
            # Using subprocess.Popen with shell=True handles complex Steam arguments flawlessly
            subprocess.Popen(exec_cmd, shell=True, start_new_session=True)
        except Exception as e:
            self.status_label.setText(f"Error launching game: {str(e)}")

def main():
    app = QApplication(sys.argv)
    window = DictionaryApp()
    window.show()
    sys.exit(app.exec())

if __name__ == "__main__":
    main()
