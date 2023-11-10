from PyQt5 import QtWidgets, uic
from PyQt5.QtWidgets import QApplication, QMainWindow, QVBoxLayout, QScrollArea, QWidget, QSizePolicy
from PyQt5.QtCore import pyqtSlot

class CardWidget(QtWidgets.QWidget):
    def __init__(self, parent=None):
        super(CardWidget, self).__init__(parent)

        # Load the UI file
        uic.loadUi('card.ui', self)

    def set_file_info(self, file_id, file_name, file_size, sender):
        self.filename.setText(file_name)
        self.fileSize.setText(file_size)
        self.sender.setText(sender)
        # Connect the download button's clicked signal to a slot
        self.downloadButton.clicked.connect(lambda: self.request_download(file_id))

    @pyqtSlot()
    def request_download(self, file_id):
        # Send the file_id to the relay node to request for a download
        # This is a placeholder, replace with your actual implementation
        print(f"Requesting download for file_id: {file_id}")

class MainWindow(QMainWindow):
    def __init__(self):
        super(MainWindow, self).__init__()

        # Load the UI file
        uic.loadUi('ui_main.ui', self)

        # Create a container QWidget and set a layout for it
        scroll_area = self.findChild(QScrollArea, "scrollArea_2")
        container = scroll_area.findChild(QWidget, "your_widget_name")

        # Get the layout of the QWidget
        layout = container.layout()

        # Hardcoded file information
        file_info_list = [
            {"file_id": 1, "file_name": "file1.txt", "file_size": "1KB", "sender": "user1"},
        ]

        for file_info in file_info_list:
            card = CardWidget()
            card.set_file_info(**file_info)
            card.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Fixed)  # Set the size policy
            card.setMinimumSize(550, 100)  # Set a minimum size for the CardWidget instances
            layout.addWidget(card)

        self.active_css = """
        QPushButton {
            border: none;
            background-color: rgb(91,90,90);
        }
        """

        # Set the container QWidget as the widget of the QScrollArea
        self.home.setWidget(self.page_my_upload)
        self.homeButton.setStyleSheet(self.active_css)

        

if __name__ == "__main__":
    app = QApplication([])
    window = MainWindow()
    window.show()
    app.exec_()