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
from PyQt5.QtSql import QSqlDatabase
from PyQt5.QtGui import QPixmap
import main_window
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
        )
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
        logins = ['admin','Ruslan','Valya']
        conn = sqlite3.connect("warehouse.db")
        cursor = conn.cursor()
        cursor.execute("SELECT password FROM users WHERE username=?", (username,))
        if username not in logins:
            QMessageBox.warning(self, "Error", "Incorrect username or password")
        else:
            passwordindb = cursor.fetchone()[0]
            password = self.password_input.text()
            if password == passwordindb:
                self.main_window = main_window.MainWindow()
                self.main_window.show()
                self.close()
            else:
                QMessageBox.warning(self, "Error", "Incorrect username or password")


if __name__ == "__main__":
    app = QApplication(sys.argv)
    db = QSqlDatabase.addDatabase("QSQLITE")
    db.setDatabaseName("warehouse.db")
    if not db.open():
        print("Cannot open database")
        sys.exit(1)
    window = LoginWindow()
    window.show()
    sys.exit(app.exec_())
