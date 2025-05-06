import sys
import os
from PyQt6.QtWidgets import (
    QApplication, QMainWindow, QPushButton, QLabel,
    QFileDialog, QVBoxLayout, QWidget, QComboBox, QSystemTrayIcon, QMenu
)
from PyQt6.QtGui import QAction
from PyQt6.QtGui import QIcon
from PyQt6.QtCore import Qt
from floating_window import FloatingWindow

class SettingsWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.floating_window = None
        self.setWindowTitle("Mascot Settings")
        self.setGeometry(500, 350, 400, 150)

        self.layout = QVBoxLayout()

        self.load_button = QPushButton("Load GIF/Image")
        self.load_button.clicked.connect(self.load_image)
        self.layout.addWidget(self.load_button)

        self.load_3d_button = QPushButton("Load 3D Model (.glb/.obj)")
        self.load_3d_button.clicked.connect(self.load_3d)
        self.layout.addWidget(self.load_3d_button)

        self.default_anim_label = QLabel("Built-in Animations:")
        self.layout.addWidget(self.default_anim_label)

        self.default_anim_combo = QComboBox()
        self.default_anim_combo.addItems(["None", "balls", "snake", "stars"])
        self.layout.addWidget(self.default_anim_combo)

        self.start_default_button = QPushButton("Start Selected Animation")
        self.start_default_button.clicked.connect(self.start_default_animation)
        self.layout.addWidget(self.start_default_button)

        self.stop_button = QPushButton("Stop Animation")
        self.stop_button.clicked.connect(self.stop_animation)
        self.layout.addWidget(self.stop_button)

        container = QWidget()
        container.setLayout(self.layout)
        self.setCentralWidget(container)

        # System tray
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

    def load_image(self):
        file_path, _ = QFileDialog.getOpenFileName(self, "Select GIF or Image", "", "Images (*.gif *.png *.jpg *.jpeg)")
        if file_path:
            self.start_floating(animation_type="image", file_path=file_path)

    def load_3d(self):
        file_path, _ = QFileDialog.getOpenFileName(self, "Select 3D Model", "", "3D Files (*.glb *.obj *.stl)")
        if file_path:
            self.start_floating(animation_type="3d", file_path=file_path)

    def start_default_animation(self):
        animation = self.default_anim_combo.currentText()
        if animation != "None":
            self.start_floating(animation_type="built_in", built_in_animation=animation)

    def start_floating(self, animation_type, file_path=None, built_in_animation=None):
        if self.floating_window:
            self.floating_window.close()

        self.floating_window = FloatingWindow(animation_type, file_path, built_in_animation)
        self.floating_window.show()

    def stop_animation(self):
        if self.floating_window:
            self.floating_window.close()
            self.floating_window = None

    def quit_app(self):
        if self.floating_window:
            self.floating_window.close()
        QApplication.quit()
