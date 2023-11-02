from PyQt5 import uic, QtCore, QtGui, QtWidgets
from peer import Peer
import threading
import re

class LoginForm(QtWidgets.QWidget):
    def __init__(self):
        super().__init__()
        uic.loadUi("login.ui", self)
        self.result = None
        self.node = Peer()
        self.thread = None
        self.startNode()
       

        # Connect login button to handler function
        self.closeButton.clicked.connect(self.close)
        self.pushButton.clicked.connect(self.handle_login)
        self.pushButton_2.clicked.connect(self.handle_register)
        self.hideButton.clicked.connect(self.toggle_password_visibility)

        # Initialize variables for tracking mouse movement
        self.dragging = False
        self.offset = QtCore.QPoint()
        self.setWindowFlags(QtCore.Qt.FramelessWindowHint)
        self.setAttribute(QtCore.Qt.WA_TranslucentBackground)

    def mousePressEvent(self, event):
        # Check if mouse is pressed within the form area
        if event.button() == QtCore.Qt.LeftButton and self.rect().contains(event.pos()):
            self.dragging = True
            self.offset = event.pos()

    def mouseMoveEvent(self, event):
        # Move the window if the mouse is being dragged
        if self.dragging:
            self.move(self.pos() + event.pos() - self.offset)

    def mouseReleaseEvent(self, event):
        # Stop dragging the window when the mouse is released
        if event.button() == QtCore.Qt.LeftButton:
            self.dragging = False

    def close(self):
        reply = QtWidgets.QMessageBox.question(self, 'Exit', 'Are you sure you want to exit?', QtWidgets.QMessageBox.Yes | QtWidgets.QMessageBox.No, QtWidgets.QMessageBox.No)
        if reply == QtWidgets.QMessageBox.Yes:
            self.node.stop()
            QtWidgets.QApplication.quit()

    def exit(self):
        QtWidgets.QApplication.quit()

    def toggle_password_visibility(self):
        if self.lineEdit_2.echoMode() == QtWidgets.QLineEdit.Password:
            self.lineEdit_2.setEchoMode(QtWidgets.QLineEdit.Normal)
            self.hideButton.setIcon(QtGui.QIcon("./icons/eye.svg"))
        else:
            self.lineEdit_2.setEchoMode(QtWidgets.QLineEdit.Password)
            self.hideButton.setIcon(QtGui.QIcon("./icons/eye-off.svg"))

    def handle_login(self):
        # Get username and password from input fields
        username = self.lineEdit.text()
        password = self.lineEdit_2.text()

        thread = threading.Thread(target=self.thread_handler, args=('login',username, password))
        thread.start()


    def handle_register(self):
        # Get username and password from input fields
        username = self.lineEdit.text()
        password = self.lineEdit_2.text()

        if not self.validate_password(password):
            QtWidgets.QMessageBox.warning(self, 'Error', 'Invalid password. Password must be at least 8 characters long and contain at least one uppercase letter, one lowercase letter, and one special character.')
            return
        
        #thread = threading.Thread(target=self.thread_handler, args=('register',username, password))
        #thread.start()

    def validate_password(self, password):
        # Check password length
        if len(password) < 8:
            return False

        # Check for at least one uppercase letter
        if not re.search(r'[A-Z]', password):
            return False

        # Check for at least one lowercase letter
        if not re.search(r'[a-z]', password):
            return False

        # Check for at least one special character
        if not re.search(r'[!@#$%^&*(),.?":{}|<>]', password):
            return False

        return True

    def thread_handler(self, type, username, password):
        if type == 'login':
            response = self.node.login(username, password)
            if response['success']:
                self.result = (True, response['message'])
                print(self.result)
                # Pass the Peer object to main.py
                from main import MainWindow
                window = MainWindow()
                self.exit()
                window.username = self.node.username
                window.show()
            else:
                self.result = (False, response['message'])
                QtWidgets.QMessageBox.warning(self, 'Error', response['message'])

        elif type == 'register':
            response = self.node.register(username, password)
            if response['success']:
                self.result = (True, response['message'])
                QtWidgets.QMessageBox.information(self, 'Success', response['message'])
                # Clear the line edits for username and password
                self.username.clear()
                self.password.clear()
            else:
                self.result = (False, response['message'])
                QtWidgets.QMessageBox.warning(self, 'Error', response['message'])

        else:
            print(f"Unknown request type: {type}")
            return

    def startNode(self):
        self.thread = threading.Thread(target=self.node.start, args=())
        self.thread.start()



if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    login_form = LoginForm()
    login_form.show()
    sys.exit(app.exec_())