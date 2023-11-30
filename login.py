import math
import pickle
from PyQt5 import uic, QtCore, QtGui, QtWidgets
from PyQt5.QtWidgets import QApplication, QMainWindow, QVBoxLayout, QScrollArea, QWidget, QSizePolicy
from PyQt5.QtCore import pyqtSlot
from blockchain import Blockchain
from metadata import FileMetadata
from peer import Peer
import threading
import re
import sys

class CardWidget(QtWidgets.QWidget):
    def __init__(self, parent=None):
        super(CardWidget, self).__init__(parent)
        self.file_id = None

        # Load the UI file
        uic.loadUi('card.ui', self)

    def set_file_info(self, file_id, file_name, file_size, sender):
        self.file_id = file_id
        self.filename.setText(file_name)
        self.fileSize.setText(file_size)
        self.sender.setText(sender)

class Worker(QtCore.QThread):
    finished = QtCore.pyqtSignal()
    successful = QtCore.pyqtSignal(str)
    failed = QtCore.pyqtSignal(str)

    def __init__(self, func, *args, **kwargs):
        super().__init__()
        self.func = func
        self.args = args
        self.kwargs = kwargs

    def run(self):
        result = self.func(*self.args, **self.kwargs)
        if result is None:
            return
        elif result[0]:  # If the function was successful
            self.successful.emit(result[1])
        else:  # If the function failed
            self.failed.emit(result[1])
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
        username = self.lineEdit.text().strip()
        password = self.lineEdit_2.text().strip()

        if not self.validate_inputs(username, password):
            QtWidgets.QMessageBox.warning(self, 'Error', 'Username or password cannot be empty')
            return        

        self.login_worker = Worker(self.thread_handler, 'login', username, password)
        self.login_worker.finished.connect(self.clear_line_edits)
        self.login_worker.successful.connect(self.open_main_window)
        self.login_worker.failed.connect(self.show_login_error)
        self.login_worker.start()



    def handle_register(self):
        # Get username and password from input fields
        username = self.lineEdit.text().strip()
        password = self.lineEdit_2.text().strip()
        if not self.validate_inputs(username, password):
            QtWidgets.QMessageBox.warning(self, 'Error', 'Username or password cannot be empty')
            return
        
        if not self.validate_password(password):
            QtWidgets.QMessageBox.warning(self, 'Error', 'Invalid password. Password must be at least 8 characters long and contain at least one uppercase letter, one lowercase letter, and one special character.')
            return
        
        self.register_worker = Worker(self.thread_handler, 'register', username, password)
        self.register_worker.finished.connect(self.clear_line_edits)
        self.register_worker.successful.connect(self.show_register_successful)
        self.register_worker.failed.connect(self.show_login_error)
        self.register_worker.start()

        #thread = threading.Thread(target=self.thread_handler, args=('register',username, password))
        #thread.start()
    def show_register_successful(self, message):
        QtWidgets.QMessageBox.information(self, 'Success', message)
    def show_login_error(self, message):
        QtWidgets.QMessageBox.warning(self, 'Error', message)

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
                return self.result
            else:
                self.result = (False, response['message'])
                return self.result

        elif type == 'register':
            response = self.node.register(username, password)
            if response['success']:
                self.result = (True, response['message'])
                return self.result
            else:
                self.result = (False, response['message'])
                return self.result

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

    def validate_inputs(self, username, password):
        if not username or not password:
            return False
        return True

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
        self.uploadButton.clicked.connect(self.upload_file)

        # Create a container QWidget and set a layout for it
        scroll_area = self.findChild(QScrollArea, "scrollArea_2")
        container = scroll_area.findChild(QWidget, "scrollAreaWidgetContents_3")

        # Get the layout of the QWidget
        layout = QVBoxLayout()
        container.setLayout(layout)

        file_info_list = self.display_file()

        if file_info_list:
            for file_info in file_info_list:
                card = CardWidget()
                card.set_file_info(**file_info)
                card.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Fixed)  # Set the size policy
                card.setMinimumSize(550, 100)  # Set a minimum size for the CardWidget instances
                layout.addWidget(card)
                card.downloadButton.clicked.connect(lambda: self.request_download(card.file_id))

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
            self.myUploadButton: self.page_my_upload,
            self.homeButton: self.page_home,
        }

        # Connect the buttons to the activate_page method
        for button in self.button_page_map.keys():
            button.setStyleSheet(self.default_css)
            button.clicked.connect(self.activate_page)

        self.homeButton.setStyleSheet(self.active_css)
        self.stackedWidget.setCurrentWidget(self.page_home)

    def upload_file(self):
        file_path, _ = QtWidgets.QFileDialog.getOpenFileName()

        self.node.upload(file_path)

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

    def updateBlockchain(self):
        self.node.update_blockchain()



    def display_file(self):
        # Load the blockchain from 'blockchain.pkl'
        blockchain = Blockchain.load_from_file('blockchain.pkl')

        if blockchain is None or len(blockchain.chain) == 0:
            return None
        # Extract the blocks from the blockchain
        blocks = blockchain.extract_file_info()

        # Convert the file information to the required format
        formatted_file_info_list = []
        for i, block in enumerate(blocks):
            # Skip the genesis block
            if i == 0:
                continue

            # Check if block.data is a FileMetadata object
            if isinstance(block.data, FileMetadata):
                # Access the file attributes
                file_info = block.data

                formatted_file_info = {
                    "file_id": file_info.file_id,
                    "file_name": file_info.file_name,
                    "file_size": self.convert_size(file_info.file_size),
                    "sender": file_info.sender,
                }
                formatted_file_info_list.append(formatted_file_info)

        return formatted_file_info_list
    
    def convert_size(self, size_bytes):
        if size_bytes == 0:
            return "0B"
        size_name = ("B", "KB", "MB", "GB")
        i = int(math.floor(math.log(size_bytes, 1024)))
        p = math.pow(1024, i)
        s = round(size_bytes / p, 2)
        return "%s %s" % (s, size_name[i])
    
    def request_download(self, file_id):
        self.node.download(file_id)




def main():
    app = QtWidgets.QApplication(sys.argv)

    login_form = LoginForm()
    login_form.show()

    sys.exit(app.exec_())

if __name__ == "__main__":
    main()