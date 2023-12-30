import hashlib
import sqlite3
from PyQt5.QtWidgets import QWidget, QLabel, QLineEdit, QPushButton, QMessageBox
from PyQt5.QtCore import QTimer, Qt

from MarkdownEditor import MarkdownEditor

class Login(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowFlags(self.windowFlags() | Qt.Window)
        QTimer.singleShot(3000, self.initUI)
        #self.initUI()

    def initUI(self):
        self.setGeometry(300, 300, 300, 220)
        self.setWindowTitle('Авторизация')

        self.label_login = QLabel(self)
        self.label_login.setText('Логин:')
        self.label_login.move(50, 50)

        self.input_login = QLineEdit(self)
        self.input_login.move(110, 50)

        self.label_password = QLabel(self)
        self.label_password.setText('Пароль:')
        self.label_password.move(50, 80)

        self.input_password = QLineEdit(self)
        self.input_password.move(110, 80)
        self.input_password.setEchoMode(QLineEdit.Password)

        self.btn_login = QPushButton('Войти', self)
        self.btn_login.move(110, 120)
        self.btn_login.clicked.connect(self.login)

        self.show()

    def login(self):
        login = self.input_login.text()
        password = self.input_password.text()

        conn = sqlite3.connect('DataBase.db')
        cursor = conn.cursor()
        
        hash_password = hashlib.md5(password.encode()).hexdigest()
        print(hash_password)
        cursor.execute(f"SELECT * FROM users WHERE login='{login}' AND password_hash='{hash_password}';")
        result = cursor.fetchall()
        print(result)
        
        if not len(result):
            QMessageBox.warning(self, 'Ошибка', 'Неверный логин или пароль')
        else:
            QMessageBox.information(self, 'Успех', 'Вы успешно авторизовались')
            self.hide()  # Скрываем окно авторизации
            self.markdownEditor = MarkdownEditor()  # Создаем и открываем окно редактора Markdown
            self.markdownEditor.show()
