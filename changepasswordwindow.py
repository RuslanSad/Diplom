import sys
from PyQt5.QtWidgets import (
    QApplication,
    QWidget,
    QVBoxLayout,
    QLabel,
    QLineEdit,
    QPushButton,
    QMessageBox,
)
import sqlite3


class ChangePasswordWin(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Change Password")
        self.setGeometry(100, 100, 300, 150)

        layout = QVBoxLayout()

        self.old_password_input = QLineEdit()
        self.old_password_input.setEchoMode(QLineEdit.Password)
        self.new_password_input = QLineEdit()
        self.new_password_input.setEchoMode(QLineEdit.Password)
        self.confirm_password_input = QLineEdit()
        self.confirm_password_input.setEchoMode(QLineEdit.Password)
        self.change_password_button = QPushButton("Change Password")

        layout.addWidget(QLabel("Old Password:"))
        layout.addWidget(self.old_password_input)
        layout.addWidget(QLabel("New Password:"))
        layout.addWidget(self.new_password_input)
        layout.addWidget(QLabel("Confirm Password:"))
        layout.addWidget(self.confirm_password_input)
        layout.addWidget(self.change_password_button)

        self.setLayout(layout)

        self.change_password_button.clicked.connect(self.on_change_password)

    def on_change_password(self):
        username = "admin"
        old_password = self.old_password_input.text()
        new_password = self.new_password_input.text()
        confirm_password = self.confirm_password_input.text()
        conn = sqlite3.connect("warehouse.db")
        cursor = conn.cursor()

        cursor.execute("SELECT password FROM users WHERE username=?", (username,))
        old_password_indb = cursor.fetchone()[0]

        if old_password == old_password_indb:
            if new_password == confirm_password:
                new_passwordindb = new_password
                cursor.execute(
                    "UPDATE users SET password=? WHERE username=?",
                    (new_passwordindb, username),
                )
                conn.commit()

                QMessageBox.information(
                    self, "Change Password", "Password changed successfully!"
                )
            else:
                QMessageBox.warning(
                    self,
                    "Change Password",
                    "New password and confirm password do not match",
                )
        else:
            QMessageBox.warning(self, "Change Password", "Incorrect old password")
        conn.close()


if __name__ == "__main__":
    app = QApplication(sys.argv)
    windows = ChangePasswordWin()
    windows.show()
    sys.exit(app.exec_())
