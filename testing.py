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
        container = QWidget()
        layout = QVBoxLayout()
        container.setLayout(layout)

        # Hardcoded file information
        file_info_list = [
            {"file_id": 1, "file_name": "file1.txt", "file_size": "1KB", "sender": "user1"},
            {"file_id": 2, "file_name": "file2.txt", "file_size": "2KB", "sender": "user2"},
            {"file_id": 3, "file_name": "file3.txt", "file_size": "3KB", "sender": "user3"},
            {"file_id": 4, "file_name": "file4.txt", "file_size": "4KB", "sender": "user4"},
            {"file_id": 5, "file_name": "file5.txt", "file_size": "5KB", "sender": "user5"},
            {"file_id": 5, "file_name": "file5.txt", "file_size": "5KB", "sender": "user5"},
            {"file_id": 5, "file_name": "file5.txt", "file_size": "5KB", "sender": "user5"},
            {"file_id": 5, "file_name": "file5.txt", "file_size": "5KB", "sender": "user5"},
            {"file_id": 5, "file_name": "file5.txt", "file_size": "5KB", "sender": "user5"},
            {"file_id": 5, "file_name": "file5.txt", "file_size": "5KB", "sender": "user5"},
        ]

        for file_info in file_info_list:
            card = CardWidget()
            card.set_file_info(**file_info)
            card.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Fixed)  # Set the size policy
            card.setMinimumSize(550, 100)  # Set a minimum size for the CardWidget instances
            layout.addWidget(card)

        # Set the container QWidget as the widget of the QScrollArea
        self.home.setWidget(container)

if __name__ == "__main__":
    app = QApplication([])
    window = MainWindow()
    window.show()
    app.exec_()