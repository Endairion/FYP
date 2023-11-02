from PyQt5 import uic, QtCore, QtGui, QtWidgets
import sys

class MainWindow(QtWidgets.QMainWindow):
    def __init__(self):
        super(MainWindow, self).__init__()
        uic.loadUi('ui_main.ui', self)

        self.dragging = False
        self.offset = QtCore.QPoint()
        self.setWindowFlags(QtCore.Qt.FramelessWindowHint)
        self.setAttribute(QtCore.Qt.WA_TranslucentBackground)

        self.minimizeButton.clicked.connect(self.showMinimized)
        self.maximizeButton.clicked.connect(self.toggleMaximize)
        self.closeButton.clicked.connect(self.close)

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
if __name__ == "__main__":
    app = QtWidgets.QApplication(sys.argv)

    window = MainWindow()
    window.show()

    sys.exit(app.exec_())