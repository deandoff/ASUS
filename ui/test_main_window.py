import sys
from PySide6.QtWidgets import (
    QApplication,
    QMainWindow,
    QTabWidget,
)

from ui.widgets.main_page_widget import MainPageWidget


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()

        # Параметры окна
        self.setWindowTitle("Главное окно приложения")
        self.setGeometry(200, 100, 800, 600)
        self.setMinimumSize(800, 600)

        self.meetings = []

        self.status_bar = self.statusBar()
        self.status_bar.showMessage("Приложение запущено.")

        # Настройка вкладок
        tabs = QTabWidget()
        tabs.setTabPosition(QTabWidget.North)
        tabs.setMovable(True)

        main_tab = MainPageWidget(self.meetings, self.status_bar)
        tabs.addTab(main_tab, "Главное")

        # make calendar_tab

        self.setCentralWidget(tabs)




if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = MainWindow()
    window.resize(800, 600)  # Устанавливаем размер окна
    window.show()
    app.exec()
