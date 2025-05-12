import sys
import pyodbc
from PyQt6.QtWidgets import QApplication
from Functions import login_user, set_current_user, get_user_role, signup_user, get_current_user
from Main_Window import MainWindow

if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec())
