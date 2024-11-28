from PySide6.QtGui import Qt, QFont
from PySide6.QtWidgets import QVBoxLayout, QWidget, QLabel, QTextEdit


class BriefInfoWidget(QWidget):
    def __init__(self, event=None, parent=None):
        super(BriefInfoWidget, self).__init__(parent)

        self.layout = QVBoxLayout(self)
        self.summary_label = QLabel("Краткая информация о совещании")
        self.summary_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.summary_label.setFont(QFont('Roboto Slab', 10))
        self.layout.addWidget(self.summary_label)

        self.summary_text = QTextEdit()
        self.summary_text.setFont(QFont('Roboto Slab'))
        self.summary_text.setStyleSheet("""
            QTextEdit { background-color: #E0FFFF;
            border-radius: 4px;
            padding: 8px;
            border-style: solid;
            border-width: 2px;
            border-color: #000000;
        }""")
        self.summary_text.setReadOnly(True)
        self.layout.addWidget(self.summary_text)

        if event:
            self.update_info(event)

    def update_info(self, event):
        """Update the brief information display with the event details."""
        summary = f"""
            Тема: {event['title']}
            Дата: {event['date']}
            Время: {event['time']}
        """
        self.summary_text.setText(summary)
