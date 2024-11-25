from PySide6.QtWidgets import QApplication, QMainWindow, QVBoxLayout, QWidget
from event_list_widget import EventListWidget  # Импортируем наш виджет


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Главное окно")

        # Данные мероприятий
        events = [
            {"date": "25 Ноября", "title": "Исповедь основного обучения :)", "time": "18:00 - 19:00", "details": "Старшие волны поделятся, как проходило их обучение."},
            {"date": "26 Ноября", "title": "Мастер-класс (уровень 1) по 3D моделированию", "time": "14:00 - 15:00", "details": "В лаборатории можно пройти серию практических занятий."},
            {"date": "27 Ноября", "title": "АНГЛИЙСКИЙ совместно с Лигой Студентов", "time": "18:30 - 20:00", "details": "Занятия, которые проводят Лига студентов для всех желающих."},
            {"date": "27 Ноября", "title": "Meetup: Введение в Kubernetes", "time": "19:00 - 20:00", "details": "На мероприятии участники знакомятся с основами Kubernetes."},
        ]

        # Главный виджет
        main_widget = QWidget()
        main_layout = QVBoxLayout()
        main_widget.setLayout(main_layout)

        # Добавляем EventListWidget
        event_list_widget = EventListWidget(events)
        main_layout.addWidget(event_list_widget)

        # Устанавливаем главный виджет
        self.setCentralWidget(main_widget)


if __name__ == "__main__":
    app = QApplication([])
    window = MainWindow()
    window.show()
    app.exec()
