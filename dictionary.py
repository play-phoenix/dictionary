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
from PyQt6.QtGui import QFont, QIcon, QColor
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
        
        # Modern Card Styling with Hover Effects
        self.setStyleSheet("""
            GameCard {
                background-color: #232629;
                border: 1px solid #31363b;
                border-radius: 8px;
            }
            GameCard:hover {
                background-color: #2a2e32;
                border: 1px solid #3daee9;
            }
            QLabel {
                color: #eff0f1;
                background: transparent;
            }
        """)
        
        layout = QVBoxLayout(self)
        layout.setAlignment(Qt.AlignmentFlag.AlignCenter)
        layout.setSpacing(8)
        
        # Game Icon
        self.icon_label = QLabel()
        self.icon_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        icon = QIcon.fromTheme(self.game["icon"])
        if not icon.isNull():
            pixmap = icon.pixmap(QSize(54, 54))
            self.icon_label.setPixmap(pixmap)
        else:
            fallback = QIcon.fromTheme("application-games")
            self.icon_label.setPixmap(fallback.pixmap(QSize(54, 54)))
            
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
        self.PASSWORD = "AZHfhszmh#786_abbas007_4252" [cite: 1]
        self.games = []
        self.clear_timer = QTimer()
        self.clear_timer.timeout.connect(self.clear_status)
        self.init_ui()
        self.load_games()
        
    def init_ui(self):
        self.setWindowTitle("Dictionary")
        self.setGeometry(100, 100, 750, 550)
        self.setWindowIcon(QIcon.fromTheme("accessories-dictionary"))
        
        # Global Dark Theme stylesheet matching modern Breeze/KDE Dark
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
                border-radius: 6px;
                color: #eff0f1;
                padding-left: 10px;
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
        
        # Real-looking Stealth Dictionary Header
        self.header_container = QWidget()
        header_layout = QVBoxLayout(self.header_container)
        header_layout.setContentsMargins(0, 0, 0, 0)
        
        self.title = QLabel("Dictionary Lookup")
        title_font = QFont()
        title_font.setPointSize(20)
        title_font.setBold(True)
        self.title.setFont(title_font)
        
        self.instructions = QLabel("Search for definitions, etymologies, and spellings.")
        self.instructions.setStyleSheet("color: #7f8c8d; font-size: 12px;")
        
        header_layout.addWidget(self.title)
        header_layout.addWidget(self.instructions)
        self.main_layout.addWidget(self.header_container)
        
        # Modernized input box 
        self.input_field = QLineEdit()
        self.input_field.setPlaceholderText("Enter word to look up...")
        self.input_field.returnPressed.connect(self.on_enter_pressed)
        self.input_field.setMinimumHeight(45)
        self.main_layout.addWidget(self.input_field)
        
        self.status_label = QLabel("")
        self.status_label.setStyleSheet("color: #da4453; font-weight: bold;")
        self.main_layout.addWidget(self.status_label)
        
        # Secret Launcher Area
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
        
        if password == self.PASSWORD: [cite: 1]
            self.input_field.clear()
            self.status_label.setText("")
            self.reveal_launcher_ui()
        else:
            # Fake dictionary "error" or not found message
            self.status_label.setText("Error: Word not found in database.")
            self.input_field.clear()
            self.clear_timer.start(4000)
            
    def clear_status(self):
        self.status_label.setText("")
        self.clear_timer.stop()
            
    def load_games(self): [cite: 1]
        self.games = [] [cite: 1]
        desktop_dirs = [ [cite: 1]
            Path.home() / ".local/share/applications", [cite: 1]
            Path("/usr/share/applications"), [cite: 1]
            Path("/usr/local/share/applications"), [cite: 1]
            Path("/var/lib/flatpak/exports/share/applications"), [cite: 1]
            Path.home() / ".local/share/flatpak/exports/share/applications", [cite: 1]
        ] [cite: 1]
        
        for directory in desktop_dirs: [cite: 1]
            if not directory.exists(): [cite: 1]
                continue [cite: 1]
                
            for desktop_file in directory.glob("*.desktop"): [cite: 1]
                try: [cite: 1]
                    config = configparser.ConfigParser() [cite: 1]
                    config.read(desktop_file) [cite: 1]
                    
                    if "Desktop Entry" not in config: [cite: 1]
                        continue [cite: 1]
                    
                    entry = config["Desktop Entry"] [cite: 1]
                    categories = entry.get("Categories", "").split(";") [cite: 1]
                    hidden = entry.get("Hidden", "false").lower() == "true" [cite: 1]
                    
                    is_game = any(cat.lower() in ["game", "games"] for cat in categories) [cite: 1]
                    
                    if is_game and not hidden: [cite: 1]
                        name = entry.get("Name", "Unknown") [cite: 1]
                        exec_cmd = entry.get("Exec", "") [cite: 1]
                        icon = entry.get("Icon", "application-games") [cite: 1]
                        
                        if exec_cmd: [cite: 1]
                            self.games.append({ [cite: 1]
                                "name": name, [cite: 1]
                                "exec": exec_cmd, [cite: 1]
                                "icon": icon, [cite: 1]
                                "desktop_file": str(desktop_file) [cite: 1]
                            }) [cite: 1]
                except Exception: [cite: 1]
                    pass [cite: 1]
        
        seen = set() [cite: 1]
        unique_games = [] [cite: 1]
        for game in self.games: [cite: 1]
            if game["name"] not in seen: [cite: 1]
                seen.add(game["name"]) [cite: 1]
                unique_games.append(game) [cite: 1]
        self.games = unique_games [cite: 1]
        
    def reveal_launcher_ui(self):
        """Morphs the layout seamlessly into a premium games dashboard."""
        self.title.setText("Games Vault")
        self.instructions.setText("Select a tactical application to deploy.")
        self.input_field.setVisible(False)
        
        # Clear layout safely
        while self.games_layout.count():
            widget = self.games_layout.takeAt(0).widget()
            if widget:
                widget.deleteLater()
        
        if not self.games: [cite: 1]
            no_games = QLabel("No anomalies detected in your library.") [cite: 1]
            no_games.setStyleSheet("color: #7f8c8d; font-size: 14px;")
            self.games_layout.addWidget(no_games, 0, 0) [cite: 1]
        else:
            # 4 Columns of highly polished cards
            for idx, game in enumerate(self.games): [cite: 1]
                card = GameCard(game, self.launch_game)
                row = idx // 4 [cite: 1]
                col = idx % 4 [cite: 1]
                self.games_layout.addWidget(card, row, col) [cite: 1]
        
        self.scroll_area.setVisible(True) [cite: 1]
        
    def launch_game(self, game): [cite: 1]
        try: [cite: 1]
            exec_cmd = game["exec"] [cite: 1]
            exec_cmd = exec_cmd.split("%")[0].strip() [cite: 1]
            subprocess.Popen(exec_cmd, shell=True, start_new_session=True) [cite: 1]
        except Exception as e: [cite: 1]
            self.status_label.setText(f"Deployment failed: {str(e)}") [cite: 1]

def main(): [cite: 1]
    app = QApplication(sys.argv) [cite: 1]
    window = DictionaryApp() [cite: 1]
    window.show() [cite: 1]
    sys.exit(app.exec()) [cite: 1]

if __name__ == "__main__": [cite: 1]
    main() [cite: 1]
