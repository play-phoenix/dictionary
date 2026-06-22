#!/usr/bin/env python3

import sys
import os
import subprocess
from pathlib import Path
from PyQt6.QtWidgets import (
    QApplication, QMainWindow, QWidget, QVBoxLayout, QHBoxLayout,
    QLabel, QLineEdit, QPushButton, QGridLayout, QScrollArea, QFrame
)
from PyQt6.QtCore import Qt, QSize, QTimer
from PyQt6.QtGui import QFont, QIcon
import configparser

class GameCard(QFrame):
    """A sleek, modern clickable card for each game."""
    def __init__(self, game, launch_callback, parent=None):
        super().__init__(parent)
        self.game = game
        self.launch_callback = launch_callback
        self.init_ui()

    def init_ui(self):
        self.setFrameShape(QFrame.Shape.StyledPanel)
        self.setFixedSize(140, 150)
        
        self.setStyleSheet("""
            QFrame {
                background-color: #232629;
                border: 1px solid #31363b;
                border-radius: 10px;
            }
            QFrame:hover {
                background-color: #2c3135;
                border: 1px solid #3daee9;
            }
            QLabel {
                color: #eff0f1;
                background: transparent;
                border: none;
            }
        """)
        
        layout = QVBoxLayout(self)
        layout.setAlignment(Qt.AlignmentFlag.AlignCenter)
        layout.setSpacing(10)
        layout.setContentsMargins(10, 10, 10, 10)
        
        # Game Icon
        self.icon_label = QLabel()
        self.icon_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        icon = QIcon.fromTheme(self.game["icon"])
        if not icon.isNull():
            pixmap = icon.pixmap(QSize(56, 56))
            self.icon_label.setPixmap(pixmap)
        else:
            fallback = QIcon.fromTheme("application-games")
            self.icon_label.setPixmap(fallback.pixmap(QSize(56, 56)))
            
        # Game Title
        self.title_label = QLabel(self.game["name"])
        self.title_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.title_label.setWordWrap(True)
        font = QFont()
        font.setPointSize(9)
        font.setBold(True)
        self.title_label.setFont(font)
        
        layout.addWidget(self.icon_label)
        layout.addWidget(self.title_label)

    def mousePressEvent(self, event):
        if event.button() == Qt.MouseButton.LeftButton:
            self.launch_callback(self.game)
        super().mousePressEvent(event)


class DictionaryApp(QMainWindow):
    def __init__(self):
        super().__init__()
        self.PASSWORD = "AZHfhszmh#786_abbas007_4252"
        self.all_games = []      # Master list of all games found
        self.visible_games = []  # Filtered list based on search bar
        self.unlocked = False
        self.clear_timer = QTimer()
        self.clear_timer.timeout.connect(self.clear_status)
        self.init_ui()
        self.load_games()
        
    def init_ui(self):
        self.setWindowTitle("Dictionary")
        self.setGeometry(100, 100, 750, 600)
        self.setWindowIcon(QIcon.fromTheme("accessories-dictionary"))
        
        # Premium Dark Theme matching Breeze-Dark styles
        self.setStyleSheet("""
            QMainWindow {
                background-color: #1b1e20;
            }
            QLabel {
                color: #eff0f1;
            }
            QLineEdit {
                background-color: #232629;
                border: 1px solid #31363b;
                border-radius: 8px;
                color: #eff0f1;
                padding-left: 12px;
                padding-right: 12px;
                font-size: 13px;
            }
            QLineEdit:focus {
                border: 1px solid #3daee9;
            }
            QScrollArea {
                border: none;
                background-color: transparent;
            }
            QScrollBar:vertical {
                border: none;
                background: #1b1e20;
                width: 8px;
                margin: 0px;
            }
            QScrollBar::handle:vertical {
                background: #4d5052;
                min-height: 20px;
                border-radius: 4px;
            }
            QScrollBar::handle:vertical:hover {
                background: #3daee9;
            }
        """)
        
        main_widget = QWidget()
        self.setCentralWidget(main_widget)
        self.main_layout = QVBoxLayout(main_widget)
        self.main_layout.setContentsMargins(25, 25, 25, 25)
        self.main_layout.setSpacing(15)
        
        # --- HEADER AREA ---
        self.header_container = QWidget()
        header_layout = QVBoxLayout(self.header_container)
        header_layout.setContentsMargins(0, 0, 0, 0)
        header_layout.setSpacing(4)
        
        self.title = QLabel("Dictionary Lookup")
        title_font = QFont()
        title_font.setPointSize(22)
        title_font.setBold(True)
        self.title.setFont(title_font)
        
        self.instructions = QLabel("Search for definitions, etymologies, and spellings.")
        self.instructions.setStyleSheet("color: #7f8c8d; font-size: 12px; background: transparent;")
        
        header_layout.addWidget(self.title)
        header_layout.addWidget(self.instructions)
        self.main_layout.addWidget(self.header_container)
        
        # --- INPUT FIELDS ---
        # Password / Dictionary Search box
        self.input_field = QLineEdit()
        self.input_field.setPlaceholderText("Enter word to look up...")
        self.input_field.returnPressed.connect(self.on_enter_pressed)
        self.input_field.setMinimumHeight(45)
        self.main_layout.addWidget(self.input_field)
        
        # Hidden Launcher Game Search box (Initially hidden)
        self.search_bar = QLineEdit()
        self.search_bar.setPlaceholderText("Search your gaming vault...")
        self.search_bar.textChanged.connect(self.filter_games)
        self.search_bar.setMinimumHeight(45)
        self.search_bar.setVisible(False)
        self.main_layout.addWidget(self.search_bar)
        
        # Status Message Label
        self.status_label = QLabel("")
        self.status_label.setStyleSheet("color: #da4453; font-weight: bold; background: transparent;")
        self.main_layout.addWidget(self.status_label)
        
        # --- GAMES DISPLAY AREA ---
        self.games_container = QWidget()
        self.games_container.setStyleSheet("background-color: transparent;")
        self.games_layout = QGridLayout(self.games_container)
        self.games_layout.setSpacing(15)
        self.games_layout.setContentsMargins(5, 5, 5, 5)
        
        self.scroll_area = QScrollArea()
        self.scroll_area.setWidget(self.games_container)
        self.scroll_area.setWidgetResizable(True)
        self.scroll_area.setVisible(False)
        self.main_layout.addWidget(self.scroll_area)
        
        self.main_layout.addStretch()
        
    def on_enter_pressed(self):
        password = self.input_field.text()
        
        if password == self.PASSWORD:
            self.input_field.clear()
            self.status_label.setText("")
            self.unlocked = True
            self.reveal_launcher_ui()
        else:
            self.status_label.setText("Error: Word not found in database.")
            self.input_field.clear()
            self.clear_timer.start(4000)
            
    def clear_status(self):
        self.status_label.setText("")
        self.clear_timer.stop()
            
    def load_games(self):
        self.all_games = []
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
                    config = configparser.ConfigParser(interpolation=None)
                    config.read(desktop_file)
                    
                    if "Desktop Entry" not in config:
                        continue
                    
                    entry = config["Desktop Entry"]
                    categories = entry.get("Categories", "").split(";")
                    hidden = entry.get("Hidden", "false").lower() == "true"
                    
                    is_game = any(cat.lower() in ["game", "games"] for cat in categories)
                    
                    if is_game and not hidden:
                        name = entry.get("Name", "Unknown")
                        exec_cmd = entry.get("Exec", "")
                        icon = entry.get("Icon", "application-games")
                        
                        if exec_cmd:
                            self.all_games.append({
                                "name": name,
                                "exec": exec_cmd,
                                "icon": icon,
                                "desktop_file": str(desktop_file)
                            })
                except Exception:
                    pass
        
        # De-duplicate entries
        seen = set()
        unique_games = []
        for game in self.all_games:
            if game["name"] not in seen:
                seen.add(game["name"])
                unique_games.append(game)
                
        # CRITICAL FIX: Sort items alphabetically by game name
        self.all_games = sorted(unique_games, key=lambda g: g["name"].lower())
        self.visible_games = self.all_games.copy()
        
    def reveal_launcher_ui(self):
        """Transitions into a high-end launcher dashboard."""
        self.title.setText("Games Vault")
        self.instructions.setText("Type to instantly filter your digital collection.")
        self.input_field.setVisible(False)
        self.search_bar.setVisible(True)
        self.scroll_area.setVisible(True)
        self.search_bar.setFocus()
        
        self.render_grid()
        
    def render_grid(self):
        """Clears and re-builds the interactive responsive grid."""
        # Clear layout safely
        while self.games_layout.count():
            widget = self.games_layout.takeAt(0).widget()
            if widget:
                widget.deleteLater()
        
        if not self.visible_games:
            no_games = QLabel("No matching games found in your vault.")
            no_games.setStyleSheet("color: #7f8c8d; font-size: 14px; font-style: italic;")
            self.games_layout.addWidget(no_games, 0, 0)
        else:
            # Render game cards inside a 4-column dynamic grid
            for idx, game in enumerate(self.visible_games):
                card = GameCard(game, self.launch_game)
                row = idx // 4
                col = idx % 4
                self.games_layout.addWidget(card, row, col)

    def filter_games(self, text):
        """Runs automatically whenever search box text changes."""
        search_term = text.lower().strip()
        if not search_term:
            self.visible_games = self.all_games.copy()
        else:
            self.visible_games = [g for g in self.all_games if search_term in g["name"].lower()]
        
        self.render_grid()
        
    def launch_game(self, game):
        try:
            exec_cmd = game["exec"]
            exec_cmd = exec_cmd.split("%")[0].strip()
            subprocess.Popen(exec_cmd, shell=True, start_new_session=True)
        except Exception as e:
            self.status_label.setText(f"Launcher Error: {str(e)}")

def main():
    app = QApplication(sys.argv)
    window = DictionaryApp()
    window.show()
    sys.exit(app.exec())

if __name__ == "__main__":
    main()
