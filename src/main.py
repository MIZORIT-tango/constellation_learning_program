from models import Constellation
from database import get_session
session = next(get_session())
from fill_db import load_constellations_from_file
from PyQt5.QtWidgets import (QApplication, QMainWindow, QLabel,
                             QPushButton, QVBoxLayout, QWidget,
                             QMessageBox, QHBoxLayout)
from PyQt5.QtGui import QPixmap
from PyQt5.QtCore import Qt
import sys
import random


class ConstellationGame(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Угадай созвездие")
        self.setGeometry(300, 200, 800, 600)
        self.current_constellation = None
        self.hint = None
        self.score = 0
        self.init_ui()
        self.load_game_data()

    def init_ui(self):
        """Инициализация пользовательского интерфейса"""
        self.central_widget = QWidget()
        self.setCentralWidget(self.central_widget)

        # Основные элементы интерфейса
        self.image_label = QLabel()
        self.image_label.setAlignment(Qt.AlignCenter)
        self.image_label.setStyleSheet("""
            QLabel {
                border: 5px solid;
                border-radius: 12px;
                border-image: linear-gradient(45deg, #CE9FFC, #7367F0, #CE9FFC);
                padding: 3px;
                background-color: #1E0D33;
            }
        """)

        self.answer_buttons = []
        for _ in range(8):  # создаю две строки кнопок (8 кнопок)
            btn = QPushButton()
            btn.setStyleSheet("""
                                QPushButton { background-color: lightblue; color: black}
                                QPushButton:hover { background-color: indigo; color: lightblue}
                                QPushButton:pressed { background-color: darkblue; }
                            """)
            btn.clicked.connect(self.check_answer)
            self.answer_buttons.append(btn)

        self.hint_button = QPushButton()
        self.hint_button.clicked.connect(self.show_hint)
        self.hint_button.setText(f'Получить подсказку')
        self.hint_button.setStyleSheet("""
                                    QPushButton { grey; color: white}
                                    QPushButton:hover { background-color: white; color: indigo}"
                                    QPushButton:pressed { background-color: white;
                                       """)

        self.hint_label = QLabel()
        self.hint_label.setAlignment(Qt.AlignCenter)

        self.score_label = QLabel(f"Очки: {self.score}")
        self.score_label.setAlignment(Qt.AlignCenter)

        # Разметка
        layout = QVBoxLayout()
        layout.addWidget(self.image_label)

        buttons_layout_1row = QHBoxLayout()
        for btn in self.answer_buttons[:4]:
            buttons_layout_1row.addWidget(btn)

        buttons_layout_2row = QHBoxLayout()
        for btn in self.answer_buttons[4:]:
            buttons_layout_2row.addWidget(btn)

        layout.addLayout(buttons_layout_1row)
        layout.addLayout(buttons_layout_2row)
        layout.addWidget(self.hint_button)
        layout.addWidget(self.hint_label)
        layout.addWidget(self.score_label)
        self.central_widget.setLayout(layout)

    def load_game_data(self):
        """Загрузка данных из базы"""
        self.constellations = session.query(Constellation).all()
        if not self.constellations:
            QMessageBox.critical(self, "Ошибка", "База данных пуста! Загрузите данные сначала.")
            return False
        self.next_question()

    def next_question(self):
        """Генерация нового вопроса"""
        self.current_constellation = random.choice(self.constellations)

        # Загрузка изображения
        pixmap = QPixmap()
        pixmap.loadFromData(self.current_constellation.image)
        self.image_label.setPixmap(pixmap.scaled(400, 400, Qt.KeepAspectRatio))

        # Подбор вариантов ответа
        answers = [c.rus_name for c in random.sample(
                  [c for c in self.constellations if c != self.current_constellation], 7)
                  ]
        answers.append(self.current_constellation.rus_name)
        random.shuffle(answers)

        for btn, answer in zip(self.answer_buttons, answers):
            btn.setText(answer)

    def show_hint(self):
        self.hint = self.current_constellation.hint
        self.hint_label.setText(self.hint)

    def check_answer(self):
        """Проверка выбранного ответа"""
        sender = self.sender()
        if sender.text() == self.current_constellation.rus_name:
            self.score += 1
            QMessageBox.information(self, "Правильно!",
                                    f"Это {self.current_constellation.rus_name}!")
        else:
            QMessageBox.critical(self, "Ошибка",
                                 f"Неправильно! Это {self.current_constellation.rus_name}.")

        self.score_label.setText(f"Очки: {self.score}")
        self.hint_label.setText(None)
        self.next_question()


def initialize_database():
    """Инициализация базы данных"""
    if not session.query(Constellation).first():
        result = load_constellations_from_file(
            "constellations_name.txt",
            "constellations_hints.txt"
        )
        if not result:
            QMessageBox.critical(None, "Ошибка",
                                 "Не удалось загрузить данные в БД!")
            return False
    return True


if __name__ == "__main__":
    try:
        app = QApplication(sys.argv)
        app.setStyleSheet("""
            QMainWindow {
                background: qlineargradient(x1:0, y1:0, x2:0, y2:1,
                    stop:0 #CE9FFC,      /* Яркий фиолетовый (верх) */
                    stop:0.4 #A582FF,    /* Средний тон */
                    stop:0.7 #8A63D8,    /* Тёмно-фиолетовый */
                    stop:1 #6A4F9E);     /* Самый тёмный (низ) */
                color: white;            /* Белый текст для контраста */
                font-family: 'Segoe UI';
            }
            QLabel, QPushButton {
                color: white;
                background-color: transparent;
                font-size: 14px;
            }
            QPushButton {
                background-color: rgba(255, 255, 255, 0.2);
                border: 1px solid white;
                border-radius: 4px;
                padding: 5px 15px;
            }
            QPushButton:hover {
                background-color: rgba(255, 255, 255, 0.3);
            }
            QMessageBox {
                background-color: #6A4F9E;
            }
            
            QMessageBox QLabel {
                color: white;
                font-size: 14px;
            }
            QMessageBox QPushButton {
                background-color: rgba(255, 255, 255, 0.2);
                color: white;
                border: 1px solid white;
                border-radius: 4px;
                padding: 5px 15px;
                min-width: 80px;
            }
            QMessageBox QPushButton:hover {
                background-color: rgba(255, 255, 255, 0.1);
            }
        """)

        if not initialize_database():
            QMessageBox.critical(None, "Ошибка", "Не удалось загрузить данные!")
            sys.exit(1)

        game = ConstellationGame()
        game.show()

        ret = app.exec_()
        sys.exit(ret)

    except Exception as e:
        print(f"Critical error: {str(e)}")
        sys.exit(1)