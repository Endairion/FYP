from PyQt5 import uic, QtCore, QtGui, QtWidgets
from peer import Peer
import threading

class LoginForm(QtWidgets.QWidget):
    def __init__(self):
        super().__init__()
        uic.loadUi("login.ui", self)
        self.result = None
        self.node = Peer()
        self.startNode()
       

        # Connect login button to handler function
        self.closeButton.clicked.connect(self.close)
        self.pushButton.clicked.connect(self.handle_login)
        self.pushButton_2.clicked.connect(self.handle_register)

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
            QtWidgets.QApplication.quit()

    def handle_login(self):
        # Get username and password from input fields
        username = self.lineEdit.text()
        password = self.lineEdit_2.text()

        response = self.node.login(username, password)

        if response['success']:
            self.result = (True, response['message'])
            self.close()
        else:
            self.result = (False, response['message'])
            QtWidgets.QMessageBox.warning(self, 'Error', response['message'])


    def handle_register(self):
        # Get username and password from input fields
        username = self.lineEdit.text()
        password = self.lineEdit_2.text()

        response = self.node.register(username, password)

        if response['success']:
            self.result = (True, response['message'])
            self.close()
        else:
            self.result = (False, response['message'])
            QtWidgets.QMessageBox.warning(self, 'Error', response['message'])

    def startNode(self):
        threading.Thread(target=self.node.start, args=()).start()




if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    login_form = LoginForm()
    login_form.show()
    sys.exit(app.exec_())