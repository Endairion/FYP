import threading
import json
from peer import Peer
from login import LoginForm
from PyQt5.QtWidgets import QApplication


if __name__ == "__main__":

    app = QApplication([])
    login_form = LoginForm()
    login_form.show()
    app.exec_()





