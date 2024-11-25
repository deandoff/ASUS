# main.py

from PySide6.QtWidgets import QApplication
from main_app_window import MainAppWindow

if __name__ == "__main__":
    app = QApplication([])

    window = MainAppWindow()
    window.show()

    app.exec()
