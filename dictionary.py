#!/usr/bin/env python3

import sys
import os
import subprocess
from pathlib import Path
from PyQt6.QtWidgets import (
    QApplication, QMainWindow, QWidget, QVBoxLayout, QHBoxLayout,
    QLabel, QLineEdit, QPushButton, QGridLayout, QScrollArea, QFrame, QGraphicsDropShadowEffect
)
from PyQt6.QtCore import Qt, QSize, QTimer, QPropertyAnimation, QEasingCurve, QPoint
from PyQt6.QtGui import QFont, QIcon, QColor, QResizeEvent
import configparser

class GameCard(QFrame):
    """A highly responsive, premium animated card for each game."""
    def __init__(self, game, launch_callback, parent=None):
        super().__init__(parent)
        self.game = game
        self.launch_callback = launch_callback
        self.init_ui()

    def init_ui(self):
        self.setFrameShape(QFrame.Shape.StyledPanel)
        self.setFixedSize(150, 160)
        
        # Native integration with KDE palette + fallback accent glow
        self.setStyleSheet("""
            QFrame {
                background-color: rgba(35, 38, 41, 0.85);
                border: 1px solid rgba(49, 54, 59, 0.8);
                border-radius: 12px;
            }
            QLabel {
                color: #eff0f1;
                background: transparent;
                border: none;
            }
        """)
        
        # Subtle drop shadow effect for depth
        self.shadow = QGraphicsDropShadowEffect(self)
        self.shadow.setBlurRadius(10)
        self.shadow.setColor(QColor(0, 0, 0, 80))
        self.shadow.setOffset(0, 2)
        self.setGraphicsEffect(self.shadow)
        
        layout = QVBoxLayout(self)
        layout.setAlignment(Qt.AlignmentFlag.AlignCenter)
        layout.setSpacing(12)
        layout.setContentsMargins(12, 15, 12, 15)
        
        # Game Icon
        self.icon_label = QLabel()
        self.icon_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        icon = QIcon.fromTheme(self.game["icon"])
        if not icon.isNull():
            self.icon_label.setPixmap(icon.pixmap(QSize(64, 64)))
        else:
            fallback = QIcon.fromTheme("application-games")
            self.icon_label.setPixmap(fallback.pixmap(QSize(64, 64)))
            
        # Game Title
        self.title_label = QLabel(self.game["name"])
        self.title_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.title_label.setWordWrap(True)
        font = QFont()
        font.setPointSize(10)
        font.setBold(True)
        self.title_label.setFont(font)
        
        layout.addWidget(self.icon_label)
        layout.addWidget(self.title_label)

    def enterEvent(self, event):
        """Hover entrance animation: border highlight, lifting drop shadow, and scaling feeling."""
        self.setStyleSheet("""
            QFrame {
                background-color: rgba(42, 46, 50, 0.95);
                border: 2px solid #3daee9;
                border-radius: 12px;
            }
            QLabel { color: #ffffff; background: transparent; border: none; }
        """)
        self.shadow.setBlurRadius(18)
        self.shadow.setColor(QColor(61, 174, 233, 100)) # Highlight neon glow
        self.shadow.setOffset(0, 4)
        super().enterEvent(event)

    def leaveEvent(self, event):
        """Hover exit animation: returns cleanly back to rest state."""
        self.setStyleSheet("""
            QFrame {
                background-color: rgba(35, 38, 41, 0.85);
                border: 1px solid rgba(49, 54, 59, 0.8);
                border-radius: 12px;
            }
            QLabel { color: #eff0f1; background: transparent; border: none; }
        """)
        self.shadow.setBlurRadius(10)
        self.shadow.setColor(QColor(0, 0, 0, 80))
        self.shadow.setOffset(0, 2)
        super().leaveEvent(event)

    def mousePressEvent(self, event):
        if event.button() == Qt.MouseButton.LeftButton:
            self.launch_callback(self.game)
        super().mousePressEvent(event)


class DictionaryApp(QMainWindow):
    def __init__(self):
        super().__init__()
        self.PASSWORD = "AZHfhszmh#786_abbas007_4252"
        self.all_games = []
        self.visible_games = []
        self.unlocked = False
        self.clear_timer = QTimer()
        self.clear_timer.timeout.connect(self.clear_status)
        self.init_ui()
        self.load_games()
        
    def init_ui(self):
        self.setWindowTitle("Dictionary")
        self.setMinimumSize(800, 600)
        self.setWindowIcon(QIcon.fromTheme("accessories-dictionary"))
        
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
                border-radius: 10px;
                color: #eff0f1;
                padding-left: 15px;
                padding-right: 15px;
                font-size: 14px;
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
                background: transparent;
                width: 10px;
            }
            QScrollBar::handle:vertical {
                background: rgba(77, 80, 82, 0.6);
                min-height: 30px;
                border-radius: 5px;
            }
            QScrollBar::handle:vertical:hover {
                background: #3daee9;
            }
        """)
        
        main_widget = QWidget()
        self.setCentralWidget(main_widget)
        self.main_layout = QVBoxLayout(main_widget)
        self.main_layout.setContentsMargins(35, 35, 35, 35)
        self.main_layout.setSpacing(20)
        
        # --- HEADER AREA ---
        self.header_container = QWidget()
        header_layout = QVBoxLayout(self.header_container)
        header_layout.setContentsMargins(0, 0, 0, 0)
        
        self.title = QLabel("Dictionary Lookup")
        title_font = QFont()
        title_font.setPointSize(24)
        title_font.setBold(True)
        self.title.setFont(title_font)
        
        self.instructions = QLabel("Search for definitions, etymologies, and spellings.")
        self.instructions.setStyleSheet("color: #7f8c8d; font-size: 13px; background: transparent;")
        
        header_layout.addWidget(self.title)
        header_layout.addWidget(self.instructions)
        self.main_layout.addWidget(self.header_container)
        
        # --- INPUT CONTROLS ---
        self.input_field = QLineEdit()
        self.input_field.setPlaceholderText("Enter word to look up...")
        self.input_field.returnPressed.connect(self.on_enter_pressed)
        self.input_field.setMinimumHeight(50)
        self.main_layout.addWidget(self.input_field)
        
        self.search_bar = QLineEdit()
        self.search_bar.setPlaceholderText("🔍 Search your gaming vault...")
        self.search_bar.textChanged.connect(self.filter_games)
        self.search_bar.setMinimumHeight(50)
        self.search_bar.setVisible(False)
        self.main_layout.addWidget(self.search_bar)
        
        self.status_label = QLabel("")
        self.status_label.setStyleSheet("color: #da4453; font-weight: bold; background: transparent;")
        self.main_layout.addWidget(self.status_label)
        
        # --- FLUID RESPONSIVE GRID AREA ---
        self.games_container = QWidget()
        self.games_container.setStyleSheet("background-color: transparent;")
        self.games_layout = QGridLayout(self.games_container)
        self.games_layout.setSpacing(20)
        self.games_layout.setContentsMargins(10, 10, 10, 10)
        
        self.scroll_area = QScrollArea()
        self.scroll_area.setWidget(self.games_container)
        self.scroll_area.setWidgetResizable(True)
        self.scroll_area.setVisible(False)
        self.main_layout.addWidget(self.scroll_area)
        
        self.main_layout.addStretch()
        
    def on_enter_pressed(self):
        if self.input_field.text() == self.PASSWORD:
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
        
        seen = set()
        unique_games = []
        for game in self.all_games:
            if game["name"] not in seen:
                seen.add(game["name"])
                unique_games.append(game)
                
        self.all_games = sorted(unique_games, key=lambda g: g["name"].lower())
        self.visible_games = self.all_games.copy()
        
    def reveal_launcher_ui(self):
        self.title.setText("Games Vault")
        self.instructions.setText("Interactive library. Fluid columns will adjust automatically as you resize.")
        self.input_field.setVisible(False)
        self.search_bar.setVisible(True)
        self.scroll_area.setVisible(True)
        self.search_bar.setFocus()
        self.render_grid()
        
    def render_grid(self):
        """Calculates adaptive layouts dynamically based on actual viewport space."""
        while self.games_layout.count():
            widget = self.games_layout.takeAt(0).widget()
            if widget:
                widget.deleteLater()
        
        if not self.visible_games:
            no_games = QLabel("No tracking matches found inside the vault.")
            no_games.setStyleSheet("color: #7f8c8d; font-size: 15px; font-style: italic;")
            self.games_layout.addWidget(no_games, 0, 0)
            return

        # Calculate columns gracefully dynamically based on current scroll area geometry
        card_width = 150
        spacing = 20
        available_width = self.scroll_area.viewport().width() - 20
        
        columns = max(1, available_width // (card_width + spacing))
        
        for idx, game in enumerate(self.visible_games):
            card = GameCard(game, self.launch_game)
            row = idx // columns
            col = idx % columns
            self.games_layout.addWidget(card, row, col)

    def resizeEvent(self, event: QResizeEvent):
        """Forces the grid layout to re-flow immediately when window dimensions scale."""
        super().resizeEvent(event)
        if self.unlocked:
            self.render_grid()

    def filter_games(self, text):
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
