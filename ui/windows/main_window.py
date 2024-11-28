from PySide6.QtWidgets import (
    QMainWindow,
    QTabWidget,
)

from ui.widgets.invitations_widget import InvitationsWidget
from ui.widgets.main_page_widget import MainPageWidget
from ui.widgets.admin_panel_widget import AdminPanelWidget
from ui.widgets.meeting_calendar_widget import CalendarWidget


class MainWindow(QMainWindow):
    def __init__(self, user_data):
        super().__init__()

        self.user_data = user_data

        # Параметры окна
        self.setWindowTitle("Главное окно приложения")
        self.setGeometry(200, 100, 800, 600)
        self.setMinimumSize(800, 600)

        # Список совещаний
        self.meetings = []

        self.status_bar = self.statusBar()
        self.status_bar.showMessage(f"Добро пожаловать!")

        # Настройка вкладок
        tabs = QTabWidget()
        tabs.setTabPosition(QTabWidget.North)
        tabs.setMovable(False)

        # Создание вкладок
        main_tab = MainPageWidget(self.meetings, self.status_bar, self.user_data)
        calendar_tab = CalendarWidget(self.meetings)

        # Передача ссылки на календарь в MainPageWidget
        main_tab.calendar_widget = calendar_tab

        tabs.addTab(main_tab, "Главное")
        tabs.addTab(calendar_tab, "Календарь")
        if self.user_data['role'] == "ADMIN":
            tabs.addTab(AdminPanelWidget(), "Дополнительно")
        tabs.addTab(InvitationsWidget(self.user_data['id']), "Приглашения")

        self.setStyleSheet("""
            QMainWindow {
                background-color: #F0FFFF;
                border: 0px;
            }
            QTabWidget::pane {
                border: 0px;
                background-color: #F0FFFF;
            }
            QTabBar::tab {
                background: #E0FFFF;
                border-style: solid; /* Устанавливает стиль границы */
                border-width: 2px; /* Толщина границы */
                border-color: #808080; /* Цвет границы */
                padding: 8px;
                margin: 5px;
                border-radius: 4px;
                font-family: Roboto Slab;
                font-size: 16px;
            }
            QTabBar::tab:selected {
                background: #87CEEB;
                border-color: #000000;
            }
        """)

        self.setCentralWidget(tabs)
