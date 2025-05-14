# settings_window.py
import sys
import threading
import keyboard
import pygame
from PyQt6.QtWidgets import (
    QApplication, QMainWindow, QPushButton, QLabel,
    QFileDialog, QVBoxLayout, QWidget, QComboBox, QSystemTrayIcon, QMenu
)
from PyQt6.QtGui import QAction, QIcon
from PyQt6.QtCore import Qt
from floating_window import FloatingWindow

class SettingsWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        pygame.mixer.init()
        self.floating_window = None
        self.music_file = None
        self.music_on = False

        self.setWindowTitle("Mascot Settings")
        self.setGeometry(500, 350, 400, 200)

        self.layout = QVBoxLayout()

        # GIF/Image loader
        self.load_button = QPushButton("Load GIF/Image")
        self.load_button.clicked.connect(self.load_image)
        self.layout.addWidget(self.load_button)

        # 3D model loader
        self.load_3d_button = QPushButton("Load 3D Model (.glb/.obj)")
        self.load_3d_button.clicked.connect(self.load_3d)
        self.layout.addWidget(self.load_3d_button)

        # Built-in animations
        self.default_anim_label = QLabel("Built-in Animations:")
        self.layout.addWidget(self.default_anim_label)

        self.default_anim_combo = QComboBox()
        self.default_anim_combo.addItems(["None", "balls", "snake", "stars"])
        self.layout.addWidget(self.default_anim_combo)

        self.start_default_button = QPushButton("Start Selected Animation")
        self.start_default_button.clicked.connect(self.start_default_animation)
        self.layout.addWidget(self.start_default_button)

        # Music controls
        self.music_button = QPushButton("Select Music")
        self.music_button.clicked.connect(self.select_music)
        self.layout.addWidget(self.music_button)

        self.stop_button = QPushButton("Stop Mascot / Music")
        self.stop_button.clicked.connect(self.stop_all)
        self.layout.addWidget(self.stop_button)

        # Wrap layout (container --> edit?)
        container = QWidget()
        container.setLayout(self.layout)
        self.setCentralWidget(container)

        # System tray (in list/work/to-do)
        self.tray_icon = QSystemTrayIcon(QIcon("icon.png"), self)
        tray_menu = QMenu()
        show_action = QAction("Show Settings", self)
        quit_action = QAction("Quit", self)
        tray_menu.addAction(show_action)
        tray_menu.addAction(quit_action)
        self.tray_icon.setContextMenu(tray_menu)
        show_action.triggered.connect(self.show)
        quit_action.triggered.connect(self.quit_app)
        self.tray_icon.show()

        # Global shortcuts listener (must)
        threading.Thread(target=self._listen_shortcuts, daemon=True).start()

    def load_image(self):
        path, _ = QFileDialog.getOpenFileName(
            self, "Select GIF or Image", "", "Images (*.gif *.png *.jpg *.jpeg)"
        )
        if path:
            self._start_window("image", file_path=path)

    def load_3d(self): # Will remove and rewrite this whole thing (next update)
        path, _ = QFileDialog.getOpenFileName(
            self, "Select 3D Model", "", "3D Files (*.glb *.obj *.stl)"
        )
        if path:
            self._start_window("3d", file_path=path)

    def start_default_animation(self):
        anim = self.default_anim_combo.currentText()
        if anim != "None":
            self._start_window("built_in", built_in_animation=anim)

    def select_music(self):
        path, _ = QFileDialog.getOpenFileName(
            self, "Select Music File", "", "Audio Files (*.mp3 *.wav)"
        )
        if path:
            self.music_file = path
            try:
                pygame.mixer.music.load(self.music_file)
                pygame.mixer.music.play(-1)
                self.music_on = True
            except Exception as e:
                print(f"Error playing music: {e}")
                self.music_on = False

    def stop_all(self):
        # Stop mascot window
        if self.floating_window:
            self.floating_window.close()
            self.floating_window = None
        # Pause music
        if self.music_on:
            pygame.mixer.music.pause()
            self.music_on = False

    def _start_window(self, animation_type, file_path=None, built_in_animation=None):
        if self.floating_window:
            self.floating_window.close()
        self.floating_window = FloatingWindow(
            animation_type, file_path, built_in_animation
        )
        self.floating_window.show()

    def _listen_shortcuts(self):
        # Toggle mascot visibility
        keyboard.add_hotkey('ctrl+alt+m', lambda: (
            self.floating_window.hide() if self.floating_window and self.floating_window.isVisible()
            else (self.floating_window.show() if self.floating_window else None)
        ))
        # Toggle music pause/unpause
        keyboard.add_hotkey('ctrl+alt+s', self._toggle_music)
        keyboard.wait()

    def _toggle_music(self):
        if not self.music_file:
            self.select_music()
            return
        if self.music_on:
            pygame.mixer.music.pause()
            self.music_on = False
        else:
            pygame.mixer.music.unpause()
            self.music_on = True

    def quit_app(self):
        self.stop_all()
        QApplication.quit()

if __name__ == "__main__":
    app = QApplication(sys.argv)
    win = SettingsWindow()
    win.show()
    sys.exit(app.exec())