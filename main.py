from PySide6.QtCore import QSize
from PySide6.QtWidgets import QApplication, QMainWindow, QPushButton
from src.witcher3_modmenu_changer import (
    IDs,
    IDs2,
    CONFIG_FILE,
    XML_LOCATION,
    BACKUP_DIR,
    EXCLUDED_FILES_XML,
)
import sys


class MainApp(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setFixedSize(QSize(1280, 720))
        self.setWindowTitle("Witcher 3 Modmenu Changer")
        button = QPushButton("Press Me!")
        button.setCheckable(True)
        button.clicked.connect(self.print_ids)
        button.clicked.connect(self.the_button_was_toggled)
        self.setCentralWidget(button)

    def print_ids(self):
        print(*IDs, *IDs2, sep=",")

    def the_button_was_toggled(self, checked):
        print("Checked?", checked)


app = QApplication(sys.argv)
window = MainApp()
window.show()

app.exec()
