from PyQt5 import uic, QtCore, QtGui, QtWidgets
from peer import Peer
import threading
import re
import sys

class Worker(QtCore.QThread):
    finished = QtCore.pyqtSignal()

    def __init__(self, func, *args, **kwargs):
        super().__init__()
        self.func = func
        self.args = args
        self.kwargs = kwargs

    def run(self):
        self.func(*self.args, **self.kwargs)
        self.finished.emit()

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

        self.login_worker = Worker(self.thread_handler, 'login', username, password)
        self.login_worker.finished.connect(self.clear_line_edits)
        self.login_worker.finished.connect(self.open_main_window)
        self.login_worker.start()

        # thread = threading.Thread(target=self.thread_handler, args=('login',username, password))
        # thread.start()
        # self.login_finished.wait()
        # self.open_main_window()

    def handle_register(self):
        # Get username and password from input fields
        username = self.lineEdit.text()
        password = self.lineEdit_2.text()

        if not self.validate_password(password):
            QtWidgets.QMessageBox.warning(self, 'Error', 'Invalid password. Password must be at least 8 characters long and contain at least one uppercase letter, one lowercase letter, and one special character.')
            return
        
        self.register_worker = Worker(self.thread_handler, 'register', username, password)
        self.register_worker.finished.connect(self.clear_line_edits)
        self.register_worker.start()

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
    def open_main_window(self):
        self.main_window = MainWindow(self.node, self)  # Pass the node to MainWindow
        self.main_window.show()
        self.hide()

    def clear_line_edits(self):
        self.lineEdit.clear()
        self.lineEdit_2.clear()

    def startNode(self):
        self.node_worker = Worker(self.node.start)
        self.node_worker.start()
        # self.thread = threading.Thread(target=self.node.start, args=())
        # self.thread.start()

class MainWindow(QtWidgets.QMainWindow):
    def __init__(self, node, login_form):
        super(MainWindow, self).__init__()
        uic.loadUi('ui_main.ui', self)
        self.node = node
        self.dragging = False
        self.offset = QtCore.QPoint()
        self.login_form = login_form
        self.setWindowFlags(QtCore.Qt.FramelessWindowHint)
        self.setAttribute(QtCore.Qt.WA_TranslucentBackground)

        self.minimizeButton.clicked.connect(self.showMinimized)
        self.maximizeButton.clicked.connect(self.toggleMaximize)
        self.closeButton.clicked.connect(self.close_program)
        self.logoutButton.clicked.connect(self.logout)
        self.username.setText(self.node.username)

        # Set the initial CSS for the QPushButton
        self.default_css = """
        QPushButton {
            border: none;
            background-color: rgba(0,0,0,0);
        }
        QPushButton:hover {
            background-color: rgb(91,90,90);
        }
        QPushButton:pressed {    
            background-color: rgba(0,0,0,0);
        }
        """
        self.active_css = """
        QPushButton {
            border: none;
            background-color: rgb(91,90,90);
        }
        """

        # Create a dictionary to map buttons to pages
        self.button_page_map = {
            self.uploadButton: self.page_upload,
            self.downloadButton: self.page_download,
            self.deleteButton: self.page_delete
        }

        # Connect the buttons to the activate_page method
        for button in self.button_page_map.keys():
            button.setStyleSheet(self.default_css)
            button.clicked.connect(self.activate_page)

        self.uploadButton.setStyleSheet(self.active_css)
        self.stackedWidget.setCurrentWidget(self.page_upload)

    def reset_button_styles(self):
        # Reset the style of all buttons
        for button in self.button_page_map.keys():
            button.setStyleSheet(self.default_css)

    def activate_page(self):
        # Get the button that sent the signal
        button = self.sender()

        # Reset the styles of all buttons and set the style of the active button
        self.reset_button_styles()
        button.setStyleSheet(self.active_css)

        # Set the current widget of the stackedWidget to the page associated with the button
        self.stackedWidget.setCurrentWidget(self.button_page_map[button])
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

    def toggleMaximize(self):
        # Toggle between maximized and normal window state
        if self.isMaximized():
            self.showNormal()
            self.maximizeButton.setIcon(QtGui.QIcon("./icons/square.svg"))
            self.maximizeButton.setToolTip("Maximize")
        else:
            self.showMaximized()
            self.maximizeButton.setIcon(QtGui.QIcon("./icons/minimize.svg"))
            self.maximizeButton.setToolTip("Restore")

    def close_program(self):
        # Confirm close
        reply = QtWidgets.QMessageBox.question(self, 'Confirm Close', 'Are you sure you want to close the program?', QtWidgets.QMessageBox.Yes | QtWidgets.QMessageBox.No, QtWidgets.QMessageBox.No)
        if reply == QtWidgets.QMessageBox.Yes:
            # Send logout request to Relay Node
            response = self.node.logout()
            if response['success']:
                print(response['message'])
                self.close()
            else:
                QtWidgets.QMessageBox.warning(self, 'Error', response['message'])

    def logout(self):
        # Confirm logout
        reply = QtWidgets.QMessageBox.question(self, 'Confirm Logout', 'Are you sure you want to logout?', QtWidgets.QMessageBox.Yes | QtWidgets.QMessageBox.No, QtWidgets.QMessageBox.No)
        if reply == QtWidgets.QMessageBox.Yes:
            # Send logout request to Relay Node
            response = self.node.logout()
            if response['success']:
                print(response['message'])
                self.close()
                # Show old login form
                self.login_form.show()
            else:
                QtWidgets.QMessageBox.warning(self, 'Error', response['message'])

        

def main():
    app = QtWidgets.QApplication(sys.argv)

    login_form = LoginForm()
    login_form.show()

    sys.exit(app.exec_())

if __name__ == "__main__":
    main()