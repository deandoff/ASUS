from PySide6.QtWidgets import (
    QMainWindow,
    QTabWidget,
)

from ui.widgets.main_page_widget import MainPageWidget
from ui.widgets.admin_panel_widget import AdminPanelWidget
from ui.windows.meeting_calendar_window import CalendarWidget


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()

        # Параметры окна
        self.setWindowTitle("Главное окно приложения")
        self.setGeometry(200, 100, 800, 600)
        self.setMinimumSize(800, 600)

        # Список совещаний
        self.meetings = []

        self.status_bar = self.statusBar()
        self.status_bar.showMessage("Приложение запущено.")

        # Настройка вкладок
        tabs = QTabWidget()
        tabs.setTabPosition(QTabWidget.North)
        tabs.setMovable(True)

        # Создание вкладок
        main_tab = MainPageWidget(self.meetings, self.status_bar)
        calendar_tab = CalendarWidget(self.meetings)

        # Передача ссылки на календарь в MainPageWidget
        main_tab.calendar_widget = calendar_tab

        tabs.addTab(main_tab, "Главное")
        tabs.addTab(calendar_tab, "Календарь")
        tabs.addTab(AdminPanelWidget(), "Дополнительно")

        self.setCentralWidget(tabs)
