import sys
import sqlite3
from PyQt5.QtWidgets import (
    QApplication,
    QWidget,
    QVBoxLayout,
    QLabel,
    QLineEdit,
    QPushButton,
    QMessageBox,
)
from PyQt5.QtGui import QPixmap
from main_window import MainWindow
from changepasswordwindow import ChangePasswordWin


class LoginWindow(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Welcome")
        self.setGeometry(100, 100, 300, 150)

        layout = QVBoxLayout()

        image_label = QLabel(self)
        pixmap = QPixmap(
            "company_logo.png"
        )  # подставьте путь к вашему логотипу компании
        image_label.setPixmap(pixmap)
        self.username_label = QLabel("Username:")
        self.password_label = QLabel("Password:")
        self.username_input = QLineEdit()
        self.password_input = QLineEdit()
        self.password_input.setEchoMode(QLineEdit.Password)
        self.login_button = QPushButton("Login")

        layout.addWidget(image_label)
        layout.addWidget(self.username_label)
        layout.addWidget(self.username_input)
        layout.addWidget(self.password_label)
        layout.addWidget(self.password_input)
        layout.addWidget(self.login_button)

        self.setLayout(layout)

        self.login_button.clicked.connect(self.on_login)
        self.change_password_button = QPushButton("Change Password")
        layout.addWidget(self.change_password_button)
        self.change_password_button.clicked.connect(self.open_change_password_window)

    def open_change_password_window(self):
        self.window = LoginWindow()
        self.window.show()
        self.change_password_window = ChangePasswordWin()
        self.change_password_window.show()
        self.close()

    def on_login(self):
        username = self.username_input.text()
        conn = sqlite3.connect("warehouse.db")
        cursor = conn.cursor()
        cursor.execute("SELECT password FROM users WHERE username=?", (username,))
        passwordindb = cursor.fetchone()[0]
        password = self.password_input.text()

        if username == "admin" and password == passwordindb:
            self.main_window = MainWindow()
            self.main_window.show()
            self.close()
        else:
            QMessageBox.warning(self, "Login", "Incorrect username or password")


if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = LoginWindow()
    window.show()
    sys.exit(app.exec_())
