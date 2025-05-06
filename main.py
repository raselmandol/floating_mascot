import sys
from PyQt6.QtWidgets import QApplication
from settings_window import SettingsWindow

def main():
    app = QApplication(sys.argv)
    window = SettingsWindow()
    window.show()
    sys.exit(app.exec())

if __name__ == "__main__":
    main()
