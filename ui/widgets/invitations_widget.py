import psycopg2
from PySide6.QtWidgets import QWidget, QVBoxLayout, QLabel, QTableWidget, QTableWidgetItem, QPushButton
from psycopg2.extras import DictCursor


class InvitationsWidget(QWidget):
    def __init__(self, user_id):
        """
        Инициализация виджета для отображения приглашений.
        :param user_id: ID пользователя.
        """
        super().__init__()
        self.user_id = user_id
        self.db_url = "dbname=postgres user=postgres password=postgres host=localhost port=5432"

        # Настройка интерфейса
        self.layout = QVBoxLayout()

        self.title_label = QLabel("Ваши приглашения:")
        self.layout.addWidget(self.title_label)

        self.refresh_button = QPushButton("Обновить приглашения")
        self.refresh_button.clicked.connect(self.load_invitations)
        self.layout.addWidget(self.refresh_button)

        # Таблица для отображения приглашений
        self.table = QTableWidget(self)
        self.table.setColumnCount(7)  # 7 колонок: Тема, Дата, Время, Статус, Дата приглашения, Принять, Отклонить
        self.table.setHorizontalHeaderLabels(
            ["Тема", "Дата", "Время", "Статус", "Дата приглашения", "Принять", "Отклонить"])
        self.layout.addWidget(self.table)

        self.setLayout(self.layout)

        # Загружаем данные о приглашениях
        self.load_invitations()

    def load_invitations(self):
        """
        Загружает приглашения пользователя из базы данных.
        """
        invitations = self.get_invitations_for_user(self.user_id)

        # Заполняем таблицу
        self.table.setRowCount(len(invitations))
        for row, invitation in enumerate(invitations):
            self.table.setItem(row, 0, QTableWidgetItem(invitation['theme']))
            self.table.setItem(row, 1, QTableWidgetItem(invitation['meeting_date']))
            self.table.setItem(row, 2, QTableWidgetItem(invitation['meeting_time']))
            self.table.setItem(row, 3, QTableWidgetItem(invitation['status']))
            self.table.setItem(row, 4, QTableWidgetItem(invitation['invite_date']))

            # Добавляем кнопки "Принять" и "Отклонить"
            accept_button = QPushButton("Принять")
            accept_button.clicked.connect(lambda checked, id=invitation['id']: self.accept_invitation(id))
            self.table.setCellWidget(row, 5, accept_button)

            decline_button = QPushButton("Отклонить")
            decline_button.clicked.connect(lambda checked, id=invitation['id']: self.decline_invitation(id))
            self.table.setCellWidget(row, 6, decline_button)

    def get_invitations_for_user(self, user_id):
        """
        Получает приглашения для указанного пользователя из базы данных.
        :param user_id: ID пользователя.
        :return: Список приглашений.
        """
        query = """
            SELECT 
                i.id AS id,
                m.theme AS theme,
                c.date AS meeting_date,
                c.time AS meeting_time,
                i.status AS status,
                i.invite_date AS invite_date
            FROM Invitations i
            JOIN Meetings m ON i.meeting_id = m.id
            JOIN Calendar c ON c.meeting_id = m.id
            WHERE i.user_id = %s;
        """
        try:
            # Подключение к базе данных
            conn = psycopg2.connect(self.db_url)
            with conn.cursor(cursor_factory=DictCursor) as cursor:
                cursor.execute(query, (user_id,))
                result = cursor.fetchall()
                return [
                    {
                        "id": row["id"],
                        "theme": row["theme"],
                        "meeting_date": str(row["meeting_date"]),
                        "meeting_time": str(row["meeting_time"]),
                        "status": row["status"],
                        "invite_date": row["invite_date"].strftime("%Y-%m-%d %H:%M:%S")
                    }
                    for row in result
                ]
        except psycopg2.Error as e:
            print(f"Ошибка при работе с базой данных: {e}")
            return []
        finally:
            conn.close()

    def accept_invitation(self, invitation_id):
        """
        Обрабатывает принятие приглашения.
        :param invitation_id: ID приглашения.
        """
        self.update_invitation_status(invitation_id, 'accepted')
        self.load_invitations()


    def decline_invitation(self, invitation_id):
        """
        Обрабатывает отклонение приглашения.
        :param invitation_id: ID приглашения.
        """
        self.update_invitation_status(invitation_id, 'declined')
        self.load_invitations()

    def update_invitation_status(self, invitation_id, status):
        """
        Обновляет статус приглашения и изменяет статус участника в базе данных.
        :param invitation_id: ID приглашения.
        :param status: Новый статус ('accepted' или 'declined').
        """
        try:
            # Подключение к базе данных
            conn = psycopg2.connect(self.db_url)
            with conn.cursor() as cursor:
                # Получаем meeting_id перед удалением приглашения
                select_query = "SELECT meeting_id FROM invitations WHERE id = %s;"
                cursor.execute(select_query, (invitation_id,))
                meeting_id_row = cursor.fetchone()

                if meeting_id_row is not None:
                    meeting_id = meeting_id_row[0]  # Извлекаем meeting_id

                    # Обновляем статус участника
                    update_query = """
                        UPDATE participant
                        SET status = %s
                        WHERE meeting_id = %s
                        AND id_from_users = %s;
                    """
                    cursor.execute(update_query, (status, meeting_id, self.user_id))

                    # Удаляем приглашение
                    delete_query = "DELETE FROM invitations WHERE id = %s;"
                    cursor.execute(delete_query, (invitation_id,))

                    conn.commit()
                else:
                    print("Приглашение не найдено.")
        except psycopg2.Error as e:
            print(f"Ошибка при работе с базой данных: {e}")
        finally:
            conn.close()