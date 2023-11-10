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

        self.active_css = """
        QPushButton {
            border: none;
            background-color: rgb(91,90,90);
        }
        """

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

        self.stackedWidget.setCurrentWidget(self.page_my_upload)
        self.myUploadButton.setStyleSheet(self.active_css)
        self.homeButton.setStyleSheet(self.default_css)

        # Create a container QWidget and set a layout for it
        scroll_area = self.findChild(QScrollArea, "scrollArea_2")
        container = scroll_area.findChild(QWidget, "scrollAreaWidgetContents_3")

        # Get the layout of the QWidget
        layout = QVBoxLayout()
        container.setLayout(layout)

        # Hardcoded file information
        file_info_list = [
            {"file_id": 1, "file_name": "file.txt", "file_size": "3.76 KB", "sender": "Endairion"},
        ]

        for file_info in file_info_list:
            card = CardWidget()
            card.set_file_info(**file_info)
            card.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Fixed)  # Set the size policy
            card.setMinimumSize(550, 100)  # Set a minimum size for the CardWidget instances
            layout.addWidget(card)



        # Set the container QWidget as the widget of the QScrollArea


        

if __name__ == "__main__":
    app = QApplication([])
    window = MainWindow()
    window.show()
    app.exec_()